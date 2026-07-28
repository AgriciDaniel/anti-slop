#!/usr/bin/env python3
"""Layer 0 scanner: reference integrity for DOIs, arXiv IDs, ISBNs and URLs.

Fabricated citations are the defect class with the most harm and the most
checkability, which is why this scanner exists. Wikipedia:Signs of AI
writing section F (WP:AIFICTREF) names the taxonomy this implements:
F1 broken external links, F2 invalid DOIs and ISBNs (checksum failures),
F3 DOIs that lead to unrelated articles, F4 book citations without page
numbers, F5 unconventional reference markup, F6 vendor tracking parameters,
F7 declared but unused named references. See
`.research/prior-art-humanizer-wikipedia.md`.

What this scanner decides offline, with no network access at all:

- DOI shape. A DOI is `10.` plus a 4 to 9 digit registrant code, a slash,
  and a non-empty suffix. Placeholder registrants and X-filled suffixes are
  reported.
- arXiv identifier shape and plausible date range. New style identifiers
  are YYMM.NNNNN. The scheme began in April 2007, the sequence number grew
  from 4 to 5 digits in January 2015, and an identifier dated after the
  current month cannot exist yet.
- ISBN-10 and ISBN-13 checksums, which are pure arithmetic.
- URL shape, plus a blocklist of example and loopback hosts that can never
  be a real citation target.

What it cannot decide offline: whether a well-formed DOI resolves, whether
it resolves to the work that was cited (F3), and whether a link is dead
(F1). `--online` resolves DOIs, arXiv IDs and URLs over the network. It is
opt-in, it is never implied by any other flag, and it prints a notice
before the first request. Title matching against the DOI record (F3) is
deliberately out of scope for a deterministic scanner: comparing a cited
title to a registry title is a judgement call and belongs in a Layer 1
procedure with a human-readable artifact.

This scanner reports mechanical defects only. A defective citation is a
defect no matter who wrote it. No authorship verdict is ever emitted.

Code awareness: references are extracted through the same shared masking
`scan_residue.py` uses, so a deliberately fake DOI inside a ```bibtex fence,
an indented code block or an inline code span is a code sample rather than a
citation. `--include-code` extracts from code regions anyway.

Determinism: the only calendar-dependent rule is the future arXiv check.
It reads `--reference-date`, which defaults to today, so a pinned date makes
two runs byte identical. Nothing else here reads the clock.

Usage:
    python3 scripts/scan_refs.py [PATH ...] [--format text|json]
    python3 scripts/scan_refs.py paper.md --reference-date 2026-07-28
    python3 scripts/scan_refs.py paper.md --online --timeout 10

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import (  # noqa: E402
    Document,
    Finding,
    UsageError,
    add_io_arguments,
    emit,
    is_prose,
    load_documents,
    prose_spans_for,
    run_cli,
    snippet_for,
)

TOOL = "scan_refs"

BLOCKED_HOSTS = {
    "example.com",
    "example.org",
    "example.net",
    "example.edu",
    "www.example.com",
    "www.example.org",
    "www.example.net",
    "www.example.edu",
    "localhost",
    "www.localhost",
    "127.0.0.1",
    "0.0.0.0",
    "example",
}
BLOCKED_SUFFIXES = (".example.com", ".example.org", ".example.net", ".example")

DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>,;)\]}]+")
ARXIV_NEW_RE = re.compile(
    r"(?:arxiv[.:\s]*(?:org/)?(?:abs/|pdf/)?|arxiv\s+)(\d{4})\.(\d{4,5})(v\d+)?",
    re.IGNORECASE,
)
ARXIV_OLD_RE = re.compile(
    r"arxiv[.:\s]*(?:org/)?(?:abs/)?([a-z-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?",
    re.IGNORECASE,
)
ISBN_RE = re.compile(
    r"\bISBN(?:[-\s]?1[03])?\b[:\s]*([0-9](?:[\s\-]?[0-9Xx]){8,16})",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s<>\"'`\]}]+")
TRAILING_PUNCTUATION = ".,;:!?)]}»'\""

ARXIV_EPOCH = (2007, 4)
ARXIV_FIVE_DIGIT_EPOCH = (2015, 1)


@dataclass(frozen=True)
class Reference:
    kind: str
    value: str
    path: str
    line: int
    column: int
    snippet: str


def strip_trailing(value: str) -> str:
    return value.rstrip(TRAILING_PUNCTUATION)


def parse_reference_date(value: str | None) -> date:
    """Return the calendar date the arXiv range checks are anchored to.

    The clock is read exactly once, here, and only when the caller declined to
    pin a date. Everything else in this scanner is pure.
    """
    if value is None:
        return date.today()
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise UsageError(
            f"--reference-date must be an ISO calendar date in YYYY-MM-DD form: {value!r}"
        ) from exc


def extract_references(document: Document, include_code: bool = False) -> list[Reference]:
    """Extract every DOI, arXiv ID, ISBN and http(s) URL in the document.

    In markdown, code regions are skipped. A fake DOI written to demonstrate
    what a fake DOI looks like is a code sample, and reporting it would leave
    the scanner unable to document itself.
    """
    patterns = (
        ("doi", DOI_RE, lambda m: strip_trailing(m.group(0))),
        ("arxiv", ARXIV_NEW_RE, lambda m: f"{m.group(1)}.{m.group(2)}{m.group(3) or ''}"),
        ("arxiv-old", ARXIV_OLD_RE, lambda m: m.group(1) + (m.group(2) or "")),
        ("isbn", ISBN_RE, lambda m: m.group(1).strip()),
        ("url", URL_RE, lambda m: strip_trailing(m.group(0))),
    )
    references: list[Reference] = []
    for line_no, line in enumerate(document.lines, 1):
        spans = prose_spans_for(document, line_no, include_code)
        if spans is not None and not spans:
            continue
        for kind, pattern, extract in patterns:
            for match in pattern.finditer(line):
                if not is_prose(spans, match.start(), match.end()):
                    continue
                value = extract(match)
                if not value:
                    continue
                references.append(
                    Reference(kind, value, document.label, line_no, match.start() + 1,
                              snippet_for(line, match.start(), match.end()))
                )
    return references


def check_doi(reference: Reference) -> list[Finding]:
    findings: list[Finding] = []
    prefix, _, suffix = reference.value.partition("/")
    registrant = prefix.split(".", 1)[1] if "." in prefix else ""
    if not suffix:
        findings.append(_finding(reference, "refs.doi_shape", "DOI has no suffix after the slash"))
        return findings
    if registrant.strip("0") == "":
        findings.append(
            _finding(reference, "refs.doi_placeholder",
                     "DOI registrant code is all zeros, which is a placeholder")
        )
    upper = suffix.upper()
    if "XXXX" in upper or upper.startswith("EXAMPLE") or upper in {"XXX", "TBD", "TODO"}:
        findings.append(
            _finding(reference, "refs.doi_placeholder", "DOI suffix is placeholder text")
        )
    if len(suffix) < 2:
        findings.append(
            _finding(reference, "refs.doi_shape", "DOI suffix is implausibly short")
        )
    return findings


def check_arxiv(reference: Reference, today: date) -> list[Finding]:
    findings: list[Finding] = []
    if reference.kind == "arxiv-old":
        return findings
    core = reference.value.split("v", 1)[0]
    yymm, _, number = core.partition(".")
    year = 2000 + int(yymm[:2])
    month = int(yymm[2:])
    if month < 1 or month > 12:
        findings.append(
            _finding(reference, "refs.arxiv_shape",
                     f"arXiv identifier month {yymm[2:]} is not a real month")
        )
        return findings
    if (year, month) < ARXIV_EPOCH:
        findings.append(
            _finding(reference, "refs.arxiv_range",
                     "arXiv YYMM.NNNNN identifiers start at 0704, April 2007")
        )
    if (year, month) > (today.year, today.month):
        findings.append(
            _finding(reference, "refs.arxiv_future",
                     f"arXiv identifier is dated {year}-{month:02d}, later than today")
        )
    if (year, month) >= ARXIV_FIVE_DIGIT_EPOCH and len(number) != 5:
        findings.append(
            _finding(reference, "refs.arxiv_digits",
                     "arXiv identifiers from 1501 onward use a 5 digit sequence number",
                     severity="review")
        )
    if (year, month) < ARXIV_FIVE_DIGIT_EPOCH and len(number) != 4:
        findings.append(
            _finding(reference, "refs.arxiv_digits",
                     "arXiv identifiers before 1501 use a 4 digit sequence number",
                     severity="review")
        )
    return findings


def normalize_isbn(value: str) -> str:
    return re.sub(r"[\s\-]", "", value).upper()


def isbn10_ok(digits: str) -> bool:
    if len(digits) != 10 or not re.fullmatch(r"\d{9}[\dX]", digits):
        return False
    total = 0
    for index, char in enumerate(digits):
        total += (10 - index) * (10 if char == "X" else int(char))
    return total % 11 == 0


def isbn13_ok(digits: str) -> bool:
    if len(digits) != 13 or not digits.isdigit():
        return False
    total = sum(int(char) * (1 if index % 2 == 0 else 3) for index, char in enumerate(digits))
    return total % 10 == 0


def check_isbn(reference: Reference) -> list[Finding]:
    digits = normalize_isbn(reference.value)
    if len(digits) == 10:
        if not isbn10_ok(digits):
            return [_finding(reference, "refs.isbn_checksum", "ISBN-10 checksum fails")]
        return []
    if len(digits) == 13:
        if not digits.startswith(("978", "979")):
            return [
                _finding(reference, "refs.isbn_shape",
                         "ISBN-13 must start with the 978 or 979 prefix")
            ]
        if not isbn13_ok(digits):
            return [_finding(reference, "refs.isbn_checksum", "ISBN-13 checksum fails")]
        return []
    return [
        _finding(reference, "refs.isbn_shape",
                 f"ISBN has {len(digits)} characters, expected 10 or 13")
    ]


def check_url(reference: Reference) -> list[Finding]:
    parsed = urlparse(reference.value)
    host = parsed.netloc.lower()
    if "@" in host:
        host = host.rsplit("@", 1)[1]
    if ":" in host and not host.startswith("["):
        host = host.rsplit(":", 1)[0]
    if parsed.scheme not in {"http", "https"} or not host:
        return [_finding(reference, "refs.url_shape", "URL is not a well-formed http(s) URL")]
    if host in BLOCKED_HOSTS or host.endswith(BLOCKED_SUFFIXES):
        return [
            _finding(reference, "refs.url_placeholder_host",
                     f"URL points at the placeholder or loopback host {host}")
        ]
    if "." not in host and host not in {"localhost"}:
        return [
            _finding(reference, "refs.url_shape",
                     f"URL host {host} has no dot and is not a known local name")
        ]
    return []


def _finding(reference: Reference, rule: str, message: str, severity: str = "defect") -> Finding:
    return Finding(
        path=reference.path,
        line=reference.line,
        column=reference.column,
        rule=rule,
        message=f"{message}: {reference.value}",
        snippet=reference.snippet,
        severity=severity,
    )


def online_target(reference: Reference) -> str | None:
    if reference.kind == "doi":
        return "https://doi.org/" + reference.value
    if reference.kind == "arxiv":
        return "https://arxiv.org/abs/" + reference.value
    if reference.kind == "arxiv-old":
        return "https://arxiv.org/abs/" + reference.value
    if reference.kind == "url":
        return reference.value
    return None


def resolve(target: str, timeout: float) -> tuple[int | None, str]:
    """Resolve one URL. Network call. Returns (status code or None, note)."""
    import urllib.error  # imported here so importing this module never touches the net
    import urllib.request

    headers = {"User-Agent": "anti-slop-scan-refs/1.0 (+deterministic link check)"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(target, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status, method
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405, 501, 400}:
                continue
            return exc.code, f"{method} {exc.reason}"
        except Exception as exc:  # noqa: BLE001 - any transport failure is a finding
            if method == "HEAD":
                continue
            return None, f"{method} {type(exc).__name__}: {exc}"
    return None, "unresolved"


def check_online(references: list[Reference], timeout: float) -> list[Finding]:
    findings: list[Finding] = []
    seen: dict[str, tuple[int | None, str]] = {}
    print(
        "NOTICE: --online makes outbound network requests to doi.org, arxiv.org "
        "and every cited host. Offline mode is the default and never does this.",
        file=sys.stderr,
    )
    for reference in references:
        target = online_target(reference)
        if target is None:
            continue
        if target not in seen:
            seen[target] = resolve(target, timeout)
        status, note = seen[target]
        if status is None:
            findings.append(
                _finding(reference, "refs.online_unreachable",
                         f"did not resolve ({note})", severity="unresolved")
            )
        elif status >= 400:
            findings.append(
                _finding(reference, "refs.online_status",
                         f"resolved with HTTP {status} ({note})")
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scan_refs.py",
        description="Check DOIs, arXiv IDs, ISBNs and URLs for mechanical defects.",
    )
    add_io_arguments(parser)
    parser.add_argument(
        "--online",
        action="store_true",
        help="Opt in to network resolution of DOIs, arXiv IDs and URLs. "
             "Offline is the default and makes no network requests.",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, help="Per-request timeout for --online."
    )
    parser.add_argument(
        "--list", action="store_true", help="Print the extracted reference inventory."
    )
    parser.add_argument(
        "--include-code",
        action="store_true",
        help="Also extract references from code blocks and inline code spans.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        metavar="YYYY-MM-DD",
        help="Calendar date the future-arXiv check is anchored to. Defaults to "
             "today. Pin it to make two runs byte identical.",
    )
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        raise UsageError("--timeout must be positive")
    today = parse_reference_date(args.reference_date)

    references: list[Reference] = []
    for document in load_documents(args):
        references.extend(extract_references(document, include_code=args.include_code))

    findings: list[Finding] = []
    for reference in references:
        if reference.kind == "doi":
            findings.extend(check_doi(reference))
        elif reference.kind in {"arxiv", "arxiv-old"}:
            findings.extend(check_arxiv(reference, today))
        elif reference.kind == "isbn":
            findings.extend(check_isbn(reference))
        elif reference.kind == "url":
            findings.extend(check_url(reference))
    if args.online:
        findings.extend(check_online(references, args.timeout))

    inventory = {
        "mode": "online" if args.online else "offline",
        "reference_date": today.isoformat(),
        "counts": {
            kind: sum(1 for reference in references if reference.kind == kind)
            for kind in ("doi", "arxiv", "arxiv-old", "isbn", "url")
        },
        "references": [
            {
                "kind": reference.kind,
                "value": reference.value,
                "path": reference.path,
                "line": reference.line,
            }
            for reference in references
        ],
    }
    if args.format == "text":
        counts = inventory["counts"]
        print(
            "extracted: "
            + ", ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
            + f"  mode={inventory['mode']}"
        )
        if args.list:
            for reference in references:
                print(f"  {reference.kind}\t{reference.value}\t"
                      f"{reference.path}:{reference.line}")
    return emit(findings, args.format, TOOL, inventory=inventory)


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
