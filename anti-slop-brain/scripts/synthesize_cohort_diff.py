#!/usr/bin/env python3
"""Lane 2 synthesis: diff two dated marker cohort snapshots.

Marker cohorts rot, which is the reason this lane exists at all. A marker
list written against one model generation drifts as vocabulary shifts and as
human writing converges on model vocabulary. A list that is never diffed
quietly becomes folklore while still being cited as evidence.

What this computes, all mechanically:

- added: marker ids present in the after snapshot and absent from before
- removed: marker ids present in before and absent from after
- tier_changed: same marker, different evidence tier, with a direction and
  a stated consequence, because a tier change is a change in what the
  marker is licensed to do rather than a bookkeeping detail
- routing_changed: same marker, different structural procedure
- stale_evidence: every marker in the after snapshot whose
  `source_refresh_due` has passed relative to `--reference-date`
- unchanged: same tier, same routing

Direction convention: a tier number that falls is a promotion, because the
evidence got stronger. Tier 1 is corpus validated, Tier 3 is folklore.

Determinism: `--reference-date` is required. Nothing here reads the clock,
and every array is sorted by marker id before it is serialized.

Usage:
    python3 scripts/synthesize_cohort_diff.py \\
        --before cohort-a.json --after cohort-b.json --reference-date 2026-07-28

Exit codes: 0 no drift and nothing stale, 1 drift or stale evidence, 2 refused input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter_common import (  # noqa: E402
    ADAPTER_DISCLAIMER,
    ENVELOPE_VERSION,
    EXIT_CLEAN,
    EXIT_FINDINGS,
    AdapterError,
    add_output_argument,
    date_value,
    dump_json,
    load_schema,
    parse_reference_date,
    read_json_input,
    run_adapter,
    validate_instance,
)

TOOL = "synthesize_cohort_diff"
SCHEMA = "cohort-diff.schema.json"

REF_KEYS = (
    "marker_id",
    "marker_class",
    "tier",
    "routes_to",
    "surface",
    "ledger_source_id",
    "source_refresh_due",
    "vault_note",
)

TIER_CONSEQUENCE = {
    ("promoted", 1): (
        "Promoted to Tier 1. It may now be reported with its figure and its source id, "
        "may be counted in a density threshold, and may route to a structural procedure. "
        "It still may not cause a hard failure on its own."
    ),
    ("promoted", 2): (
        "Promoted to Tier 2. It may now route to a structural procedure and may be counted "
        "in a density threshold alongside a Tier 1 signal, with the population level caveat "
        "stated every time it is reported."
    ),
    ("demoted", 2): (
        "Demoted to Tier 2. Any density threshold that counted it alone is now invalid; it "
        "may only be counted alongside a Tier 1 signal, and every report of it must carry "
        "the population level caveat."
    ),
    ("demoted", 3): (
        "Demoted to Tier 3 folklore. It may still be recorded and labelled as folklore, but "
        "it may no longer be counted in any density threshold and may only route to a "
        "structural procedure in a cluster of three or more."
    ),
}


def marker_ref(marker: dict) -> dict:
    return {key: marker[key] for key in REF_KEYS if key in marker}


def require_envelope(envelope: dict, label: str) -> None:
    if envelope.get("tool") != "ingest_marker_cohort" or envelope.get("ok") is not True:
        raise AdapterError(
            "not_a_cohort_envelope",
            f"{label} is not an accepted ingest_marker_cohort envelope",
            [
                {
                    "pointer": "/tool",
                    "keyword": "const",
                    "message": "run scripts/ingest_marker_cohort.py first and feed its output here",
                }
            ],
        )
    for key in ("cohort_id", "snapshot_date", "markers"):
        if key not in envelope:
            raise AdapterError(
                "not_a_cohort_envelope",
                f"{label} envelope is missing {key}",
                [{"pointer": f"/{key}", "keyword": "required", "message": "is required and missing"}],
            )


def snapshot_ref(envelope: dict) -> dict:
    return {
        "cohort_id": envelope["cohort_id"],
        "marker_count": len(envelope["markers"]),
        "snapshot_date": envelope["snapshot_date"],
    }


def tier_consequence(direction: str, to_tier: int) -> str:
    return TIER_CONSEQUENCE.get(
        (direction, to_tier),
        f"Tier changed and the marker is now {direction} to Tier {to_tier}.",
    )


def compute_stale(after: dict, reference: str) -> list[dict]:
    anchor = date_value(reference, "/reference_date")
    stale: list[dict] = []
    for marker in after["markers"]:
        refresh_due = marker.get("source_refresh_due")
        if not refresh_due:
            continue
        due = date_value(refresh_due, f"/markers/{marker['marker_id']}/source_refresh_due")
        if due > anchor:
            continue
        entry = {
            "days_overdue": (anchor - due).days,
            "marker_class": marker["marker_class"],
            "marker_id": marker["marker_id"],
            "refresh_due": refresh_due,
            "tier": marker["tier"],
        }
        if marker.get("ledger_source_id"):
            entry["ledger_source_id"] = marker["ledger_source_id"]
        if marker.get("vault_note"):
            entry["vault_note"] = marker["vault_note"]
        stale.append(entry)
    return sorted(stale, key=lambda item: (-item["days_overdue"], item["marker_id"]))


def diff(before: dict, after: dict, reference_date: str) -> dict:
    before_by_id = {marker["marker_id"]: marker for marker in before["markers"]}
    after_by_id = {marker["marker_id"]: marker for marker in after["markers"]}

    added = [marker_ref(after_by_id[key]) for key in sorted(set(after_by_id) - set(before_by_id))]
    removed = [marker_ref(before_by_id[key]) for key in sorted(set(before_by_id) - set(after_by_id))]

    tier_changed: list[dict] = []
    routing_changed: list[dict] = []
    unchanged: list[str] = []
    for key in sorted(set(before_by_id) & set(after_by_id)):
        old = before_by_id[key]
        new = after_by_id[key]
        moved = False
        if old["tier"] != new["tier"]:
            moved = True
            direction = "promoted" if new["tier"] < old["tier"] else "demoted"
            entry = {
                "consequence": tier_consequence(direction, new["tier"]),
                "direction": direction,
                "from_tier": old["tier"],
                "marker_class": new["marker_class"],
                "marker_id": key,
                "to_tier": new["tier"],
            }
            if new.get("ledger_source_id"):
                entry["ledger_source_id"] = new["ledger_source_id"]
            tier_changed.append(entry)
        if old["routes_to"] != new["routes_to"]:
            moved = True
            routing_changed.append(
                {
                    "from_procedure": old["routes_to"],
                    "marker_class": new["marker_class"],
                    "marker_id": key,
                    "to_procedure": new["routes_to"],
                }
            )
        if not moved:
            unchanged.append(key)

    stale = compute_stale(after, reference_date)
    span_days = (
        date_value(after["snapshot_date"], "/after/snapshot_date")
        - date_value(before["snapshot_date"], "/before/snapshot_date")
    ).days

    counts = {
        "added": len(added),
        "days_between_snapshots": span_days,
        "removed": len(removed),
        "routing_changed": len(routing_changed),
        "stale_evidence": len(stale),
        "tier_changed": len(tier_changed),
        "unchanged": len(unchanged),
    }
    drifted = bool(added or removed or tier_changed or routing_changed or stale)
    return {
        "added": added,
        "after": snapshot_ref(after),
        "before": snapshot_ref(before),
        "counts": counts,
        "envelope_version": ENVELOPE_VERSION,
        "note": ADAPTER_DISCLAIMER,
        "ok": not drifted,
        "reference_date": reference_date,
        "removed": removed,
        "routing_changed": routing_changed,
        "stale_evidence": stale,
        "tier_changed": tier_changed,
        "tool": TOOL,
        "unchanged": unchanged,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="synthesize_cohort_diff.py",
        description="Diff two dated marker cohort snapshots and flag stale evidence.",
    )
    parser.add_argument("--before", required=True, help="Earlier ingest_marker_cohort envelope.")
    parser.add_argument("--after", required=True, help="Later ingest_marker_cohort envelope.")
    parser.add_argument(
        "--reference-date",
        required=True,
        help="ISO date the refresh_due comparison is anchored to.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    before = read_json_input(args.before, "before cohort envelope")
    after = read_json_input(args.after, "after cohort envelope")
    require_envelope(before, "before cohort")
    require_envelope(after, "after cohort")
    reference_date = parse_reference_date(args.reference_date)

    if date_value(after["snapshot_date"], "/after/snapshot_date") < date_value(
        before["snapshot_date"], "/before/snapshot_date"
    ):
        raise AdapterError(
            "snapshots_out_of_order",
            "the after snapshot is dated earlier than the before snapshot",
            [
                {
                    "pointer": "/after/snapshot_date",
                    "keyword": "order",
                    "message": (
                        f"before is {before['snapshot_date']} and after is "
                        f"{after['snapshot_date']}; pass them the other way round"
                    ),
                }
            ],
        )

    payload = diff(before, after, reference_date)
    schema = load_schema(SCHEMA)
    errors = validate_instance(payload, schema, schema)
    if errors:
        raise AdapterError(
            "self_check_failed",
            "the cohort diff does not satisfy cohort-diff.schema.json",
            errors,
        )
    dump_json(payload, args.output)
    return EXIT_CLEAN if payload["ok"] else EXIT_FINDINGS


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
