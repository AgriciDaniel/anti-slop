#!/usr/bin/env python3
"""Lane 1 synthesis: turn a review envelope into findings.

This is where the firewall from PLAN.md section 3 is actually enforced, so
the rules are stated here as standing constraints rather than as steps.

Rule 1. No authorship verdict, ever, in any form. This module emits no key
naming authorship, origin, or a probability that a model produced anything.
`schemas/findings.schema.json` sets `additionalProperties: false` at every
level, so a caller cannot add one either.

Rule 2. A marker never convicts. Only two things produce a finding: a
deterministic Layer 0 scanner, which decided something mechanically
checkable, or a Layer 1 structural procedure that was actually run and
returned `convicted`. A marker with no procedure result behind it leaves
this module as a routed procedure suggestion. Tier 2 and Tier 3 markers can
never leave it any other way, which is the rule the tests pin down.

Rule 3. Severity is impact and confidence is certainty. They are computed
by `severity_for` and `confidence_for`, which share no inputs beyond the
finding itself, and they are written to two separate required fields.

Rule 4. A finding with no evidence span is refused. It goes into
`refusals` with reason code `no_evidence_span` and never appears in
`findings`. Refusing loudly beats emitting an unfalsifiable claim.

The severity rubric

    HIGH    a fabricated fact, citation or API. An attribution procedure
            that convicted, a `scan_refs` finding, a `scan_packages`
            finding, and the residue tokens that are the visible remains of
            a citation the pipeline could not resolve.
    MEDIUM  padding or filler that changes nothing when cut. A deletion,
            inversion, stranger or load-bearing procedure that convicted,
            plus vendor residue and unfilled placeholders.
    LOW     a stylistic tell. A non-attribution procedure whose only
            routing evidence was a Tier 2 or Tier 3 marker. Tier 2 is a
            population level indicator and Tier 3 is folklore, so the
            impact claim that rests on it is weak even when the procedure
            convicted the span.

The confidence rubric

    high    the finding came from a deterministic scanner, or a procedure
            conviction whose span overlaps a scanner finding, so two
            independent mechanisms agree.
    medium  a procedure conviction that showed its work: the artifact text
            is present.
    low     a procedure conviction with no artifact recorded, or one whose
            only routing evidence is Tier 3 folklore.

`lint_voice` is deliberately absent from the finding path. It is a house
style rule and says so in its own output; a house style violation is not a
defect in the artifact under review, so it is recorded as a refusal with
reason code `house_style_is_not_a_defect`.

Determinism: findings are ordered by severity, then confidence, then span
position, then the finding id, which is a blake2b digest of the finding's
own content. Nothing reads the clock.

Usage:
    python3 scripts/ingest_review_input.py --input review.json --output envelope.json
    python3 scripts/synthesize_findings.py --envelope envelope.json --output findings.json

Exit codes: 0 no findings, 1 findings present, 2 refused input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapter_common import (  # noqa: E402
    ADAPTER_DISCLAIMER,
    CONFIDENCE_ORDER,
    ENVELOPE_VERSION,
    EXIT_CLEAN,
    EXIT_FINDINGS,
    PROCEDURES,
    SEVERITY_ORDER,
    AdapterError,
    add_output_argument,
    confidence_rank,
    dump_json,
    load_schema,
    normalize_span,
    parse_reference_date,
    read_json_input,
    run_adapter,
    severity_rank,
    spans_overlap,
    stable_id,
    validate_instance,
)

TOOL = "synthesize_findings"
SCHEMA = "findings.schema.json"

FIREWALL = [
    "This report names defects. It does not report origin and it carries no authorship field.",
    "A marker never convicts a span. Only a Layer 0 scanner or a Layer 1 procedure that returned convicted does.",
    "Severity is impact and confidence is certainty. They are separate fields and are never merged.",
    "A finding with no evidence span is refused rather than emitted.",
]

# Which structural procedure convicts each Layer 0 scanner, and what class of
# defect the scanner rule belongs to. lint_voice is absent on purpose: it is a
# house style rule, explicitly not a defect in the artifact under review.
SCANNER_ROUTING: dict[str, tuple[str, str]] = {
    "scan_refs": ("attribution", "fabricated_reference"),
    "scan_packages": ("attribution", "fabricated_package_or_api"),
    "scan_residue": ("deletion", "vendor_residue"),
    "scan_placeholders": ("stranger", "unfilled_placeholder"),
}

# Residue tokens that are the remains of a citation the pipeline could not
# resolve. The sentence carries an unresolved reference, so these are convicted
# by the attribution test and sit with the fabricated citation class rather than
# with ordinary vendor litter such as a tracking parameter.
CITATION_RESIDUE_RULES = frozenset(
    {
        "residue.oaicite",
        "residue.content_reference",
        "residue.gemini_cite",
        "residue.lenticular_citation",
        "residue.gemini_span",
        "residue.attached_file",
    }
)

PROCEDURE_DEFECT_KIND: dict[str, str] = {
    "attribution": "unsupported_attribution",
    "deletion": "padding",
    "inversion": "empty_claim",
    "stranger": "generic_filler",
    "load-bearing": "dead_scaffold",
}

PROCEDURE_SUMMARY: dict[str, str] = {
    "attribution": "The attribution test did not resolve this claim to a named source that supports it.",
    "deletion": "The deletion test cut this span and named no loss, so the span was padding.",
    "inversion": "The inversion test negated this claim and nobody would assert the negation, so the claim carries no information.",
    "stranger": "The stranger test found no fact here that required doing the work, so the span is generic.",
    "load-bearing": "The load-bearing test removed this and nothing broke or became unclear, so it was dead scaffolding.",
}

SCANNER_SUMMARY: dict[str, str] = {
    "scan_refs": "A reference in this span failed mechanical integrity checking.",
    "scan_packages": "A package or import in this span could not be confirmed to exist in its registry.",
    "scan_residue": "This span carries a vendor pipeline artifact that no author wrote.",
    "scan_placeholders": "This span carries unresolved template text, so the document promises content that is not there.",
}

TIER_ROUTING_REASON: dict[int, str] = {
    1: (
        "Tier 1 marker: corpus validated. It may point at a span and it may be counted "
        "in a density threshold, but it still cannot convict on its own. Run the "
        "procedure and report its artifact."
    ),
    2: (
        "Tier 2 marker: measured but high false positive, a population level indicator "
        "rather than a per document detector. It routes to a structural procedure and "
        "can never become a finding by itself."
    ),
    3: (
        "Tier 3 marker: folk wisdom, recorded and never acted on alone. It routes to a "
        "structural procedure only in a cluster, and can never become a finding by itself."
    ),
}


def routing_for_scanner(scanner: str, rule: str) -> tuple[str, str]:
    """Return the convicting procedure and the defect kind for a scanner rule."""
    if scanner == "scan_residue" and rule in CITATION_RESIDUE_RULES:
        return "attribution", "fabricated_citation"
    return SCANNER_ROUTING[scanner]


def severity_for(defect_kind: str, procedure: str, tier: int | None) -> tuple[str, str]:
    """Return the impact severity and the sentence that justifies it."""
    if defect_kind in {
        "fabricated_citation",
        "fabricated_reference",
        "fabricated_package_or_api",
        "unsupported_attribution",
    }:
        return "HIGH", (
            "HIGH because a fabricated fact, citation or API is the defect class that "
            "carries real downstream harm, regardless of which marker pointed at it."
        )
    if procedure != "attribution" and tier in (2, 3):
        return "LOW", (
            f"LOW because the only routing evidence was a Tier {tier} marker. Tier 2 is a "
            "population level indicator and Tier 3 is folklore, so this reads as a "
            "stylistic tell even though the procedure convicted the span."
        )
    return "MEDIUM", (
        "MEDIUM because the span changes nothing when it is cut. It is padding or filler, "
        "not a fabrication."
    )


def confidence_for(
    origin: str,
    has_artifact: bool,
    corroborated: list[str],
    tier: int | None,
) -> tuple[str, str]:
    """Return certainty that the finding is real, and the sentence that justifies it."""
    if origin == "layer0-scanner":
        return "high", (
            "high because a deterministic scanner decided this mechanically. There is no "
            "judgement in the decision to reproduce."
        )
    if corroborated:
        return "high", (
            "high because a deterministic scanner independently flagged an overlapping "
            f"span: {', '.join(corroborated)}."
        )
    if not has_artifact:
        return "low", (
            "low because the procedure returned convicted but recorded no artifact, so "
            "the work it did is not on the page and cannot be rechecked."
        )
    if tier == 3:
        return "low", (
            "low because the procedure showed its work but the only thing that routed it "
            "here was a Tier 3 folklore marker."
        )
    return "medium", (
        "medium because the procedure showed its work and the artifact is on the page, "
        "but no second mechanism corroborates it."
    )


def finding_sort_key(finding: dict) -> tuple:
    span = finding["evidence_span"]
    return (
        severity_rank(finding["severity"]),
        confidence_rank(finding["confidence"]),
        span["path"],
        span["start_line"],
        span["start_column"],
        finding["finding_id"],
    )


def build_scanner_findings(envelope: dict, refusals: list[dict]) -> list[dict]:
    findings: list[dict] = []
    for row in envelope.get("scanner_findings", []):
        scanner = row["scanner"]
        rule = row["rule"]
        if scanner not in SCANNER_ROUTING:
            refusals.append(
                {
                    "candidate": f"{scanner}:{rule}",
                    "reason_code": "house_style_is_not_a_defect",
                    "reason": (
                        "lint_voice enforces house style and says so in its own output. A "
                        "house style violation is not a defect in the artifact under review, "
                        "so it is recorded here and never promoted to a finding."
                    ),
                }
            )
            continue
        span = normalize_span(row.get("evidence_span"))
        if span is None:
            refusals.append(
                {
                    "candidate": f"{scanner}:{rule}",
                    "reason_code": "no_evidence_span",
                    "reason": (
                        "The scanner finding carried no usable evidence span, so there is "
                        "nothing a reader could check. Refused rather than emitted."
                    ),
                }
            )
            continue
        procedure, defect_kind = routing_for_scanner(scanner, rule)
        severity, why_severity = severity_for(defect_kind, procedure, None)
        confidence, why_confidence = confidence_for("layer0-scanner", True, [], None)
        finding = {
            "confidence": confidence,
            "defect_kind": defect_kind,
            "evidence_span": span,
            "finding_id": stable_id(
                "ASF",
                [envelope["review_id"], scanner, rule, span["path"], str(span["start_line"]), span["text"]],
            ),
            "origin": "layer0-scanner",
            "procedure": procedure,
            "rule": rule,
            "scanner": scanner,
            "severity": severity,
            "summary": row.get("message") or SCANNER_SUMMARY[scanner],
            "why_confidence": why_confidence,
            "why_severity": why_severity,
        }
        findings.append(finding)
    return findings


def build_procedure_findings(
    envelope: dict,
    scanner_spans: list[tuple[str, dict]],
    refusals: list[dict],
) -> tuple[list[dict], list[dict], set[str]]:
    findings: list[dict] = []
    survived: list[dict] = []
    consumed_markers: set[str] = set()
    markers = {hit["marker_id"]: hit for hit in envelope.get("marker_hits", [])}

    for row in envelope.get("procedure_results", []):
        result_id = row["result_id"]
        procedure = row["procedure"]
        marker_id = row.get("routed_from_marker_id")
        marker = markers.get(marker_id) if marker_id else None
        if marker_id:
            consumed_markers.add(marker_id)
        span = normalize_span(row.get("evidence_span"))
        artifact = row.get("artifact") or ""

        if row["outcome"] == "survived":
            entry = {
                "note": (
                    "The procedure was run and the span passed. A marker that routed to a "
                    "passing test is a false positive for this document, and saying so "
                    "costs nothing."
                ),
                "procedure": procedure,
                "result_id": result_id,
            }
            if artifact:
                entry["procedure_artifact"] = artifact
            if marker_id:
                entry["routed_from_marker_id"] = marker_id
            if span is not None:
                entry["evidence_span"] = span
            survived.append(entry)
            continue

        if span is None:
            refusals.append(
                {
                    "candidate": result_id,
                    "reason_code": "no_evidence_span",
                    "reason": (
                        f"The {procedure} procedure returned convicted but recorded no "
                        "evidence span. A finding a reader cannot locate in the text is not "
                        "a finding, so it is refused."
                    ),
                }
            )
            continue

        tier = marker["tier"] if marker else None
        defect_kind = PROCEDURE_DEFECT_KIND[procedure]
        corroborated = sorted(
            {rule for rule, other in scanner_spans if spans_overlap(span, other)}
        )
        severity, why_severity = severity_for(defect_kind, procedure, tier)
        confidence, why_confidence = confidence_for(
            "layer1-procedure", bool(artifact), corroborated, tier
        )
        finding = {
            "confidence": confidence,
            "defect_kind": defect_kind,
            "evidence_span": span,
            "finding_id": stable_id(
                "ASF",
                [envelope["review_id"], procedure, result_id, span["path"], str(span["start_line"]), span["text"]],
            ),
            "origin": "layer1-procedure",
            "procedure": procedure,
            "severity": severity,
            "summary": PROCEDURE_SUMMARY[procedure],
            "why_confidence": why_confidence,
            "why_severity": why_severity,
        }
        if artifact:
            finding["procedure_artifact"] = artifact
        if corroborated:
            finding["corroborated_by"] = corroborated
        if marker is not None:
            finding["routed_from_marker_id"] = marker["marker_id"]
            finding["routed_from_tier"] = marker["tier"]
            if marker.get("ledger_source_id"):
                finding["ledger_source_id"] = marker["ledger_source_id"]
        findings.append(finding)
    return findings, survived, consumed_markers


def build_routed_procedures(envelope: dict, consumed: set[str], refusals: list[dict]) -> list[dict]:
    routed: list[dict] = []
    for hit in envelope.get("marker_hits", []):
        if hit["marker_id"] in consumed:
            continue
        entry = {
            "marker_class": hit["marker_class"],
            "marker_id": hit["marker_id"],
            "reason": TIER_ROUTING_REASON[hit["tier"]],
            "suggested_procedure": hit["routes_to"],
            "tier": hit["tier"],
        }
        for key in ("ledger_source_id", "observed", "occurrences", "evidence_span"):
            if key in hit:
                entry[key] = hit[key]
        routed.append(entry)
        refusals.append(
            {
                "candidate": hit["marker_id"],
                "reason_code": "marker_alone_cannot_convict",
                "reason": (
                    f"Tier {hit['tier']} marker with no procedure result behind it. It is "
                    f"routed to the {hit['routes_to']} test as a suggestion and is not a finding."
                ),
            }
        )
    return sorted(routed, key=lambda item: (item["tier"], item["marker_id"]))


def synthesize(envelope: dict, reference_date: str) -> dict:
    refusals: list[dict] = []
    scanner_findings = build_scanner_findings(envelope, refusals)
    scanner_spans = [(item["rule"], item["evidence_span"]) for item in scanner_findings]
    procedure_findings, survived, consumed = build_procedure_findings(
        envelope, scanner_spans, refusals
    )
    routed = build_routed_procedures(envelope, consumed, refusals)

    findings = sorted(scanner_findings + procedure_findings, key=finding_sort_key)
    counts = {
        "by_confidence": {
            level: sum(1 for item in findings if item["confidence"] == level)
            for level in CONFIDENCE_ORDER
        },
        "by_procedure": {
            procedure: sum(1 for item in findings if item["procedure"] == procedure)
            for procedure in PROCEDURES
        },
        "by_severity": {
            level: sum(1 for item in findings if item["severity"] == level)
            for level in SEVERITY_ORDER
        },
        "total": len(findings),
    }
    return {
        "artifact": envelope["artifact"],
        "counts": counts,
        "envelope_version": ENVELOPE_VERSION,
        "findings": findings,
        "firewall": FIREWALL,
        "note": ADAPTER_DISCLAIMER,
        "ok": not findings,
        "reference_date": reference_date,
        "refusals": sorted(refusals, key=lambda item: (item["reason_code"], item["candidate"])),
        "review_id": envelope["review_id"],
        "routed_procedures": routed,
        "survived_procedures": sorted(survived, key=lambda item: (item["procedure"], item["result_id"])),
        "tool": TOOL,
    }


def require_envelope(envelope: dict) -> None:
    if envelope.get("tool") != "ingest_review_input" or envelope.get("ok") is not True:
        raise AdapterError(
            "not_a_review_envelope",
            "input is not an accepted ingest_review_input envelope",
            [
                {
                    "pointer": "/tool",
                    "keyword": "const",
                    "message": "run scripts/ingest_review_input.py first and feed its output here",
                }
            ],
        )
    for key in ("review_id", "artifact"):
        if key not in envelope:
            raise AdapterError(
                "not_a_review_envelope",
                f"envelope is missing {key}",
                [{"pointer": f"/{key}", "keyword": "required", "message": "is required and missing"}],
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="synthesize_findings.py",
        description="Turn a review envelope into severity and confidence separated findings.",
    )
    parser.add_argument(
        "--envelope",
        required=True,
        help="Path to the ingest_review_input envelope, or - to read stdin.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date the report is anchored to. Overrides the value in the envelope.",
    )
    add_output_argument(parser)
    args = parser.parse_args(argv)

    envelope = read_json_input(args.envelope, "review envelope")
    require_envelope(envelope)
    reference_date = parse_reference_date(args.reference_date, envelope.get("reference_date"))
    payload = synthesize(envelope, reference_date)

    schema = load_schema(SCHEMA)
    errors = validate_instance(payload, schema, schema)
    if errors:
        raise AdapterError(
            "self_check_failed",
            "the synthesized report does not satisfy findings.schema.json",
            errors,
        )
    dump_json(payload, args.output)
    return EXIT_FINDINGS if payload["findings"] else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(run_adapter(main, TOOL))
