#!/usr/bin/env python3
"""Lane 2 renderer: markdown report for a marker cohort diff.

Like the findings renderer, this adds no judgement. It recomputes no tier,
reorders nothing, and decides nothing about staleness. All of that happened
in `synthesize_cohort_diff.py`.

The order of the report is the order a curator has to act in. Stale
evidence comes first, because a marker resting on a source whose
`refresh_due` has passed is being cited beyond its own expiry date and that
is the failure the whole lane exists to catch. Tier changes come next,
because a tier change changes what the marker is licensed to do. Additions
and removals come last, because they are the easiest to see and the least
likely to be missed.

Determinism: the same diff renders byte identical markdown. No clock read;
the header date is the diff's reference date.

Usage:
    python3 scripts/render_cohort_report.py --diff diff.json --output cohort-report.md

Exit codes: 0 rendered, 2 refused input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter_common import (  # noqa: E402
    EXIT_CLEAN,
    AdapterError,
    add_output_argument,
    parse_reference_date,
    read_json_input,
    run_adapter,
    validate_or_refuse,
    write_output,
)

TOOL = "render_cohort_report"
SCHEMA = "cohort-diff.schema.json"


def source_cell(item: dict) -> str:
    return f"`{item['ledger_source_id']}`" if item.get("ledger_source_id") else "none in ledger"


def render_marker_table(title: str, rows: list[dict], empty: str) -> list[str]:
    lines = [f"## {title}", ""]
    if not rows:
        lines.extend([empty, ""])
        return lines
    lines.extend(
        [
            "| marker | class | tier | routes to | surface | ledger source |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in rows:
        lines.append(
            f"| `{item['marker_id']}` | {item['marker_class']} | {item['tier']} | "
            f"`{item['routes_to']}` | `{item['surface']}` | {source_cell(item)} |"
        )
    lines.append("")
    return lines


def render(payload: dict, reference_date: str) -> str:
    counts = payload["counts"]
    before = payload["before"]
    after = payload["after"]

    lines: list[str] = [
        "# Anti-Slop marker cohort refresh",
        "",
        f"- Reference date: {reference_date}",
        f"- Before: `{before['cohort_id']}` dated {before['snapshot_date']}, "
        f"{before['marker_count']} markers",
        f"- After: `{after['cohort_id']}` dated {after['snapshot_date']}, "
        f"{after['marker_count']} markers",
        f"- Days between snapshots: {counts['days_between_snapshots']}",
        f"- Drift: {counts['added']} added, {counts['removed']} removed, "
        f"{counts['tier_changed']} retiered, {counts['routing_changed']} rerouted",
        f"- Stale evidence: {counts['stale_evidence']} markers resting on a source past its refresh date",
        f"- Unchanged: {counts['unchanged']}",
        "",
        "Marker lists rot. Vocabulary cohorts shift by model generation and human writing",
        "converges on model vocabulary, so a marker that was corpus validated in one",
        "snapshot can be folklore two snapshots later. This report is the mechanical",
        "record of that drift, not a judgement about any document.",
        "",
    ]

    lines.extend(["## Stale evidence", ""])
    if payload["stale_evidence"]:
        lines.extend(
            [
                "These markers rest on a ledger source whose `refresh_due` has passed relative",
                "to the reference date. Reverify the source or demote the marker. A marker",
                "cited past its own expiry date is folklore wearing a citation.",
                "",
                "| marker | tier | ledger source | refresh due | days overdue |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in payload["stale_evidence"]:
            lines.append(
                f"| `{item['marker_id']}` | {item['tier']} | {source_cell(item)} | "
                f"{item['refresh_due']} | {item['days_overdue']} |"
            )
        lines.append("")
    else:
        lines.extend(["Every marker rests on a source that is still inside its refresh window.", ""])

    lines.extend(["## Tier changes", ""])
    if payload["tier_changed"]:
        lines.extend(
            [
                "| marker | from | to | direction | ledger source |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in payload["tier_changed"]:
            lines.append(
                f"| `{item['marker_id']}` | {item['from_tier']} | {item['to_tier']} | "
                f"{item['direction']} | {source_cell(item)} |"
            )
        lines.append("")
        for item in payload["tier_changed"]:
            lines.append(f"- `{item['marker_id']}`: {item['consequence']}")
        lines.append("")
    else:
        lines.extend(["No marker changed evidence tier between these snapshots.", ""])

    lines.extend(["## Routing changes", ""])
    if payload["routing_changed"]:
        lines.extend(
            [
                "| marker | from procedure | to procedure |",
                "| --- | --- | --- |",
            ]
        )
        for item in payload["routing_changed"]:
            lines.append(
                f"| `{item['marker_id']}` | `{item['from_procedure']}` | `{item['to_procedure']}` |"
            )
        lines.append("")
    else:
        lines.extend(["No marker changed the structural procedure it routes to.", ""])

    lines.extend(render_marker_table("Added markers", payload["added"], "No marker was added."))
    lines.extend(
        render_marker_table("Removed markers", payload["removed"], "No marker was removed.")
    )

    lines.extend(["## Unchanged markers", ""])
    if payload["unchanged"]:
        lines.extend([", ".join(f"`{marker}`" for marker in payload["unchanged"]), ""])
    else:
        lines.extend(["No marker survived both snapshots with its tier and routing intact.", ""])

    lines.extend(["---", "", f"NOTE: {payload['note']}", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="render_cohort_report.py",
        description="Render a marker cohort diff as markdown. Adds no judgement of its own.",
    )
    parser.add_argument(
        "--diff",
        required=True,
        help="Path to the synthesize_cohort_diff output, or - to read stdin.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date shown in the header. Overrides the value in the diff.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    payload = read_json_input(args.diff, "cohort diff")
    if payload.get("tool") != "synthesize_cohort_diff":
        raise AdapterError(
            "not_a_cohort_diff",
            "input is not a synthesize_cohort_diff envelope",
            [
                {
                    "pointer": "/tool",
                    "keyword": "const",
                    "message": "run scripts/synthesize_cohort_diff.py first and feed its output here",
                }
            ],
        )
    validate_or_refuse(payload, SCHEMA, "cohort diff")
    reference_date = parse_reference_date(args.reference_date, payload.get("reference_date"))
    write_output(render(payload, reference_date), args.output)
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
