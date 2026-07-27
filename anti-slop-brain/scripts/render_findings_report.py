#!/usr/bin/env python3
"""Lane 1 renderer: markdown report for a findings envelope.

The renderer adds no judgement. It reorders nothing, recomputes no severity
and no confidence, and invents no summary text. Everything it prints came
out of `synthesize_findings.py`, which is the only module allowed to decide
what a finding is. That separation is deliberate: a renderer that quietly
reranks is a second, unaudited scoring pass.

The report is laid out in the order a reviewer actually needs it:

1. Header with the review id, the artifact, and the reference date.
2. The firewall rules the report was produced under, so a reader who never
   saw the source knows what this document refuses to claim.
3. The severity by confidence matrix, which is the whole point of keeping
   the two axes apart. A HIGH severity finding at low confidence and a LOW
   severity finding at high confidence are different problems and a single
   merged score hides that.
4. Findings, already ordered by severity then confidence, each with its
   evidence span, the procedure that convicted it, and the procedure's own
   artifact.
5. Routed procedures: markers that fired and convicted nothing.
6. Procedures that were run and passed.
7. Refusals, including every candidate finding dropped for having no
   evidence span.

Determinism: the same envelope renders byte identical markdown. No clock
read; the date in the header is the envelope's reference date, which can be
overridden with `--reference-date`.

Usage:
    python3 scripts/render_findings_report.py --findings findings.json --output report.md

Exit codes: 0 rendered, 2 refused input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter_common import (  # noqa: E402
    CONFIDENCE_ORDER,
    EXIT_CLEAN,
    SEVERITY_ORDER,
    AdapterError,
    add_output_argument,
    parse_reference_date,
    read_json_input,
    run_adapter,
    validate_or_refuse,
    write_output,
)

TOOL = "render_findings_report"
SCHEMA = "findings.schema.json"


def span_line(span: dict) -> str:
    return (
        f"{span['path']}:{span['start_line']}:{span['start_column']}"
        f"-{span['end_line']}:{span['end_column']}"
    )


def fence(text: str) -> list[str]:
    return ["```text", text, "```"]


def render_matrix(findings: list[dict]) -> list[str]:
    lines = [
        "## Severity by confidence",
        "",
        "Severity is impact. Confidence is certainty that the finding is real. They are",
        "reported on two axes because a merged score hides the difference between a",
        "fabricated citation nobody is sure about and a stylistic tell everybody is.",
        "",
        "| severity | high | medium | low | total |",
        "| --- | --- | --- | --- | --- |",
    ]
    for severity in SEVERITY_ORDER:
        row = [severity]
        total = 0
        for confidence in CONFIDENCE_ORDER:
            count = sum(
                1
                for item in findings
                if item["severity"] == severity and item["confidence"] == confidence
            )
            total += count
            row.append(str(count))
        row.append(str(total))
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return lines


def render_finding(index: int, finding: dict) -> list[str]:
    lines = [
        f"### {index}. {finding['severity']} severity, {finding['confidence']} confidence",
        "",
        f"- Finding id: `{finding['finding_id']}`",
        f"- Defect kind: `{finding['defect_kind']}`",
        f"- Convicting procedure: `{finding['procedure']}`",
        f"- Origin: `{finding['origin']}`",
    ]
    if "scanner" in finding:
        lines.append(f"- Scanner rule: `{finding['scanner']}` / `{finding['rule']}`")
    if "routed_from_marker_id" in finding:
        lines.append(
            f"- Routed from marker: `{finding['routed_from_marker_id']}` "
            f"at evidence tier {finding.get('routed_from_tier')}"
        )
    if "ledger_source_id" in finding:
        lines.append(f"- Ledger source: `{finding['ledger_source_id']}`")
    if "corroborated_by" in finding:
        joined = ", ".join(f"`{rule}`" for rule in finding["corroborated_by"])
        lines.append(f"- Corroborated by: {joined}")
    lines.extend(
        [
            f"- Location: `{span_line(finding['evidence_span'])}`",
            "",
            finding["summary"],
            "",
            "Evidence span:",
            "",
        ]
    )
    lines.extend(fence(finding["evidence_span"]["text"]))
    lines.append("")
    if "procedure_artifact" in finding:
        lines.extend(["Procedure artifact:", ""])
        lines.extend(fence(finding["procedure_artifact"]))
        lines.append("")
    lines.extend(
        [
            f"Why this severity: {finding['why_severity']}",
            "",
            f"Why this confidence: {finding['why_confidence']}",
            "",
        ]
    )
    return lines


def render(payload: dict, reference_date: str) -> str:
    artifact = payload["artifact"]
    findings = payload["findings"]
    counts = payload["counts"]

    lines: list[str] = [
        f"# Anti-Slop findings: {artifact['title']}",
        "",
        f"- Review id: `{payload['review_id']}`",
        f"- Artifact id: `{artifact['artifact_id']}`",
        f"- Surface: `{artifact['surface']}`",
        f"- Reference date: {reference_date}",
    ]
    if "source_uri" in artifact:
        lines.append(f"- Source: {artifact['source_uri']}")
    if "word_count" in artifact:
        lines.append(f"- Word count: {artifact['word_count']}")
    if artifact.get("reviewed_paths"):
        joined = ", ".join(f"`{path}`" for path in artifact["reviewed_paths"])
        lines.append(f"- Reviewed paths: {joined}")
    lines.extend(
        [
            f"- Findings: {counts['total']} "
            f"(HIGH {counts['by_severity']['HIGH']}, "
            f"MEDIUM {counts['by_severity']['MEDIUM']}, "
            f"LOW {counts['by_severity']['LOW']})",
            "",
            "## What this report refuses to claim",
            "",
        ]
    )
    lines.extend(f"- {rule}" for rule in payload["firewall"])
    lines.append("")
    lines.extend(render_matrix(findings))

    lines.extend(["## Findings", ""])
    if findings:
        for index, finding in enumerate(findings, start=1):
            lines.extend(render_finding(index, finding))
    else:
        lines.extend(
            [
                "No finding was convicted. Nothing in this artifact was decided by a",
                "deterministic scanner or convicted by a structural procedure.",
                "",
            ]
        )

    lines.extend(["## Routed procedures", ""])
    if payload["routed_procedures"]:
        lines.extend(
            [
                "These markers fired and convicted nothing. A marker is a routing decision,",
                "not a conclusion. Run the suggested procedure and report its artifact.",
                "",
                "| marker | tier | suggested procedure | ledger source | observed |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in payload["routed_procedures"]:
            lines.append(
                "| `{marker}` | {tier} | `{procedure}` | {source} | {observed} |".format(
                    marker=item["marker_id"],
                    tier=item["tier"],
                    procedure=item["suggested_procedure"],
                    source=(
                        f"`{item['ledger_source_id']}`" if item.get("ledger_source_id") else "none in ledger"
                    ),
                    observed=item.get("observed", ""),
                )
            )
        lines.append("")
        for item in payload["routed_procedures"]:
            lines.append(f"- `{item['marker_id']}`: {item['reason']}")
        lines.append("")
    else:
        lines.extend(["Every marker that fired was consumed by a procedure that was run.", ""])

    lines.extend(["## Procedures that passed", ""])
    if payload["survived_procedures"]:
        for item in payload["survived_procedures"]:
            location = (
                f" at `{span_line(item['evidence_span'])}`" if "evidence_span" in item else ""
            )
            routed = (
                f", routed from `{item['routed_from_marker_id']}`"
                if "routed_from_marker_id" in item
                else ""
            )
            lines.append(f"- `{item['result_id']}`: `{item['procedure']}`{location}{routed}. {item['note']}")
        lines.append("")
    else:
        lines.extend(["No procedure was run that passed.", ""])

    lines.extend(["## Refusals", ""])
    if payload["refusals"]:
        lines.extend(
            [
                "| candidate | reason code | reason |",
                "| --- | --- | --- |",
            ]
        )
        for item in payload["refusals"]:
            lines.append(
                f"| `{item['candidate']}` | `{item['reason_code']}` | {item['reason']} |"
            )
        lines.append("")
    else:
        lines.extend(["Nothing was refused.", ""])

    lines.extend(["---", "", f"NOTE: {payload['note']}", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="render_findings_report.py",
        description="Render a findings envelope as markdown. Adds no judgement of its own.",
    )
    parser.add_argument(
        "--findings",
        required=True,
        help="Path to the synthesize_findings output, or - to read stdin.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date shown in the header. Overrides the value in the envelope.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    payload = read_json_input(args.findings, "findings envelope")
    if payload.get("tool") != "synthesize_findings":
        raise AdapterError(
            "not_a_findings_envelope",
            "input is not a synthesize_findings envelope",
            [
                {
                    "pointer": "/tool",
                    "keyword": "const",
                    "message": "run scripts/synthesize_findings.py first and feed its output here",
                }
            ],
        )
    validate_or_refuse(payload, SCHEMA, "findings envelope")
    reference_date = parse_reference_date(args.reference_date, payload.get("reference_date"))
    write_output(render(payload, reference_date), args.output)
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
