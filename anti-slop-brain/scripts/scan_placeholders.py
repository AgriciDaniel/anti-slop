#!/usr/bin/env python3
"""Layer 0 scanner: unresolved template and placeholder text.

Placeholders are Mad-Libs blanks that a generation or templating step left
behind: `[Your Name]`, `|url=INSERT_SOURCE_URL_30`, `access-date=20XX`,
`TODO: quote`. They are unambiguous defects. The document promises content
that is not there.

The marker inventory follows Wikipedia:Signs of AI writing section D3
(WP:AIPLACEHOLDER, phrasal templates and placeholder text) and the
placeholder citation fields listed there, as captured in
`.research/prior-art-humanizer-wikipedia.md`.

Two false-positive classes are handled explicitly. First, documentation
that teaches a date format writes `YYYY-MM-DD` in running prose, so the
bare token is only reported when it is the value of a date field. Second,
templates and examples live in fenced code blocks, so markdown fences and
inline code spans are skipped unless `--include-code` is passed.

This scanner reports mechanical defects only. It never emits an authorship
verdict.

Usage:
    python3 scripts/scan_placeholders.py [PATH ...] [--format text|json]
    cat draft.md | python3 scripts/scan_placeholders.py

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import (  # noqa: E402
    Document,
    Finding,
    add_io_arguments,
    emit,
    load_documents,
    run_cli,
    snippet_for,
    starts_in,
)

TOOL = "scan_placeholders"

DATE_FIELD = (
    r"(?:access[-_ ]?date|accessdate|accessed|date|published|publication[-_ ]?date|"
    r"updated|retrieved|last[-_ ]?verified|refresh[-_ ]?due|created|deadline)"
)
URL_FIELD = r"(?:url|link|href|src|source[-_ ]?url|archive[-_ ]?url|permalink)"

RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "placeholder.your_field",
        re.compile(
            r"\[(?:your|our|my|client|company|entertainer's|author's|insert|specific|"
            r"describe|add|name of)[^\]\n]{0,70}\](?!\()",
            re.IGNORECASE,
        ),
        "Unresolved bracket placeholder, for example [Your Name]",
    ),
    (
        "placeholder.insert_token",
        re.compile(
            r"\b(?:INSERT|PASTE)_[A-Z0-9_]{2,}(?:_\d+)?\b|\bINSERT_SOURCE_URL(?:_\d+)?\b"
            r"|\bSOURCE_PUBLISHER\b|\bSOURCE_TITLE\b",
        ),
        "Unresolved uppercase template token, for example INSERT_SOURCE_URL",
    ),
    (
        "placeholder.date_field_x",
        re.compile(
            DATE_FIELD + r"\s*[:=]\s*[\"']?[^\s|}\]\"'<>]*(?:XX|20XX)[^\s|}\]\"'<>]*",
            re.IGNORECASE,
        ),
        "Date field still holds an X placeholder, for example access-date=20XX",
    ),
    (
        "placeholder.date_field_yyyy",
        re.compile(
            DATE_FIELD + r"\s*[:=]\s*[\"'\[]?\s*YYYY-MM-DD",
            re.IGNORECASE,
        ),
        "Date field still holds the literal YYYY-MM-DD format string",
    ),
    (
        "placeholder.year_x",
        re.compile(r"\b20XX\b"),
        "Unresolved year placeholder 20XX",
    ),
    (
        "placeholder.todo_quote",
        re.compile(r"TODO\s*:?\s*(?:add\s+)?quote", re.IGNORECASE),
        "Unresolved quote placeholder: TODO quote",
    ),
    (
        "placeholder.quote_needed",
        re.compile(r"\[\s*(?:quote|citation|source|page)\s+needed\s*\]", re.IGNORECASE),
        "Unresolved bracket note, for example [quote needed]",
    ),
    (
        "placeholder.placeholder_quote",
        re.compile(r"placeholder\s+(?:quote|text|citation|source)", re.IGNORECASE),
        "Text describes itself as a placeholder",
    ),
    (
        "placeholder.lorem_ipsum",
        re.compile(r"lorem\s+ipsum", re.IGNORECASE),
        "Lorem ipsum filler text",
    ),
    (
        "placeholder.your_tag",
        re.compile(r"<your\s", re.IGNORECASE),
        "Unresolved angle-bracket placeholder, for example <your api key>",
    ),
    (
        "placeholder.url_field_tbd",
        re.compile(
            URL_FIELD + r"\s*[:=]\s*[\"']?[^\s|}\]\"'<>]*\bTBD\b[^\s|}\]\"'<>]*",
            re.IGNORECASE,
        ),
        "URL field still holds TBD",
    ),
    (
        "placeholder.url_tbd",
        re.compile(r"https?://[^\s<>\"')\]]*\bTBD\b", re.IGNORECASE),
        "URL contains TBD",
    ),
)


def scan_document(document: Document, include_code: bool = False) -> list[Finding]:
    """Return placeholder findings for one document."""
    findings: list[Finding] = []
    for line_no, line in enumerate(document.lines, 1):
        fenced = document.is_markdown and line_no in document.fenced_lines
        if fenced and not include_code:
            continue
        prose_spans = (
            document.code_free_spans(line_no)
            if document.is_markdown and not include_code
            else None
        )
        for rule, pattern, message in RULES:
            for match in pattern.finditer(line):
                span = (match.start(), match.end())
                if prose_spans is not None and not starts_in(span, prose_spans):
                    continue
                findings.append(
                    Finding(
                        path=document.label,
                        line=line_no,
                        column=match.start() + 1,
                        rule=rule,
                        message=message,
                        snippet=snippet_for(line, match.start(), match.end()),
                    )
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scan_placeholders.py",
        description="Detect unresolved template and placeholder text.",
    )
    add_io_arguments(parser)
    parser.add_argument(
        "--include-code",
        action="store_true",
        help="Also scan fenced code blocks and inline code spans in markdown.",
    )
    args = parser.parse_args(argv)
    findings: list[Finding] = []
    for document in load_documents(args):
        findings.extend(scan_document(document, include_code=args.include_code))
    return emit(findings, args.format, TOOL)


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
