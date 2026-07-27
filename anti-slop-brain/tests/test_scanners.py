#!/usr/bin/env python3
"""Tests for the Layer 0 deterministic scanners.

Plain script, no pytest, matching the convention in tests/test_pipeline.py.
Every scanner gets at least two tests: one proving it fires on a genuine
mechanical defect, and one proving it stays silent on the legitimate
lookalike. The second kind matters more. A scanner that cannot tell a
document discussing a residue marker from a document carrying one is a
scanner nobody will keep running.

No network access anywhere in this file. Online modes are exercised only
by their argument handling, never by calling out.
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
PY = sys.executable

# Built from code points so that no forbidden character appears literally in
# this file. See CONTRIBUTING style rule and lint_voice.py.
EM = chr(0x2014)
EN = chr(0x2013)
LENTICULAR_OPEN = chr(0x3010)
LENTICULAR_CLOSE = chr(0x3011)
DAGGER = chr(0x2020)

FAILURES: list[str] = []
CHECKS = 0
SKIPS: list[str] = []


def run(script: str, args: list[str], stdin_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(SCRIPTS / script), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        input=stdin_text,
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


def rules_in(proc: subprocess.CompletedProcess[str]) -> set[str]:
    payload = json.loads(proc.stdout)
    return {finding["rule"] for finding in payload["findings"]}


def write(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_scan_residue(tmp: Path) -> None:
    print("scan_residue")
    dirty = write(
        tmp,
        "residue-dirty.md",
        "# Draft\n\n"
        "The result was decisive :contentReference[oaicite:0]{index=0} in that trial.\n"
        "A second claim followed [cite: 3, 12] and a third one too.\n"
        f"The bracket form {LENTICULAR_OPEN}85{DAGGER}L261-269{LENTICULAR_CLOSE} was left in place.\n"
        "Span markers survived here [span_1](start_span) and here [span_1](end_span).\n"
        '<grok-card data-id="abc" data-type="citation_card"></grok-card>\n'
        ':::writing{variant="document" id="28471"}\n'
        "Perplexity kept the attachment pointer [attached_file:1] in the sentence.\n"
        "See https://www.nature.com/articles/xyz?utm_source=chatgpt.com for the study.\n"
        "Also https://example-news.test/page?referrer=grok.com was cited.\n",
    )
    dirty_run = run("scan_residue.py", [str(dirty), "--format", "json"])
    expect_exit("fires on a document carrying residue", dirty_run, 1)
    found = rules_in(dirty_run)
    for rule in (
        "residue.oaicite",
        "residue.content_reference",
        "residue.gemini_cite",
        "residue.lenticular_citation",
        "residue.gemini_span",
        "residue.grok_card",
        "residue.writing_block",
        "residue.attached_file",
        "residue.utm_source",
        "residue.referrer",
    ):
        check(f"detects {rule}", rule in found, f"(found {sorted(found)})")

    clean = write(
        tmp,
        "residue-clean.md",
        "# How residue markers look\n\n"
        "ChatGPT sometimes leaves an `oaicite` token behind. Gemini leaves a\n"
        "`[cite: 1]` marker. Neither belongs in a published draft.\n\n"
        "```text\n"
        ":contentReference[oaicite:0]{index=0}\n"
        "[cite: 3, 12, 13]\n"
        "[span_1](start_span)\n"
        f"{LENTICULAR_OPEN}85{DAGGER}L261-269{LENTICULAR_CLOSE}\n"
        ':::writing{variant="document" id="28471"}\n'
        "[attached_file:1]\n"
        "```\n\n"
        "The taxonomy above comes from the Wikipedia signs-of-AI-writing page.\n",
    )
    clean_run = run("scan_residue.py", [str(clean), "--format", "json"])
    expect_exit("stays silent on a document that only discusses residue", clean_run, 0)

    fenced_url = write(
        tmp,
        "residue-fenced-url.md",
        "# Citation block\n\n"
        "```\n"
        "https://www.nature.com/articles/xyz?utm_source=chatgpt.com\n"
        "```\n",
    )
    fenced_run = run("scan_residue.py", [str(fenced_url), "--format", "json"])
    expect_exit("still fires on a tracking parameter inside a fenced URL", fenced_run, 1)

    stdin_run = run("scan_residue.py", [], stdin_text="A line with oaicite in it.\n")
    expect_exit("reads stdin", stdin_run, 1)

    missing_run = run("scan_residue.py", [str(tmp / "does-not-exist.md")])
    expect_exit("returns exit 2 for a missing path", missing_run, 2)


def test_scan_placeholders(tmp: Path) -> None:
    print("scan_placeholders")
    dirty = write(
        tmp,
        "placeholders-dirty.md",
        "# Report\n\n"
        "Prepared by [Your Name] for the committee.\n"
        "Source: |url=INSERT_SOURCE_URL_30 |publisher=SOURCE_PUBLISHER\n"
        "access-date=20XX-04-11\n"
        "date: YYYY-MM-DD\n"
        "TODO: quote the minister here.\n"
        "The witness said something notable [quote needed].\n"
        "Insert placeholder quote from the transcript.\n"
        "Lorem ipsum dolor sit amet.\n"
        "Set the header to <your api key> before running.\n"
        "url: https://TBD/report\n",
    )
    dirty_run = run("scan_placeholders.py", [str(dirty), "--format", "json"])
    expect_exit("fires on unresolved template text", dirty_run, 1)
    found = rules_in(dirty_run)
    for rule in (
        "placeholder.your_field",
        "placeholder.insert_token",
        "placeholder.date_field_x",
        "placeholder.date_field_yyyy",
        "placeholder.todo_quote",
        "placeholder.quote_needed",
        "placeholder.placeholder_quote",
        "placeholder.lorem_ipsum",
        "placeholder.your_tag",
        "placeholder.url_tbd",
    ):
        check(f"detects {rule}", rule in found, f"(found {sorted(found)})")

    clean = write(
        tmp,
        "placeholders-clean.md",
        "---\n"
        "type: note\n"
        "date: 2026-07-27\n"
        "access-date: 2026-07-27\n"
        "---\n\n"
        "# Style guide for dates\n\n"
        "Every date field uses the ISO 8601 form, written YYYY-MM-DD, so that\n"
        "sorting works. A date such as 2026-07-27 is valid; a bare year is not.\n\n"
        "Fill the template below before publishing:\n\n"
        "```markdown\n"
        "Prepared by [Your Name]\n"
        "|url=INSERT_SOURCE_URL_30\n"
        "access-date=20XX\n"
        "```\n\n"
        "The [style manual](https://example-styleguide.test/manual) has the rest.\n",
    )
    clean_run = run("scan_placeholders.py", [str(clean), "--format", "json"])
    expect_exit(
        "stays silent when YYYY-MM-DD is prose and placeholders are in a fence",
        clean_run,
        0,
    )


def test_scan_refs(tmp: Path) -> None:
    print("scan_refs")
    dirty = write(
        tmp,
        "refs-dirty.md",
        "# References\n\n"
        "1. A study, doi:10.0000/xxxx, reported the effect.\n"
        "2. Another, DOI 10.1234/EXAMPLE-PLACEHOLDER, did not.\n"
        "3. A preprint, arXiv:2812.09999, is dated in the future.\n"
        "4. A book, ISBN 978-0-13-235088-5, fails its checksum.\n"
        "5. A second book, ISBN 0-13-235088-9, fails ISBN-10.\n"
        "6. Homepage: https://example.com/paper and https://127.0.0.1:8080/draft\n",
    )
    dirty_run = run("scan_refs.py", [str(dirty), "--format", "json"])
    expect_exit("fires on defective references", dirty_run, 1)
    found = rules_in(dirty_run)
    for rule in (
        "refs.doi_placeholder",
        "refs.arxiv_future",
        "refs.isbn_checksum",
        "refs.url_placeholder_host",
    ):
        check(f"detects {rule}", rule in found, f"(found {sorted(found)})")

    clean = write(
        tmp,
        "refs-clean.md",
        "# References\n\n"
        "1. Kobak et al., Science Advances 11(27), 2025-07-02. "
        "https://doi.org/10.1126/sciadv.adt3813\n"
        "2. Shaib, Chakrabarty, Garcia-Olano and Wallace, arXiv:2509.19163.\n"
        "3. Martin, Clean Code, ISBN 978-0-13-235088-4, Prentice Hall, 2008.\n"
        "4. Same work, ISBN-10: 0-13-235088-2.\n"
        "5. An old-scheme preprint, arXiv:math/0309136, is also cited.\n"
        "6. Project page: https://arxiv.org/abs/2509.19163\n",
    )
    clean_run = run("scan_refs.py", [str(clean), "--format", "json"])
    expect_exit("stays silent on valid DOIs, ISBNs, arXiv IDs and URLs", clean_run, 0)

    payload = json.loads(clean_run.stdout)
    check(
        "offline mode is the default and is recorded",
        payload["inventory"]["mode"] == "offline",
        f"(mode {payload['inventory']['mode']})",
    )
    counts = payload["inventory"]["counts"]
    check("extracts both ISBNs", counts["isbn"] == 2, f"(counts {counts})")
    check("extracts the DOI", counts["doi"] >= 1, f"(counts {counts})")
    check("extracts the modern arXiv ID", counts["arxiv"] >= 1, f"(counts {counts})")
    check("extracts the legacy arXiv ID", counts["arxiv-old"] >= 1, f"(counts {counts})")

    usage_run = run("scan_refs.py", [str(clean), "--timeout", "0"])
    expect_exit("rejects a non-positive timeout with exit 2", usage_run, 2)


def test_scan_packages(tmp: Path) -> None:
    print("scan_packages")
    project = tmp / "project"
    write(project, "helper.py", "VALUE = 1\n")
    write(
        project,
        "main.py",
        "import json\n"
        "import pathlib\n"
        "import requests\n"
        "import helper\n"
        "from concurrent.futures import ThreadPoolExecutor\n"
        "from .relative import thing\n"
        "\n"
        "TEXT = 'import quantumjsonify'  # a string, not an import\n",
    )
    write(
        project,
        "package.json",
        json.dumps(
            {
                "name": "demo",
                "dependencies": {"react": "^18.0.0", "zod": "^3.0.0"},
                "devDependencies": {"typescript": "^5.0.0"},
            },
            indent=2,
        )
        + "\n",
    )
    write(project, "requirements.txt", "requests==2.32.3\n# comment\npytest>=8.0\n")
    clean_run = run("scan_packages.py", [str(project), "--format", "json"])
    expect_exit("stays silent on stdlib, local and allowlisted packages", clean_run, 0)
    payload = json.loads(clean_run.stdout)
    statuses = {
        (item["ecosystem"], item["name"]): item["status"] for item in payload["inventory"]["packages"]
    }
    check("stdlib import is classified stdlib", statuses.get(("pypi", "json")) == "stdlib", str(statuses))
    check(
        "sibling module is classified local",
        statuses.get(("pypi", "helper")) == "local",
        str(statuses),
    )
    check(
        "known package is allowlisted",
        statuses.get(("pypi", "requests")) == "allowlisted",
        str(statuses),
    )
    check(
        "npm dependency is allowlisted",
        statuses.get(("npm", "react")) == "allowlisted",
        str(statuses),
    )
    check(
        "an import inside a string literal is not counted",
        ("pypi", "quantumjsonify") not in statuses,
        str(statuses),
    )
    check(
        "offline mode is the default and is recorded",
        payload["inventory"]["mode"] == "offline",
        str(payload["inventory"]["mode"]),
    )

    suspicious = tmp / "suspicious"
    write(
        suspicious,
        "app.py",
        "import quantumjsonify\nfrom hyperfastyaml import load\n",
    )
    write(
        suspicious,
        "package.json",
        json.dumps({"dependencies": {"leftpad-turbo-native": "^1.0.0"}}, indent=2) + "\n",
    )
    dirty_run = run("scan_packages.py", [str(suspicious), "--format", "json"])
    expect_exit("fires on packages it cannot confirm", dirty_run, 1)
    found = rules_in(dirty_run)
    check("reports unverified packages", "packages.unverified" in found, f"(found {sorted(found)})")
    names = {
        item["name"]
        for item in json.loads(dirty_run.stdout)["inventory"]["packages"]
        if item["status"] == "unverified"
    }
    for name in ("quantumjsonify", "hyperfastyaml", "leftpad-turbo-native"):
        check(f"flags {name}", name in names, f"(unverified {sorted(names)})")


def lint_prose_available() -> bool:
    probe = run("lint_voice.py", ["--format", "json"], stdin_text="plain text\n")
    return probe.returncode != 2


def test_lint_voice(tmp: Path) -> None:
    print("lint_voice")
    if not lint_prose_available():
        SKIPS.append(
            "lint_voice: claude-blog lint_prose.py was not found on this machine, "
            "so the wrapper tests did not run. Set ANTI_SLOP_LINT_PROSE."
        )
        print("  SKIP: claude-blog lint_prose.py not found")
        return

    voice = write(tmp, "voice.txt", "# banned tokens\ndelve\nleverage\n")

    dirty = write(
        tmp,
        "voice-dirty.md",
        "# Draft\n\n"
        f"The committee met once{EM}and then adjourned.\n"
        f"The range 1914{EN}1918 is written in body prose here.\n"
        "We must delve into the archive before we leverage the result.\n"
        "Another sentence -- written with the ASCII form -- also breaks the rule.\n",
    )
    dirty_run = run("lint_voice.py", [str(dirty), "--voice", str(voice), "--format", "json"])
    expect_exit("fires on house style violations", dirty_run, 1)
    found = rules_in(dirty_run)
    for rule in ("voice.em_dash", "voice.en_dash", "voice.double_hyphen", "voice.banned_token"):
        check(f"detects {rule}", rule in found, f"(found {sorted(found)})")

    clean = write(
        tmp,
        "voice-clean.md",
        "# Quoting sources\n\n"
        "House style avoids the long dash in body prose. Quoted source text is\n"
        "never restyled, so the lines below stay exactly as published.\n\n"
        f"> The war of 1914{EN}1918 reshaped the discipline{EM}and its funding.\n"
        f"> Smith, A History, 1971, page 42.\n\n"
        f"An inline code span such as `a{EM}b` is a literal, not prose.\n\n"
        "```text\n"
        f"parser.add_argument('--flag')  # dash example: {EM} and {EN}\n"
        "we delve into the buffer here\n"
        "```\n\n"
        "The banned token above sits inside a fenced block, so it is a code\n"
        "sample rather than house prose.\n",
    )
    clean_run = run("lint_voice.py", [str(clean), "--voice", str(voice), "--format", "json"])
    expect_exit(
        "stays silent on quoted source text, inline code and fenced code",
        clean_run,
        0,
    )
    payload = json.loads(clean_run.stdout)
    check(
        "declares itself a house style rule",
        payload["inventory"]["rule_class"] == "house-style",
        str(payload["inventory"].get("rule_class")),
    )
    check(
        "declares that it is not an authorship signal",
        payload["inventory"]["authorship_signal"] is False
        and payload["inventory"]["slop_verdict"] is False,
        str(payload["inventory"]),
    )
    check(
        "records the quoted lines it deliberately skipped",
        payload["inventory"]["quoted_lines_exempt"] >= 2,
        str(payload["inventory"].get("quoted_lines_exempt")),
    )

    text_run = run("lint_voice.py", [str(clean), "--voice", str(voice)])
    check(
        "text output states the house style disclaimer",
        "HOUSE STYLE ONLY" in text_run.stdout
        and "not an authorship signal" in text_run.stdout,
        text_run.stdout,
    )

    quoted_run = run(
        "lint_voice.py", [str(clean), "--voice", str(voice), "--include-quotes", "--format", "json"]
    )
    expect_exit("can be asked to lint quoted lines too", quoted_run, 1)


def build_note(prefix: str, sources: tuple[str, str], heading: str) -> str:
    lines = [
        "---",
        "type: spoke",
        f"title: {heading}",
        f"sources: [{sources[0]}, {sources[1]}]",
        "---",
        "",
        f"# {heading}",
        "",
        f"## Evidence from {sources[0]}",
        "",
    ]
    for block in range(16):
        words = " ".join(f"{prefix}{block:02d}{index:02d}" for index in range(10))
        lines.append(words)
    lines.extend(
        [
            "",
            f"## Procedure recorded against {sources[1]}",
            "",
            f"| {prefix} input | {prefix} output |",
            "| --- | --- |",
            f"| {prefix}alpha | {prefix}beta |",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def test_score_substance(tmp: Path) -> None:
    print("score_substance")
    ledger = write(
        tmp,
        "source-ledger.json",
        json.dumps(
            {
                "sources": [
                    {"id": "SRC-001", "url": "https://arxiv.org/abs/2509.19163"},
                    {"id": "SRC-002", "url": "https://doi.org/10.1126/sciadv.adt3813"},
                    {"id": "SRC-003", "url": "https://arxiv.org/abs/2606.29540"},
                    {"id": "SRC-004", "url": "https://arxiv.org/abs/2512.09292"},
                ]
            },
            indent=2,
        )
        + "\n",
    )

    good = tmp / "vault-good"
    write(good, "concepts/first.md", build_note("kappa", ("SRC-001", "SRC-002"), "Judge agreement"))
    write(good, "concepts/second.md", build_note("omega", ("SRC-003", "SRC-004"), "Dash evidence"))
    good_run = run(
        "score_substance.py",
        ["--vault", str(good), "--ledger", str(ledger), "--format", "json"],
    )
    expect_exit("stays silent on distinct, cited, dense notes", good_run, 0)
    payload = json.loads(good_run.stdout)
    check("scores a clean vault at 100", payload["score"] == 100, str(payload["score"]))
    check(
        "keeps the ported thresholds visible in the metrics",
        payload["metrics"]["near_duplicate_pairs"] == 0
        and payload["metrics"]["specific_citation_coverage"] == 1.0,
        str(payload["metrics"]),
    )

    padded = tmp / "vault-padded"
    body = build_note("kappa", ("SRC-001", "SRC-002"), "Judge agreement")
    write(padded, "concepts/first.md", body)
    write(padded, "concepts/duplicate.md", body)
    padded_run = run(
        "score_substance.py",
        ["--vault", str(padded), "--ledger", str(ledger), "--format", "json"],
    )
    expect_exit("fires on near duplicate notes", padded_run, 1)
    padded_payload = json.loads(padded_run.stdout)
    check(
        "reports the duplicate pair as critical",
        padded_payload["metrics"]["near_duplicate_pairs"] >= 1
        and any("near_duplicate_pairs" in item for item in padded_payload["critical"]),
        str(padded_payload["critical"]),
    )
    check(
        "caps the score for a vault with duplicates",
        padded_payload["score"] <= 40,
        str(padded_payload["score"]),
    )

    missing_run = run("score_substance.py", ["--vault", str(tmp / "no-such-vault")])
    expect_exit("returns exit 2 for a missing vault", missing_run, 2)


def test_no_forbidden_characters() -> None:
    print("house style of the scanners themselves")
    offenders: list[str] = []
    targets = sorted(SCRIPTS.glob("scan_*.py")) + [
        SCRIPTS / "lint_voice.py",
        SCRIPTS / "score_substance.py",
        Path(__file__),
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if EM in line or EN in line:
                offenders.append(f"{path.name}:{number}")
    check("scanner sources contain no long dash characters", not offenders, str(offenders))


def test_never_emits_authorship_verdict(tmp: Path) -> None:
    print("firewall rule 1")
    sample = write(tmp, "firewall.md", "A line with oaicite left in it.\n")
    for script, args in (
        ("scan_residue.py", [str(sample), "--format", "json"]),
        ("scan_placeholders.py", [str(sample), "--format", "json"]),
        ("scan_refs.py", [str(sample), "--format", "json"]),
    ):
        proc = run(script, args)
        payload = json.loads(proc.stdout)
        check(
            f"{script} carries a null authorship verdict",
            payload.get("authorship_verdict", "missing") is None,
            str(payload.get("authorship_verdict")),
        )
        check(
            f"{script} states that it reports defects only",
            "does not judge authorship" in payload.get("note", ""),
            payload.get("note", ""),
        )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="anti-slop-scanners-") as raw:
        tmp = Path(raw)
        test_scan_residue(tmp)
        test_scan_placeholders(tmp)
        test_scan_refs(tmp)
        test_scan_packages(tmp)
        test_lint_voice(tmp)
        test_score_substance(tmp)
        test_no_forbidden_characters()
        test_never_emits_authorship_verdict(tmp)
    print()
    for note in SKIPS:
        print(f"SKIPPED: {note}")
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} of {CHECKS} checks")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print(f"Scanner tests passed: {CHECKS} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
