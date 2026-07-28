#!/usr/bin/env python3
"""Layer 0 scanner: vendor and model residue artifacts left in text.

Residue markers are strings that a rendering or citation layer emitted and
that nobody would type on purpose. They are near deterministic, cheap to
grep, and they have no legitimate false-positive class outside of documents
that discuss the markers themselves, which is why this scanner is fence
aware and inline-code aware for markdown input.

Marker inventory follows the Wikipedia:Signs of AI writing taxonomy,
section E3 (WP:OAICITE, internal formatting and reference markup bugs) and
section F6 (utm_source), as captured in
`.research/prior-art-humanizer-wikipedia.md`. Wikipedia calls E3 markers
"an unambiguous indicator that the text originated with AI"; this scanner
deliberately does not repeat that inference. A residue marker is a
mechanical defect in the document. Removing it is correct regardless of
who wrote the sentence around it, and its presence is not reported here as
evidence of authorship.

Quoted source protection: markdown blockquote lines are exempt by default,
on the same reasoning `lint_voice.py` already documents. You do not edit
somebody else's sentence, so a residue token inside a quotation of a
defective source is a description of the defect rather than the defect. The
skipped lines are counted and reported as `quoted_lines_exempt` rather than
silently dropped, and `--include-quotes` scans them anyway.

Usage:
    python3 scripts/scan_residue.py [PATH ...] [--format text|json]
    cat draft.md | python3 scripts/scan_residue.py

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
    in_span_list,
    load_documents,
    run_cli,
    snippet_for,
    starts_in,
    url_spans,
)

TOOL = "scan_residue"

# (rule id, compiled pattern, message)
RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "residue.oaicite",
        re.compile(r"oaicite"),
        "ChatGPT reference markup residue: oaicite",
    ),
    (
        "residue.content_reference",
        re.compile(r"contentReference"),
        "ChatGPT reference markup residue: contentReference",
    ),
    (
        "residue.oai_citation",
        re.compile(r"oai_citation"),
        "ChatGPT reference markup residue: oai_citation",
    ),
    (
        "residue.turn_search",
        re.compile(r"\bturn\d+search\d+\b"),
        "ChatGPT search-tool residue: turnNsearchN token",
    ),
    (
        "residue.attributable_index",
        re.compile(r"attributableIndex"),
        "ChatGPT reference markup residue: attributableIndex",
    ),
    (
        "residue.gemini_cite",
        re.compile(r"\[cite:\s*\d+(?:\s*,\s*\d+)*\s*\]"),
        "Gemini citation residue: [cite: N] marker",
    ),
    (
        "residue.gemini_cite_start",
        re.compile(r"\[cite_start\]"),
        "Gemini citation residue: [cite_start] marker",
    ),
    (
        "residue.gemini_span",
        re.compile(r"\((?:start_span|end_span)\)"),
        "Gemini span residue: (start_span) or (end_span) marker",
    ),
    (
        "residue.lenticular_citation",
        re.compile("【[^】\n]*†[^】\n]*】"),
        "DeepSeek style citation residue: lenticular brackets with a dagger",
    ),
    (
        "residue.grok_card",
        re.compile(r"grok-card|grok_render_citation_card_json"),
        "Grok citation card residue",
    ),
    (
        "residue.writing_block",
        re.compile(r":::(?:writing|écriture)\{"),
        "Unclassified vendor block residue: :::writing{ directive",
    ),
    (
        "residue.attached_file",
        re.compile(r"\[attached_file:\s*\d+\]"),
        "Perplexity attachment residue: [attached_file:N]",
    ),
    (
        "residue.web_ref",
        re.compile(r"\[web:\s*\d+\]"),
        "Perplexity web reference residue: [web:N]",
    ),
    (
        "residue.ppl_upload",
        re.compile(r"ppl-ai-file-upload"),
        "Perplexity upload host residue in a URL",
    ),
    (
        "residue.utm_source",
        re.compile(
            r"utm_source=(?:chatgpt\.com|chatgpt|openai|copilot\.com|"
            r"perplexity\.ai|perplexity|grok\.com|claude\.ai)",
            re.IGNORECASE,
        ),
        "Vendor tracking parameter left in a URL: utm_source",
    ),
    (
        "residue.referrer",
        re.compile(
            r"referrer=(?:grok\.com|chatgpt\.com|openai\.com|perplexity\.ai)",
            re.IGNORECASE,
        ),
        "Vendor tracking parameter left in a URL: referrer",
    ),
)


def scan_document(
    document: Document,
    include_code: bool = False,
    include_quotes: bool = False,
) -> tuple[list[Finding], int]:
    """Return residue findings for one document, and the quoted-line skip count.

    In markdown, matches inside code blocks, fenced or indented, and inside
    inline code spans are skipped, because documents about residue markers
    quote them. A match that lands inside a URL is still reported: a code
    block is not a licence to ship a tracking parameter. A match on a
    blockquote line is skipped and counted, because quoted source text is not
    yours to edit.
    """
    findings: list[Finding] = []
    quoted_exempt = 0
    for line_no, line in enumerate(document.lines, 1):
        urls = url_spans(line)
        fenced = document.is_markdown and line_no in document.code_lines
        quoted = not include_quotes and document.is_quoted(line_no)
        prose_spans = document.code_free_spans(line_no) if document.is_markdown else None
        for rule, pattern, message in RULES:
            for match in pattern.finditer(line):
                span = (match.start(), match.end())
                in_url = in_span_list(span, urls)
                if quoted:
                    quoted_exempt += 1
                    continue
                if not include_code and not in_url:
                    if fenced:
                        continue
                    if prose_spans is not None and not starts_in(span, prose_spans):
                        continue
                detail = message + (" (inside a URL)" if in_url else "")
                findings.append(
                    Finding(
                        path=document.label,
                        line=line_no,
                        column=match.start() + 1,
                        rule=rule,
                        message=detail,
                        snippet=snippet_for(line, match.start(), match.end()),
                    )
                )
    return findings, quoted_exempt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scan_residue.py",
        description="Detect vendor and model residue markers left in text.",
    )
    add_io_arguments(parser)
    parser.add_argument(
        "--include-code",
        action="store_true",
        help="Also scan code blocks and inline code spans in markdown.",
    )
    parser.add_argument(
        "--include-quotes",
        action="store_true",
        help="Also scan markdown blockquote lines. Off by default: quoted source "
             "text is not yours to edit.",
    )
    args = parser.parse_args(argv)
    findings: list[Finding] = []
    quoted_exempt = 0
    for document in load_documents(args):
        document_findings, exempt = scan_document(
            document, include_code=args.include_code, include_quotes=args.include_quotes
        )
        findings.extend(document_findings)
        quoted_exempt += exempt
    inventory = {"quoted_lines_exempt": quoted_exempt}
    if args.format == "text" and quoted_exempt:
        print(
            f"exempt: {quoted_exempt} match(es) inside quoted source lines were not reported."
        )
    return emit(findings, args.format, TOOL, inventory=inventory)


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
