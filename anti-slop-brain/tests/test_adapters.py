#!/usr/bin/env python3
"""Tests for the two Anti-Slop domain adapter lanes.

Plain script, no pytest, matching the convention in tests/test_pipeline.py
and tests/test_scanners.py.

Both lanes are exercised end to end, importer to synthesis to renderer, and
then the properties that actually matter are pinned:

- determinism: every stage is run twice and the bytes are compared
- malformed JSON produces a structured error envelope and a non-zero exit,
  never a traceback
- an invalid ISO date is rejected
- a URL that is not http or https is rejected
- a convicted procedure with no evidence span is refused, not emitted
- a Tier 2 marker on its own produces no finding, only a routed suggestion
- no output object anywhere contains an authorship verdict key

The last one is checked structurally rather than by eye. Every key of every
object in every JSON output is walked and matched against a banned key set,
because the firewall rule is about what a consumer can read a value out of,
not about what the prose says.

All writes go to a tempfile.TemporaryDirectory. No network access anywhere
in this file.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
FIXTURES = REPO / "tests" / "fixtures"
PY = sys.executable

REVIEW_INPUT = FIXTURES / "sample-review-input.json"
COHORT_A = FIXTURES / "sample-marker-cohort-a.json"
COHORT_B = FIXTURES / "sample-marker-cohort-b.json"

REFERENCE_DATE = "2026-07-28"

# Built from code points so that no forbidden character appears literally in
# this file. See CONTRIBUTING style rule and lint_voice.py.
EM = chr(0x2014)
EN = chr(0x2013)

# Firewall rule 1 is enforced on keys, not on prose. Any key that would let a
# consumer read an origin claim out of adapter output is banned outright.
BANNED_KEY_SUBSTRINGS = (
    "authorship",
    "verdict",
    "ai_generated",
    "aigenerated",
    "machine_written",
    "human_written",
    "llm_written",
    "ai_probability",
    "ai_score",
    "likely_author",
    "written_by",
)

FAILURES: list[str] = []
CHECKS = 0


def run(script: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(SCRIPTS / script), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )


def check(name: str, condition: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if condition:
        print(f"  pass: {name}")
    else:
        print(f"  FAIL: {name} {detail}")
        FAILURES.append(f"{name} {detail}".strip())


def expect_exit(name: str, proc: subprocess.CompletedProcess[str], code: int) -> None:
    check(
        name,
        proc.returncode == code,
        f"(exit {proc.returncode}, wanted {code})\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}",
    )


def write(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def banned_keys(value: object, trail: str = "") -> list[str]:
    """Walk a decoded JSON value and return every banned key path found."""
    offenders: list[str] = []
    if isinstance(value, dict):
        for key in sorted(value):
            flat = str(key).lower().replace("-", "_")
            if any(token in flat for token in BANNED_KEY_SUBSTRINGS):
                offenders.append(f"{trail}/{key}")
            offenders.extend(banned_keys(value[key], f"{trail}/{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            offenders.extend(banned_keys(item, f"{trail}/{index}"))
    return offenders


def error_envelope_of(proc: subprocess.CompletedProcess[str]) -> dict | None:
    """Decode a structured refusal, or return None when there is not one."""
    if not proc.stdout.strip():
        return None
    try:
        payload = json.loads(proc.stdout)
    except ValueError:
        return None
    return payload if isinstance(payload, dict) and payload.get("ok") is False else None


def check_structured_refusal(name: str, proc: subprocess.CompletedProcess[str], code: str) -> None:
    check(f"{name}: non-zero exit", proc.returncode != 0, f"(exit {proc.returncode})")
    check(
        f"{name}: no traceback",
        "Traceback (most recent call last)" not in proc.stderr,
        proc.stderr,
    )
    envelope = error_envelope_of(proc)
    check(f"{name}: emits a structured error envelope", envelope is not None, proc.stdout)
    if envelope is None:
        return
    check(
        f"{name}: reports error code {code}",
        envelope.get("error", {}).get("code") == code,
        json.dumps(envelope.get("error", {}), sort_keys=True),
    )
    check(
        f"{name}: refusal carries no authorship key",
        not banned_keys(envelope),
        str(banned_keys(envelope)),
    )


def review_lane(tmp: Path, tag: str) -> tuple[Path, Path, Path]:
    """Run the whole review lane into uniquely named files and return them."""
    envelope = tmp / f"review-envelope-{tag}.json"
    findings = tmp / f"findings-{tag}.json"
    report = tmp / f"findings-report-{tag}.md"
    ingest = run(
        "ingest_review_input.py",
        ["--input", str(REVIEW_INPUT), "--reference-date", REFERENCE_DATE, "--output", str(envelope)],
    )
    expect_exit(f"review lane {tag}: importer accepts the fixture", ingest, 0)
    synth = run(
        "synthesize_findings.py",
        ["--envelope", str(envelope), "--reference-date", REFERENCE_DATE, "--output", str(findings)],
    )
    expect_exit(f"review lane {tag}: synthesis reports findings with exit 1", synth, 1)
    render = run(
        "render_findings_report.py",
        ["--findings", str(findings), "--reference-date", REFERENCE_DATE, "--output", str(report)],
    )
    expect_exit(f"review lane {tag}: renderer succeeds", render, 0)
    return envelope, findings, report


def cohort_lane(tmp: Path, tag: str) -> tuple[Path, Path, Path]:
    """Run the whole cohort lane into uniquely named files and return them."""
    before = tmp / f"cohort-before-{tag}.json"
    after = tmp / f"cohort-after-{tag}.json"
    diff = tmp / f"cohort-diff-{tag}.json"
    report = tmp / f"cohort-report-{tag}.md"
    first = run("ingest_marker_cohort.py", ["--input", str(COHORT_A), "--output", str(before)])
    expect_exit(f"cohort lane {tag}: importer accepts snapshot A", first, 0)
    second = run("ingest_marker_cohort.py", ["--input", str(COHORT_B), "--output", str(after)])
    expect_exit(f"cohort lane {tag}: importer accepts snapshot B", second, 0)
    synth = run(
        "synthesize_cohort_diff.py",
        [
            "--before", str(before),
            "--after", str(after),
            "--reference-date", REFERENCE_DATE,
            "--output", str(diff),
        ],
    )
    expect_exit(f"cohort lane {tag}: diff reports drift with exit 1", synth, 1)
    render = run("render_cohort_report.py", ["--diff", str(diff), "--output", str(report)])
    expect_exit(f"cohort lane {tag}: renderer succeeds", render, 0)
    return after, diff, report


def test_review_lane_happy_path(tmp: Path) -> dict:
    print("review lane, happy path")
    _, findings_path, report_path = review_lane(tmp, "first")
    payload = json.loads(findings_path.read_text(encoding="utf-8"))

    check("emits at least one finding", payload["counts"]["total"] >= 1, str(payload["counts"]))
    check(
        "every finding carries a separate severity and confidence",
        all(
            item.get("severity") in {"HIGH", "MEDIUM", "LOW"}
            and item.get("confidence") in {"high", "medium", "low"}
            for item in payload["findings"]
        ),
        json.dumps([(i.get("severity"), i.get("confidence")) for i in payload["findings"]]),
    )
    check(
        "severity and confidence are never merged into one field",
        all(
            "severity_confidence" not in item and "score" not in item and "risk" not in item
            for item in payload["findings"]
        ),
        "a merged axis key appeared on a finding",
    )
    check(
        "every finding names a convicting structural procedure",
        all(
            item["procedure"] in {"deletion", "inversion", "stranger", "attribution", "load-bearing"}
            for item in payload["findings"]
        ),
        str([item.get("procedure") for item in payload["findings"]]),
    )
    check(
        "every finding carries a non-empty evidence span",
        all(item["evidence_span"]["text"].strip() for item in payload["findings"]),
        "an emitted finding had a blank evidence span",
    )

    severities = [item["severity"] for item in payload["findings"]]
    confidences = [item["confidence"] for item in payload["findings"]]
    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    confidence_rank = {"high": 0, "medium": 1, "low": 2}
    ordered = [
        (severity_rank[severity], confidence_rank[confidence])
        for severity, confidence in zip(severities, confidences)
    ]
    check("findings are ordered by severity then confidence", ordered == sorted(ordered), str(ordered))

    check(
        "a fabricated reference is HIGH severity",
        any(
            item["severity"] == "HIGH" and item["defect_kind"] == "fabricated_reference"
            for item in payload["findings"]
        ),
        json.dumps([(i["severity"], i["defect_kind"]) for i in payload["findings"]]),
    )
    check(
        "a hallucinated package is HIGH severity",
        any(
            item["severity"] == "HIGH" and item["defect_kind"] == "fabricated_package_or_api"
            for item in payload["findings"]
        ),
        json.dumps([(i["severity"], i["defect_kind"]) for i in payload["findings"]]),
    )
    check(
        "a deletion test conviction is MEDIUM severity padding",
        any(
            item["severity"] == "MEDIUM"
            and item["procedure"] == "deletion"
            and item["defect_kind"] == "padding"
            for item in payload["findings"]
        ),
        json.dumps([(i["severity"], i["procedure"], i["defect_kind"]) for i in payload["findings"]]),
    )
    check(
        "a conviction routed only from a weak tier is LOW severity",
        any(
            item["severity"] == "LOW" and item.get("routed_from_tier") in (2, 3)
            for item in payload["findings"]
        ),
        json.dumps([(i["severity"], i.get("routed_from_tier")) for i in payload["findings"]]),
    )
    check(
        "house style from lint_voice never becomes a finding",
        all(item.get("scanner") != "lint_voice" for item in payload["findings"])
        and any(
            item["reason_code"] == "house_style_is_not_a_defect" for item in payload["refusals"]
        ),
        json.dumps(payload["refusals"], sort_keys=True),
    )
    check(
        "a procedure that passed is recorded rather than dropped",
        any(item["procedure"] == "load-bearing" for item in payload["survived_procedures"]),
        json.dumps(payload["survived_procedures"], sort_keys=True),
    )

    report = report_path.read_text(encoding="utf-8")
    for fragment in (
        "# Anti-Slop findings",
        "## Severity by confidence",
        "## Findings",
        "## Routed procedures",
        "## Refusals",
        "does not judge authorship",
    ):
        check(f"report contains {fragment!r}", fragment in report, report[:400])
    check("report states the reference date", REFERENCE_DATE in report, report[:400])
    return payload


def test_cohort_lane_happy_path(tmp: Path) -> dict:
    print("cohort lane, happy path")
    _, diff_path, report_path = cohort_lane(tmp, "first")
    payload = json.loads(diff_path.read_text(encoding="utf-8"))
    counts = payload["counts"]

    check("counts the days between snapshots", counts["days_between_snapshots"] == 103, str(counts))
    check(
        "detects the two added markers",
        sorted(item["marker_id"] for item in payload["added"])
        == ["hallucinated-package-import", "negative-parallelism"],
        json.dumps(payload["added"], sort_keys=True),
    )
    check(
        "detects the removed marker",
        [item["marker_id"] for item in payload["removed"]] == ["uniform-paragraph-length"],
        json.dumps(payload["removed"], sort_keys=True),
    )
    changes = {item["marker_id"]: item for item in payload["tier_changed"]}
    check(
        "detects the em dash demotion from Tier 1 to Tier 2",
        changes.get("em-dash-density", {}).get("direction") == "demoted"
        and changes["em-dash-density"]["from_tier"] == 1
        and changes["em-dash-density"]["to_tier"] == 2,
        json.dumps(payload["tier_changed"], sort_keys=True),
    )
    check(
        "detects the sycophancy promotion from Tier 3 to Tier 2",
        changes.get("sycophantic-verbal-tics", {}).get("direction") == "promoted",
        json.dumps(payload["tier_changed"], sort_keys=True),
    )
    check(
        "detects the rerouted marker",
        [item["marker_id"] for item in payload["routing_changed"]] == ["tricolon-density"],
        json.dumps(payload["routing_changed"], sort_keys=True),
    )
    stale = {item["marker_id"]: item for item in payload["stale_evidence"]}
    check(
        "flags both markers whose source refresh_due has passed",
        sorted(stale) == ["single-ai-vocabulary-word", "sycophantic-verbal-tics"],
        json.dumps(payload["stale_evidence"], sort_keys=True),
    )
    check(
        "computes days overdue against the reference date",
        stale.get("single-ai-vocabulary-word", {}).get("days_overdue") == 75
        and stale.get("sycophantic-verbal-tics", {}).get("days_overdue") == 13,
        json.dumps(payload["stale_evidence"], sort_keys=True),
    )
    check(
        "a marker inside its refresh window is not flagged",
        "excess-vocabulary-density" not in stale,
        json.dumps(sorted(stale), sort_keys=True),
    )

    report = report_path.read_text(encoding="utf-8")
    for fragment in (
        "# Anti-Slop marker cohort refresh",
        "## Stale evidence",
        "## Tier changes",
        "## Routing changes",
        "does not judge authorship",
    ):
        check(f"cohort report contains {fragment!r}", fragment in report, report[:400])
    return payload


def test_determinism(tmp: Path) -> None:
    print("determinism")
    envelope_a, findings_a, report_a = review_lane(tmp, "det1")
    envelope_b, findings_b, report_b = review_lane(tmp, "det2")
    check(
        "review importer is byte identical across runs",
        envelope_a.read_bytes() == envelope_b.read_bytes(),
        "review envelope bytes differ between two runs",
    )
    check(
        "review synthesis is byte identical across runs",
        findings_a.read_bytes() == findings_b.read_bytes(),
        "findings bytes differ between two runs",
    )
    check(
        "review report is byte identical across runs",
        report_a.read_bytes() == report_b.read_bytes(),
        "report bytes differ between two runs",
    )

    after_a, diff_a, cohort_report_a = cohort_lane(tmp, "det1")
    after_b, diff_b, cohort_report_b = cohort_lane(tmp, "det2")
    check(
        "cohort importer is byte identical across runs",
        after_a.read_bytes() == after_b.read_bytes(),
        "cohort envelope bytes differ between two runs",
    )
    check(
        "cohort diff is byte identical across runs",
        diff_a.read_bytes() == diff_b.read_bytes(),
        "cohort diff bytes differ between two runs",
    )
    check(
        "cohort report is byte identical across runs",
        cohort_report_a.read_bytes() == cohort_report_b.read_bytes(),
        "cohort report bytes differ between two runs",
    )


def test_malformed_json(tmp: Path) -> None:
    print("malformed input")
    broken = write(tmp, "broken.json", '{"schema_version": 1, "review_id": "oops",\n')
    proc = run("ingest_review_input.py", ["--input", str(broken)])
    check_structured_refusal("malformed review JSON", proc, "invalid_json")

    broken_cohort = write(tmp, "broken-cohort.json", "[1, 2, 3]")
    cohort_proc = run("ingest_marker_cohort.py", ["--input", str(broken_cohort)])
    check_structured_refusal("malformed cohort JSON", cohort_proc, "invalid_json")

    missing = run("ingest_review_input.py", ["--input", str(tmp / "does-not-exist.json")])
    check_structured_refusal("missing input file", missing, "missing_input")

    document = json.loads(REVIEW_INPUT.read_text(encoding="utf-8"))
    del document["artifact"]
    incomplete = write(tmp, "no-artifact.json", json.dumps(document, indent=2))
    schema_proc = run("ingest_review_input.py", ["--input", str(incomplete)])
    check_structured_refusal("review input missing a required object", schema_proc, "schema_violation")


def test_invalid_iso_date(tmp: Path) -> None:
    print("invalid ISO date")
    document = json.loads(REVIEW_INPUT.read_text(encoding="utf-8"))
    document["reference_date"] = "2026-02-30"
    impossible = write(tmp, "impossible-date.json", json.dumps(document, indent=2))
    proc = run("ingest_review_input.py", ["--input", str(impossible)])
    check_structured_refusal("impossible calendar date in the document", proc, "schema_violation")

    flag = run(
        "ingest_review_input.py",
        ["--input", str(REVIEW_INPUT), "--reference-date", "28-07-2026"],
    )
    check_structured_refusal("non ISO reference date on the flag", flag, "invalid_reference_date")

    cohort = json.loads(COHORT_B.read_text(encoding="utf-8"))
    cohort["markers"][0]["source_refresh_due"] = "2026-13-01"
    bad_refresh = write(tmp, "bad-refresh.json", json.dumps(cohort, indent=2))
    refresh_proc = run("ingest_marker_cohort.py", ["--input", str(bad_refresh)])
    check_structured_refusal("impossible refresh_due month", refresh_proc, "schema_violation")

    diff_proc = run(
        "synthesize_cohort_diff.py",
        [
            "--before", str(tmp / "cohort-before-first.json"),
            "--after", str(tmp / "cohort-after-first.json"),
            "--reference-date", "not-a-date",
        ],
    )
    check_structured_refusal("non ISO reference date on the diff", diff_proc, "invalid_reference_date")


def test_non_http_url(tmp: Path) -> None:
    print("non-http URL")
    document = json.loads(REVIEW_INPUT.read_text(encoding="utf-8"))
    document["artifact"]["source_uri"] = "file:///etc/passwd"
    file_scheme = write(tmp, "file-scheme.json", json.dumps(document, indent=2))
    proc = run("ingest_review_input.py", ["--input", str(file_scheme)])
    check_structured_refusal("file scheme source_uri", proc, "schema_violation")

    document["artifact"]["source_uri"] = "javascript:alert(1)"
    script_scheme = write(tmp, "script-scheme.json", json.dumps(document, indent=2))
    script_proc = run("ingest_review_input.py", ["--input", str(script_scheme)])
    check_structured_refusal("javascript scheme source_uri", script_proc, "schema_violation")

    cohort = json.loads(COHORT_B.read_text(encoding="utf-8"))
    cohort["markers"][0]["source_url"] = "ftp://example.invalid/paper.pdf"
    ftp = write(tmp, "ftp-source.json", json.dumps(cohort, indent=2))
    ftp_proc = run("ingest_marker_cohort.py", ["--input", str(ftp)])
    check_structured_refusal("ftp scheme marker source_url", ftp_proc, "schema_violation")


def test_refuses_finding_without_evidence_span(payload: dict) -> None:
    print("refusal: a finding with no evidence span")
    refused = {
        item["candidate"] for item in payload["refusals"] if item["reason_code"] == "no_evidence_span"
    }
    check(
        "the spanless conviction is refused",
        "proc-deletion-unlocated-claim" in refused,
        json.dumps(payload["refusals"], sort_keys=True),
    )
    check(
        "the spanless conviction never reaches findings",
        all(
            "proc-deletion-unlocated-claim" not in json.dumps(item, sort_keys=True)
            for item in payload["findings"]
        ),
        "a refused candidate appeared in findings",
    )
    check(
        "no emitted finding has an empty evidence span",
        all(item["evidence_span"]["text"].strip() for item in payload["findings"]),
        "an emitted finding had a blank evidence span",
    )


def test_weak_tier_marker_alone_produces_no_finding(payload: dict) -> None:
    print("firewall: a Tier 2 marker alone cannot convict")
    routed = {item["marker_id"]: item for item in payload["routed_procedures"]}
    check(
        "the lone Tier 2 marker is routed rather than emitted",
        routed.get("sycophantic-verbal-tics", {}).get("tier") == 2,
        json.dumps(payload["routed_procedures"], sort_keys=True),
    )
    check(
        "the lone Tier 2 marker names a suggested procedure",
        routed.get("sycophantic-verbal-tics", {}).get("suggested_procedure") == "deletion",
        json.dumps(payload["routed_procedures"], sort_keys=True),
    )
    for marker_id in ("sycophantic-verbal-tics", "em-dash-density"):
        check(
            f"no finding is attributed to the lone Tier 2 marker {marker_id}",
            all(item.get("routed_from_marker_id") != marker_id for item in payload["findings"]),
            json.dumps([item.get("routed_from_marker_id") for item in payload["findings"]]),
        )
    check(
        "every routed marker is also recorded as a refusal",
        {item["marker_id"] for item in payload["routed_procedures"]}
        <= {
            item["candidate"]
            for item in payload["refusals"]
            if item["reason_code"] == "marker_alone_cannot_convict"
        },
        json.dumps(payload["refusals"], sort_keys=True),
    )
    check(
        "no Tier 2 or Tier 3 marker appears as a scanner style hard failure",
        all(item["tier"] in (1, 2, 3) for item in payload["routed_procedures"]),
        json.dumps(payload["routed_procedures"], sort_keys=True),
    )


def test_no_authorship_key_anywhere(tmp: Path, payloads: list[dict]) -> None:
    print("firewall: no authorship key in any output object")
    for payload in payloads:
        offenders = banned_keys(payload)
        check(
            f"{payload['tool']} output carries no authorship key",
            not offenders,
            str(offenders),
        )
    envelope_path = tmp / "review-envelope-first.json"
    cohort_path = tmp / "cohort-after-first.json"
    for path in (envelope_path, cohort_path):
        data = json.loads(path.read_text(encoding="utf-8"))
        offenders = banned_keys(data)
        check(f"{path.name} carries no authorship key", not offenders, str(offenders))
    for path in sorted(SCHEMA_FILES):
        data = json.loads(path.read_text(encoding="utf-8"))
        offenders = [
            item
            for item in banned_keys(data)
            if not item.endswith("/description") and not item.endswith("/title")
        ]
        check(f"{path.name} declares no authorship property", not offenders, str(offenders))


SCHEMA_FILES = sorted((REPO / "schemas").glob("*.schema.json"))


def forged_envelope(**overrides: object) -> dict:
    """A hand written envelope that never passed through the importer."""
    envelope: dict = {
        "artifact": {
            "artifact_id": "drafts/forged.md",
            "surface": "prose",
            "title": "An envelope written by hand",
        },
        "envelope_version": 1,
        "marker_hits": [],
        "note": "hand written, not produced by ingest_review_input.py",
        "ok": True,
        "procedure_results": [
            {
                "artifact": "cut the span and named no loss",
                "evidence_span": {
                    "end_column": 40,
                    "end_line": 5,
                    "path": "drafts/forged.md",
                    "start_column": 1,
                    "start_line": 5,
                    "text": "Great question, and an important one to raise.",
                },
                "outcome": "convicted",
                "procedure": "deletion",
                "result_id": "proc-deletion-laundered",
                "routed_from_marker_id": "sycophantic-verbal-tics",
            }
        ],
        "reference_date": REFERENCE_DATE,
        "review_id": "forged-review",
        "scanner_findings": [],
        "schema": "review-input.schema.json",
        "tool": "ingest_review_input",
    }
    envelope.update(overrides)
    return envelope


def test_forged_envelope_is_refused(tmp: Path) -> None:
    """Regression: the firewall could be bypassed with a hand written envelope.

    `require_envelope` checked only that tool was ingest_review_input and ok was
    true. It never validated the envelope, so every guarantee the importer
    provides was optional for anyone willing to skip it.

    The concrete laundering path: the importer refuses a routed_from_marker_id
    that is absent from marker_hits with dangling_marker_reference. Skip the
    importer and the marker resolves to None, the tier resolves to None, and
    severity_for only downgraded to LOW when the tier was 2 or 3. A Tier 3
    folklore marker therefore came out the far side as a MEDIUM finding with no
    tier recorded anywhere in the report.
    """
    print("firewall: a forged envelope is refused")

    laundering = write(tmp, "forged-dangling.json", json.dumps(forged_envelope(), indent=2))
    proc = run("synthesize_findings.py", ["--envelope", str(laundering)])
    check_structured_refusal("forged envelope with a dangling marker route", proc, "dangling_marker_reference")
    check(
        "the forged envelope produces no findings document",
        '"findings"' not in proc.stdout,
        proc.stdout[:400],
    )

    malformed = write(
        tmp,
        "forged-malformed.json",
        json.dumps(forged_envelope(artifact={"artifact_id": "x", "surface": "telepathy", "title": "t"}), indent=2),
    )
    malformed_proc = run("synthesize_findings.py", ["--envelope", str(malformed)])
    check_structured_refusal("forged envelope that violates the schema", malformed_proc, "schema_violation")

    undeclared = write(
        tmp,
        "forged-undeclared.json",
        json.dumps(forged_envelope(marker_hits=[{"marker_id": "made-up", "tier": 9}]), indent=2),
    )
    undeclared_proc = run("synthesize_findings.py", ["--envelope", str(undeclared)])
    check_structured_refusal("forged envelope with an out of range tier", undeclared_proc, "schema_violation")

    duplicates = forged_envelope()
    duplicates["procedure_results"] = [
        {**duplicates["procedure_results"][0], "routed_from_marker_id": None},
        {**duplicates["procedure_results"][0], "routed_from_marker_id": None},
    ]
    for row in duplicates["procedure_results"]:
        del row["routed_from_marker_id"]
    duplicate_path = write(tmp, "forged-duplicate.json", json.dumps(duplicates, indent=2))
    duplicate_proc = run("synthesize_findings.py", ["--envelope", str(duplicate_path)])
    check_structured_refusal("forged envelope with a duplicate result id", duplicate_proc, "duplicate_result_id")

    # Defence in depth. Even if a routed marker ever reached severity_for with
    # no resolvable tier, it must fail closed rather than default to MEDIUM.
    probe = subprocess.run(
        [
            PY,
            "-c",
            "import sys; sys.path.insert(0, 'scripts'); import synthesize_findings as s; "
            "print(s.severity_for('padding', 'deletion', None, routed_marker_unresolved=True)[0]); "
            "print(s.severity_for('padding', 'deletion', None)[0])",
        ],
        cwd=REPO,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )
    lines = probe.stdout.split()
    check(
        "an unresolvable routed marker fails closed to LOW severity",
        lines[:1] == ["LOW"],
        probe.stdout + probe.stderr,
    )
    check(
        "a procedure with no routing claim at all is still MEDIUM",
        lines[1:2] == ["MEDIUM"],
        probe.stdout + probe.stderr,
    )

    # The importer still refuses the same document, and the honest envelope it
    # produces still works, so the fix did not simply block the whole lane.
    envelope = tmp / "review-envelope-first.json"
    good = run("synthesize_findings.py", ["--envelope", str(envelope), "--reference-date", REFERENCE_DATE])
    expect_exit("a real importer envelope is still accepted", good, 1)


def test_refresh_due_warning_band(tmp: Path) -> None:
    """Regression: a shared refresh_due date was a cliff with no warning band.

    Fourteen ledger sources carry refresh_due 2026-08-26 and a past refresh_due
    was a CRITICAL failure, so on 2026-08-27 the brain fell from market-ready to
    scaffolded and the market-ready release gate hard-failed, with no code
    change and no notice. A date that is a plan needs a band, and the band needs
    to be printed before it matters rather than after.
    """
    print("audit: the refresh_due warning band")

    today_run = run("audit_brain.py", ["--json"])
    expect_exit("the audit still passes today", today_run, 0)
    today_payload = json.loads(today_run.stdout)
    window = today_payload.get("refresh_window", {})
    check(
        "every audit run reports the earliest refresh_due date",
        isinstance(window.get("earliest_refresh_due"), str),
        json.dumps(window, sort_keys=True),
    )
    check(
        "every audit run reports how many sources share it",
        isinstance(window.get("earliest_refresh_due_count"), int)
        and window["earliest_refresh_due_count"] >= 1,
        json.dumps(window, sort_keys=True),
    )
    text_run = run("audit_brain.py", [])
    check(
        "the text report prints the refresh window on every run",
        "Refresh window:" in text_run.stdout
        and str(window.get("earliest_refresh_due")) in text_run.stdout,
        text_run.stdout[:600],
    )

    day_after = run("audit_brain.py", ["--json", "--reference-date", "2026-08-27"])
    expect_exit("the day after the shared refresh_due is not a failure", day_after, 0)
    payload = json.loads(day_after.stdout)
    check(
        "the brain does not drop off the cliff on 2026-08-27",
        payload["status"] == "market-ready" and payload["score"] >= 90,
        f"{payload['status']} {payload['score']}",
    )
    check(
        "no refresh_due critical is raised inside the warning band",
        not [item for item in payload["critical_failures"] if "refresh_due" in item],
        json.dumps(payload["critical_failures"], sort_keys=True),
    )
    check(
        "the warning band is counted",
        payload["refresh_window"]["recently_overdue"] >= 14,
        json.dumps(payload["refresh_window"], sort_keys=True),
    )
    check(
        "the warning band is reported prominently as a warning",
        any("Refresh window" in item for item in payload["warnings"]),
        json.dumps(payload["warnings"], sort_keys=True),
    )

    gate = run("audit_brain.py", ["--require", "market-ready", "--reference-date", "2026-08-27"])
    expect_exit("the market-ready gate still passes inside the warning band", gate, 0)

    approaching = run("audit_brain.py", ["--json", "--reference-date", "2026-08-20"])
    approaching_payload = json.loads(approaching.stdout)
    check(
        "a source inside the window before its date is warned about, not failed",
        approaching_payload["refresh_window"]["due_soon"] >= 14
        and approaching_payload["status"] == "market-ready",
        json.dumps(approaching_payload["refresh_window"], sort_keys=True),
    )

    past_band = run("audit_brain.py", ["--json", "--reference-date", "2026-09-30"])
    expect_exit("past the warning band the audit fails", past_band, 1)
    past_payload = json.loads(past_band.stdout)
    check(
        "past the warning band a stale refresh_due is critical again",
        [item for item in past_payload["critical_failures"] if "refresh_due is stale" in item],
        json.dumps(past_payload["critical_failures"], sort_keys=True),
    )
    check(
        "past the warning band the overdue sources are counted as critical",
        past_payload["refresh_window"]["critically_overdue"] >= 14,
        json.dumps(past_payload["refresh_window"], sort_keys=True),
    )

    bad_date = run("audit_brain.py", ["--reference-date", "27-08-2026"])
    expect_exit("a non ISO reference date is a usage error", bad_date, 2)


def test_no_forbidden_characters() -> None:
    print("house style of the adapters themselves")
    offenders: list[str] = []
    targets = (
        [SCRIPTS / "adapter_common.py"]
        + sorted(SCRIPTS.glob("ingest_*.py"))
        + sorted(SCRIPTS.glob("synthesize_*.py"))
        + sorted(SCRIPTS.glob("render_*.py"))
        + SCHEMA_FILES
        + [REVIEW_INPUT, COHORT_A, COHORT_B, Path(__file__)]
    )
    for path in targets:
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if EM in line or EN in line:
                offenders.append(f"{path.name}:{number}")
    check("adapter sources contain no long dash characters", not offenders, str(offenders))


def test_manifest_is_domain_adapted() -> None:
    print("adapter manifest")
    manifest = json.loads((REPO / "references" / "adapter-manifest.json").read_text(encoding="utf-8"))
    check(
        "generic_only is the boolean false",
        manifest.get("generic_only") is False,
        repr(manifest.get("generic_only")),
    )
    sections = ("input_schemas", "importers", "synthesis_modules", "report_renderers", "fixtures", "tests")
    for section in sections:
        entries = manifest.get(section)
        check(f"{section} is a non-empty array", isinstance(entries, list) and bool(entries), repr(entries))
        if not isinstance(entries, list):
            continue
        for entry in entries:
            path = entry.get("path") if isinstance(entry, dict) else None
            check(
                f"{section} entry {path!r} resolves on disk",
                isinstance(path, str) and (REPO / path).exists(),
                repr(entry),
            )
            check(
                f"{section} entry {path!r} is marked implemented",
                isinstance(entry, dict)
                and entry.get("status") == "implemented"
                and entry.get("planned") is False,
                repr(entry),
            )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="anti-slop-adapters-") as raw:
        tmp = Path(raw)
        findings = test_review_lane_happy_path(tmp)
        diff = test_cohort_lane_happy_path(tmp)
        test_determinism(tmp)
        test_malformed_json(tmp)
        test_invalid_iso_date(tmp)
        test_non_http_url(tmp)
        test_refuses_finding_without_evidence_span(findings)
        test_weak_tier_marker_alone_produces_no_finding(findings)
        test_forged_envelope_is_refused(tmp)
        test_refresh_due_warning_band(tmp)
        test_no_authorship_key_anywhere(tmp, [findings, diff])
        test_no_forbidden_characters()
        test_manifest_is_domain_adapted()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} of {CHECKS} checks")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print(f"Adapter tests passed: {CHECKS} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
