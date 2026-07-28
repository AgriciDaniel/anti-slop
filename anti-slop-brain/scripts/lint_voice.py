#!/usr/bin/env python3
"""Layer 0 linter: house style, and nothing more than house style.

READ THIS FIRST. Every finding this tool emits is a house style rule. A
house style rule is a preference the owner of the document chose. It is not
a slop verdict, it is not evidence about who wrote the text, and it must
never be quoted as an authorship signal. Czuma (arXiv 2606.29540,
2026-06-28), pre-registered on 69,632 medRxiv preprints, states the
position this tool adopts verbatim: the em dash is a population-level
indicator, not a per-paper detector of LLM use. Punctuation preference is
a style choice, and detector bias against English-language learners is
peer reviewed and current (Stowe et al., ACL 2026, arXiv 2512.09292).

What it checks:

1. The three forbidden prose characters: U+2014, U+2013, and ASCII
   space-hyphen-hyphen-space.
2. Optional banned tokens from a voice file, one token per line, `#` starts
   a comment.

Both checks run through the same masking machinery the other Layer 0
scanners use, from `scan_common.py`: code blocks in either markdown syntax,
fenced and four-space indented, are skipped, and so are inline code spans.
A document is therefore free to demonstrate the exact character it forbids.

Attribution. The rule set and the fence and backtick handling are derived
from the design of `scripts/lint_prose.py` in claude-blog 2.1.0, which
solved the same problem first. This is a clean reimplementation against the
shared helpers in this repository, not a wrapper: nothing here imports or
executes code from another project, because a linter that only runs on one
machine is a linter that does not run. See THIRD_PARTY_NOTICES.md.

Quoted source protection: lines that are markdown blockquotes are exempt by
default. You do not edit punctuation inside somebody else's sentence, so an
en dash in a quoted date range, or an em dash in a quoted citation, is not
a violation. The skipped matches are counted and reported as
`quoted_lines_exempt` rather than silently dropped, and `--include-quotes`
lints them anyway.

Usage:
    python3 scripts/lint_voice.py [PATH ...] [--voice voice.txt]
    cat draft.md | python3 scripts/lint_voice.py --stdin-name draft.md

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
    UsageError,
    add_io_arguments,
    emit,
    is_prose,
    load_documents,
    prose_spans_for,
    run_cli,
    snippet_for,
)

TOOL = "lint_voice"

HOUSE_STYLE_NOTE = (
    "HOUSE STYLE ONLY. These findings are house style rules chosen by the "
    "owner of this document. They are not a slop verdict, not a quality "
    "judgement, and not an authorship signal. Punctuation preference says "
    "nothing about who or what wrote the text."
)

DERIVED_FROM = (
    "Rule set and masking design derived from claude-blog 2.1.0 "
    "scripts/lint_prose.py. Reimplemented here; not a runtime dependency."
)

# (literal, rule id, description). Written as escapes on purpose: this file
# is itself subject to the rule it enforces.
FORBIDDEN: tuple[tuple[str, str, str], ...] = (
    ("\u2014", "voice.em_dash", "U+2014 em dash"),
    ("\u2013", "voice.en_dash", "U+2013 en dash"),
    ("\x20--\x20", "voice.double_hyphen", "ASCII double hyphen with spaces"),
)


def load_voice_tokens(path: Path | None) -> list[str]:
    if path is None:
        return []
    if not path.is_file():
        raise UsageError(f"no such voice file: {path}")
    tokens: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            tokens.append(line)
    return tokens


def token_pattern(token: str) -> re.Pattern[str]:
    """Compile a banned token into a word-boundary-aware pattern.

    The boundary is only asserted on an end that is alphanumeric, so a token
    that starts or ends in punctuation still matches.
    """
    escaped = re.escape(token)
    left = r"\b" if token[:1].isalnum() else ""
    right = r"\b" if token[-1:].isalnum() else ""
    return re.compile(left + escaped + right, re.IGNORECASE)


def first_prose_index(line: str, spans: list[tuple[int, int]] | None, needle: str) -> int:
    """Return the first index of `needle` that lands in prose, or -1."""
    start = line.find(needle)
    while start != -1:
        if is_prose(spans, start, start + len(needle)):
            return start
        start = line.find(needle, start + 1)
    return -1


def first_prose_match(
    line: str, spans: list[tuple[int, int]] | None, pattern: re.Pattern[str]
) -> re.Match[str] | None:
    """Return the first match of `pattern` that lands in prose, or None."""
    for match in pattern.finditer(line):
        if is_prose(spans, match.start(), match.end()):
            return match
    return None


def lint_document(
    document: Document,
    tokens: list[str],
    include_code: bool = False,
    include_quotes: bool = False,
) -> tuple[list[Finding], int]:
    """Return house style findings for one document, and the quoted skip count.

    One finding per rule per line, anchored at the first occurrence that is
    not inside code. Repeating a rule for every occurrence on the same line
    tells the author nothing the first hit did not already tell them.
    """
    findings: list[Finding] = []
    quoted_exempt = 0
    compiled = [(token, token_pattern(token)) for token in tokens]
    for line_no, line in enumerate(document.lines, 1):
        spans = prose_spans_for(document, line_no, include_code)
        quoted = not include_quotes and document.is_quoted(line_no)
        for needle, rule, description in FORBIDDEN:
            start = first_prose_index(line, spans, needle)
            if start < 0:
                continue
            if quoted:
                quoted_exempt += 1
                continue
            end = start + len(needle)
            findings.append(
                Finding(
                    path=document.label,
                    line=line_no,
                    column=start + 1,
                    rule=rule,
                    message=f"house style forbids {description}",
                    snippet=snippet_for(line, start, end),
                    severity="house-style",
                )
            )
        for token, pattern in compiled:
            match = first_prose_match(line, spans, pattern)
            if match is None:
                continue
            if quoted:
                quoted_exempt += 1
                continue
            findings.append(
                Finding(
                    path=document.label,
                    line=line_no,
                    column=match.start() + 1,
                    rule="voice.banned_token",
                    message=f"house style banned token: {token}",
                    snippet=snippet_for(line, match.start(), match.end()),
                    severity="house-style",
                )
            )
    return findings, quoted_exempt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lint_voice.py",
        description="House style linter. Standard library only. Not a slop verdict.",
    )
    add_io_arguments(parser)
    parser.add_argument("--voice", default=None, help="Voice file of banned tokens.")
    parser.add_argument(
        "--include-code",
        action="store_true",
        help="Also lint code blocks and inline code spans in markdown.",
    )
    parser.add_argument(
        "--include-quotes", action="store_true",
        help="Also lint markdown blockquote lines. Off by default: quoted source "
             "text is not yours to restyle.",
    )
    args = parser.parse_args(argv)

    tokens = load_voice_tokens(Path(args.voice) if args.voice else None)

    findings: list[Finding] = []
    exempt_total = 0
    for document in load_documents(args):
        document_findings, exempt = lint_document(
            document,
            tokens,
            include_code=args.include_code,
            include_quotes=args.include_quotes,
        )
        findings.extend(document_findings)
        exempt_total += exempt

    inventory = {
        "rule_class": "house-style",
        "authorship_signal": False,
        "slop_verdict": False,
        "statement": HOUSE_STYLE_NOTE,
        "derived_from": DERIVED_FROM,
        "banned_tokens": tokens,
        "quoted_lines_exempt": exempt_total,
    }
    if args.format == "text":
        print(HOUSE_STYLE_NOTE)
        if exempt_total:
            print(f"exempt: {exempt_total} finding(s) inside quoted source lines were not reported.")
    exit_code = emit(findings, args.format, TOOL, inventory=inventory)
    if args.format == "text":
        print(HOUSE_STYLE_NOTE)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
