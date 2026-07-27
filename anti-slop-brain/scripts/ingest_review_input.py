#!/usr/bin/env python3
"""Lane 1 importer: validate and normalize one review input document.

This is the only place in the review lane that touches operator supplied
JSON. Everything downstream consumes the canonical envelope this script
emits, so the shape checking, the date checking and the URL scheme checking
happen exactly once and in one file.

What it refuses, always with a structured error envelope and a non-zero
exit rather than a traceback:

- text that is not valid JSON, or a top level value that is not an object
- any document that violates `schemas/review-input.schema.json`
- a date that is not a real ISO 8601 calendar date
- a `source_uri` that is not http or https
- a `procedure_result` that points at a `routed_from_marker_id` which is
  not in `marker_hits`, because a dangling route hides a marker

What it normalizes:

- evidence spans get their optional columns filled in and their text
  whitespace collapsed, so the same span written two ways hashes the same
- every array is sorted by a stable key, so the envelope does not inherit
  the order the operator happened to write things in
- duplicate marker ids and duplicate procedure result ids are refused
  rather than silently deduplicated

Determinism: no clock read. The reference date comes from the document or
from `--reference-date`.

Usage:
    python3 scripts/ingest_review_input.py --input tests/fixtures/sample-review-input.json
    cat review.json | python3 scripts/ingest_review_input.py --input -

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
    dump_json,
    normalize_span,
    parse_reference_date,
    read_json_input,
    run_adapter,
    validate_or_refuse,
)

TOOL = "ingest_review_input"
SCHEMA = "review-input.schema.json"


def normalize_artifact(raw: dict) -> dict:
    artifact = {
        "artifact_id": raw["artifact_id"].strip(),
        "surface": raw["surface"],
        "title": collapse(raw["title"]),
    }
    if isinstance(raw.get("source_uri"), str):
        artifact["source_uri"] = raw["source_uri"].strip()
    if isinstance(raw.get("word_count"), int):
        artifact["word_count"] = raw["word_count"]
    paths = raw.get("reviewed_paths")
    if isinstance(paths, list) and paths:
        artifact["reviewed_paths"] = sorted({path.strip() for path in paths if path.strip()})
    return artifact


def normalize_scanner_findings(rows: list) -> list[dict]:
    out: list[dict] = []
    for index, row in enumerate(rows):
        span = normalize_span(row.get("evidence_span"))
        if span is None:
            raise AdapterError(
                "empty_evidence_span",
                "a scanner finding carries an evidence span with no usable text",
                [
                    {
                        "pointer": f"/scanner_findings/{index}/evidence_span",
                        "keyword": "evidence",
                        "message": "span text is blank after whitespace collapsing",
                    }
                ],
            )
        entry = {
            "evidence_span": span,
            "rule": row["rule"],
            "scanner": row["scanner"],
        }
        if isinstance(row.get("message"), str) and row["message"].strip():
            entry["message"] = collapse(row["message"])
        out.append(entry)
    return sorted(
        out,
        key=lambda item: (
            item["scanner"],
            item["rule"],
            item["evidence_span"]["path"],
            item["evidence_span"]["start_line"],
            item["evidence_span"]["start_column"],
        ),
    )


def normalize_marker_hits(rows: list) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        marker_id = row["marker_id"]
        if marker_id in seen:
            raise AdapterError(
                "duplicate_marker_id",
                f"marker_id {marker_id!r} appears more than once",
                [
                    {
                        "pointer": f"/marker_hits/{index}/marker_id",
                        "keyword": "unique",
                        "message": "each marker class is recorded once per review",
                    }
                ],
            )
        seen.add(marker_id)
        entry = {
            "marker_class": collapse(row["marker_class"]),
            "marker_id": marker_id,
            "routes_to": row["routes_to"],
            "tier": row["tier"],
        }
        if isinstance(row.get("ledger_source_id"), str):
            entry["ledger_source_id"] = row["ledger_source_id"]
        if isinstance(row.get("observed"), str) and row["observed"].strip():
            entry["observed"] = collapse(row["observed"])
        if isinstance(row.get("occurrences"), int) and not isinstance(row.get("occurrences"), bool):
            entry["occurrences"] = row["occurrences"]
        span = normalize_span(row.get("evidence_span"))
        if span is not None:
            entry["evidence_span"] = span
        out.append(entry)
    return sorted(out, key=lambda item: (item["tier"], item["marker_id"]))


def normalize_procedure_results(rows: list, marker_ids: set[str]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        result_id = row["result_id"]
        if result_id in seen:
            raise AdapterError(
                "duplicate_result_id",
                f"result_id {result_id!r} appears more than once",
                [
                    {
                        "pointer": f"/procedure_results/{index}/result_id",
                        "keyword": "unique",
                        "message": "each procedure run is recorded once",
                    }
                ],
            )
        seen.add(result_id)
        routed_from = row.get("routed_from_marker_id")
        if isinstance(routed_from, str) and routed_from not in marker_ids:
            raise AdapterError(
                "dangling_marker_reference",
                f"procedure result {result_id!r} routes from unknown marker {routed_from!r}",
                [
                    {
                        "pointer": f"/procedure_results/{index}/routed_from_marker_id",
                        "keyword": "reference",
                        "message": "every routed_from_marker_id must appear in marker_hits",
                    }
                ],
            )
        entry = {
            "outcome": row["outcome"],
            "procedure": row["procedure"],
            "result_id": result_id,
        }
        if isinstance(row.get("artifact"), str) and row["artifact"].strip():
            entry["artifact"] = collapse(row["artifact"])
        if isinstance(routed_from, str):
            entry["routed_from_marker_id"] = routed_from
        span = normalize_span(row.get("evidence_span"))
        if span is not None:
            entry["evidence_span"] = span
        out.append(entry)
    return sorted(out, key=lambda item: (item["procedure"], item["result_id"]))


def build_envelope(document: dict, reference_date: str) -> dict:
    marker_hits = normalize_marker_hits(document.get("marker_hits", []))
    marker_ids = {hit["marker_id"] for hit in marker_hits}
    return {
        "artifact": normalize_artifact(document["artifact"]),
        "envelope_version": ENVELOPE_VERSION,
        "marker_hits": marker_hits,
        "note": ADAPTER_DISCLAIMER,
        "ok": True,
        "procedure_results": normalize_procedure_results(
            document.get("procedure_results", []), marker_ids
        ),
        "reference_date": reference_date,
        "review_id": document["review_id"],
        "scanner_findings": normalize_scanner_findings(document.get("scanner_findings", [])),
        "schema": SCHEMA,
        "tool": TOOL,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ingest_review_input.py",
        description="Validate and normalize a review input document into the canonical envelope.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the review input JSON, or - to read stdin.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date the review is anchored to. Overrides the value in the document.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    document = read_json_input(args.input, "review input")
    validate_or_refuse(document, SCHEMA, "review input")
    reference_date = parse_reference_date(args.reference_date, document.get("reference_date"))
    dump_json(build_envelope(document, reference_date), args.output)
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
