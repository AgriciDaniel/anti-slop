#!/usr/bin/env python3
"""Lane 2 importer: validate and normalize one dated marker cohort snapshot.

A marker cohort is the taxonomy as it stood on one day: every marker class,
its evidence tier, the structural procedure it routes to, and the ledger
source that carries its evidence together with that source's `refresh_due`.

Marker lists rot. Vocabulary cohorts shift by model generation, and human
speech is converging on model vocabulary, so a marker that was Tier 1 in one
snapshot can be folklore two snapshots later. That is why the snapshot
carries a date and why the refresh date travels with the marker rather than
living only in the ledger: the diff has to be computable from two files with
no lookup against a moving target.

What it refuses, always with a structured error envelope and a non-zero
exit rather than a traceback:

- text that is not valid JSON, or a top level value that is not an object
- any document that violates `schemas/marker-cohort.schema.json`
- a `snapshot_date` or `source_refresh_due` that is not a real ISO 8601
  calendar date
- a `source_url` that is not http or https
- a duplicate `marker_id`
- a Tier 1 or Tier 2 marker with no `ledger_source_id`, because a marker
  that claims measured evidence has to name the measurement

Determinism: no clock read. `--reference-date` is accepted and recorded so
that a downstream diff run and this run agree on the anchor date.

Usage:
    python3 scripts/ingest_marker_cohort.py --input tests/fixtures/sample-marker-cohort-a.json

Exit codes: 0 accepted, 2 refused.
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
    AdapterError,
    add_output_argument,
    collapse,
    date_value,
    dump_json,
    parse_reference_date,
    read_json_input,
    run_adapter,
    validate_or_refuse,
)

TOOL = "ingest_marker_cohort"
SCHEMA = "marker-cohort.schema.json"

MEASURED_TIERS = (1, 2)


def normalize_markers(rows: list) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        marker_id = row["marker_id"]
        if marker_id in seen:
            raise AdapterError(
                "duplicate_marker_id",
                f"marker_id {marker_id!r} appears more than once in this snapshot",
                [
                    {
                        "pointer": f"/markers/{index}/marker_id",
                        "keyword": "unique",
                        "message": "a cohort snapshot records each marker class exactly once",
                    }
                ],
            )
        seen.add(marker_id)
        ledger_source_id = row.get("ledger_source_id")
        if row["tier"] in MEASURED_TIERS and not isinstance(ledger_source_id, str):
            raise AdapterError(
                "unsourced_measured_marker",
                f"marker {marker_id!r} claims tier {row['tier']} but names no ledger source",
                [
                    {
                        "pointer": f"/markers/{index}/ledger_source_id",
                        "keyword": "required",
                        "message": (
                            "Tier 1 and Tier 2 assert that the effect was measured, so the "
                            "measurement has to be named. Only Tier 3 may be unsourced."
                        ),
                    }
                ],
            )
        entry = {
            "marker_class": collapse(row["marker_class"]),
            "marker_id": marker_id,
            "routes_to": row["routes_to"],
            "surface": row["surface"],
            "tier": row["tier"],
        }
        if isinstance(ledger_source_id, str):
            entry["ledger_source_id"] = ledger_source_id
        refresh_due = row.get("source_refresh_due")
        if isinstance(refresh_due, str):
            date_value(refresh_due, f"/markers/{index}/source_refresh_due")
            entry["source_refresh_due"] = refresh_due
        if isinstance(row.get("source_url"), str):
            entry["source_url"] = row["source_url"].strip()
        if isinstance(row.get("false_positive_class"), str) and row["false_positive_class"].strip():
            entry["false_positive_class"] = collapse(row["false_positive_class"])
        if isinstance(row.get("vault_note"), str) and row["vault_note"].strip():
            entry["vault_note"] = collapse(row["vault_note"])
        out.append(entry)
    return sorted(out, key=lambda item: item["marker_id"])


def build_envelope(document: dict, reference_date: str) -> dict:
    snapshot_date = document["snapshot_date"]
    date_value(snapshot_date, "/snapshot_date")
    envelope = {
        "cohort_id": document["cohort_id"],
        "envelope_version": ENVELOPE_VERSION,
        "markers": normalize_markers(document["markers"]),
        "note": ADAPTER_DISCLAIMER,
        "ok": True,
        "reference_date": reference_date,
        "schema": SCHEMA,
        "snapshot_date": snapshot_date,
        "tool": TOOL,
    }
    if isinstance(document.get("ledger_path"), str):
        envelope["ledger_path"] = document["ledger_path"].strip()
    if isinstance(document.get("notes"), str) and document["notes"].strip():
        envelope["notes"] = collapse(document["notes"])
    return envelope


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ingest_marker_cohort.py",
        description="Validate and normalize a dated marker cohort snapshot.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the marker cohort JSON, or - to read stdin.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date the refresh run is anchored to. Defaults to the snapshot date.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    document = read_json_input(args.input, "marker cohort")
    validate_or_refuse(document, SCHEMA, "marker cohort")
    reference_date = parse_reference_date(args.reference_date, document.get("snapshot_date"))
    dump_json(build_envelope(document, reference_date), args.output)
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
