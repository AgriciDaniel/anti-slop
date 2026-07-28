#!/usr/bin/env python3
"""Shared helpers for the Layer 0 deterministic scanners.

Layer 0 scanners report mechanical defects only. They never emit an
authorship verdict, never estimate whether a model produced the text, and
never score style. See PLAN.md section 3 for the firewall rules.

Fence tracking mirrors the approach proven in claude-blog 2.1.0
`scripts/lint_prose.py`: the opening fence delimiter is tracked so that a
nested fence with a different delimiter, or a shorter run of the same
character, does not toggle state.

Markdown has two code block syntaxes, not one. An indented code block is
four spaces of leading whitespace after a blank line, and it is exactly as
much a code block as a fenced one. `code_line_numbers` covers both, so a
document that demonstrates a defect token in an indented block is not
punished for it. Indentation inside a list is measured from the list item
content column, which is what CommonMark specifies, so an ordinary wrapped
list paragraph is still prose.

Standard library only. No network access anywhere in this module.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

DISCLAIMER = (
    "Mechanical defect report only. This scanner reports residue, placeholders, "
    "reference integrity, package existence, or house style. It does not judge "
    "authorship and it is not evidence about who or what wrote the text."
)

MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx", ".mdown"}

DEFAULT_EXTENSIONS = (
    ".md", ".markdown", ".mdx", ".txt", ".rst", ".py", ".json",
    ".yaml", ".yml", ".toml", ".html", ".htm", ".csv", ".tex",
)

SKIP_DIR_NAMES = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", "venv", ".venv",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".ruff_cache",
}

FENCE_RE = re.compile(r"(`{3,}|~{3,})")
URL_RE = re.compile(r"https?://[^\s<>\]\"'`)]+")
DOUBLE_TICK_RE = re.compile(r"``[^\n]*?``")
SINGLE_TICK_RE = re.compile(r"`[^`\n]*`")
LIST_MARKER_RE = re.compile(r"^(\s*)(?:[-*+]|\d{1,9}[.)])(\s+)\S")
BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>")

# A markdown indented code block starts four columns past the enclosing
# content column. Tabs are expanded to this many columns when measuring.
INDENT_CODE_COLUMNS = 4
TAB_WIDTH = 4

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2


class UsageError(Exception):
    """Raised for bad invocation. Callers map this to exit code 2."""


@dataclass(frozen=True)
class Finding:
    """One mechanical defect at one location."""

    path: str
    line: int
    column: int
    rule: str
    message: str
    snippet: str
    severity: str = "defect"

    def as_dict(self) -> dict:
        return asdict(self)


class Document:
    """A unit of text to scan, with code-region bookkeeping."""

    def __init__(self, label: str, text: str, is_markdown: bool) -> None:
        self.label = label
        self.text = text
        self.is_markdown = is_markdown
        self.lines = text.splitlines()
        self.code_lines = code_line_numbers(text) if is_markdown else set()
        # Kept under the original name because the scanners read it, and
        # because both syntaxes are code blocks for every purpose here.
        self.fenced_lines = self.code_lines

    def is_quoted(self, line_no: int) -> bool:
        """True when the line is a markdown blockquote.

        A blockquote is somebody else's sentence. Quoting a defective source
        in order to describe the defect is the normal way to document one.
        """
        if not self.is_markdown:
            return False
        return bool(BLOCKQUOTE_RE.match(self.lines[line_no - 1]))

    def code_free_spans(self, line_no: int) -> list[tuple[int, int]]:
        """Return character spans of the line that are outside inline code.

        Line numbers are 1 based. For a non-markdown document the whole line
        is returned, because backticks carry no meaning there.
        """
        line = self.lines[line_no - 1]
        if not self.is_markdown:
            return [(0, len(line))]
        masked = _mask_inline_code(line)
        spans: list[tuple[int, int]] = []
        start: int | None = None
        for index, char in enumerate(masked):
            if char == "\x00":
                if start is not None:
                    spans.append((start, index))
                    start = None
            elif start is None:
                start = index
        if start is not None:
            spans.append((start, len(masked)))
        return spans


def _mask_inline_code(line: str) -> str:
    """Replace inline code spans with NUL characters, preserving length.

    Double backtick spans are masked first, exactly as lint_prose.py does,
    so that the single backtick pattern cannot match the empty span between
    two opening backticks.
    """
    masked = DOUBLE_TICK_RE.sub(lambda m: "\x00" * len(m.group(0)), line)
    masked = SINGLE_TICK_RE.sub(lambda m: "\x00" * len(m.group(0)), masked)
    return masked


def fenced_line_numbers(text: str) -> set[int]:
    """Return the set of 1 based line numbers inside a fenced code block.

    The fence delimiter lines themselves are included.
    """
    inside: set[int] = set()
    fence_open: str | None = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        match = FENCE_RE.match(stripped)
        if fence_open is None:
            if match is not None:
                fence_open = match.group(1)
                inside.add(number)
            continue
        inside.add(number)
        if (
            match is not None
            and match.group(1)[0] == fence_open[0]
            and len(match.group(1)) >= len(fence_open)
        ):
            fence_open = None
    return inside


def indent_columns(line: str) -> int:
    """Return the visual indentation width of the line, tabs expanded."""
    width = 0
    for char in line:
        if char == " ":
            width += 1
        elif char == "\t":
            width += TAB_WIDTH - (width % TAB_WIDTH)
        else:
            break
    return width


def indented_code_line_numbers(text: str, fenced: set[int]) -> set[int]:
    """Return the 1 based line numbers inside a markdown indented code block.

    An indented code block cannot interrupt a paragraph, so a run only opens
    after a blank line or at the start of the document. Inside a list the
    threshold moves to the list item content column plus four, which is what
    keeps an ordinary indented list continuation classified as prose.
    """
    inside: set[int] = set()
    in_code = False
    threshold = INDENT_CODE_COLUMNS
    list_indent = 0
    after_blank = True
    for number, line in enumerate(text.splitlines(), 1):
        if number in fenced:
            in_code = False
            after_blank = False
            continue
        if not line.strip():
            after_blank = True
            continue
        width = indent_columns(line)
        if in_code:
            if width >= threshold:
                inside.add(number)
                after_blank = False
                continue
            in_code = False
        if after_blank and width >= list_indent + INDENT_CODE_COLUMNS:
            in_code = True
            threshold = list_indent + INDENT_CODE_COLUMNS
            inside.add(number)
            after_blank = False
            continue
        marker = LIST_MARKER_RE.match(line)
        if marker is not None:
            list_indent = marker.end(2)
        elif width < list_indent:
            list_indent = 0
        after_blank = False
    return inside


def code_line_numbers(text: str) -> set[int]:
    """Return every 1 based line number that markdown treats as code.

    Both syntaxes count: a fenced block and an indented block. This is the
    set the scanners mask, so a document is free to demonstrate the exact
    token it warns about without tripping its own scanner.
    """
    fenced = fenced_line_numbers(text)
    return fenced | indented_code_line_numbers(text, fenced)


def prose_spans_for(
    document: Document, line_no: int, include_code: bool = False
) -> list[tuple[int, int]] | None:
    """Return the non-code spans of a line, or None when nothing is masked.

    None means every column counts as prose, which is the case for a non
    markdown document and for a caller that asked to include code. An empty
    list means the opposite: the whole line is code. Callers test both
    through `is_prose` rather than unpacking the sentinel themselves.
    """
    if include_code or not document.is_markdown:
        return None
    if line_no in document.code_lines:
        return []
    return document.code_free_spans(line_no)


def is_prose(spans: list[tuple[int, int]] | None, start: int, end: int) -> bool:
    """True when a match starting at `start` sits in prose rather than code."""
    return spans is None or starts_in((start, end), spans)


def url_spans(line: str) -> list[tuple[int, int]]:
    """Return character spans of http(s) URLs in the line."""
    return [(m.start(), m.end()) for m in URL_RE.finditer(line)]


def overlaps(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    start, end = span
    return any(start < other_end and other_start < end for other_start, other_end in spans)


def in_span_list(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    """True when the span sits entirely inside one of the given spans."""
    start, end = span
    return any(other_start <= start and end <= other_end for other_start, other_end in spans)


def starts_in(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    """True when the span begins inside one of the given spans.

    Start position rather than overlap is the right test for code masking. A
    marker quoted inside backticks is a code sample even when a greedy
    pattern runs past the closing delimiter.
    """
    start = span[0]
    return any(other_start <= start < other_end for other_start, other_end in spans)


def add_io_arguments(parser: argparse.ArgumentParser) -> None:
    """Attach the shared input and output options."""
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan. Use - or omit to read stdin.",
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text", help="Output format."
    )
    parser.add_argument(
        "--treat-as",
        choices=("auto", "markdown", "text"),
        default="auto",
        help="How to classify input for code-fence handling. Default auto by suffix.",
    )
    parser.add_argument(
        "--stdin-name", default="<stdin>", help="Label used for stdin input."
    )
    parser.add_argument(
        "--ext",
        action="append",
        default=None,
        metavar="SUFFIX",
        help="Extra file suffix to include when a directory is given. Repeatable.",
    )


def expand_paths(raw_paths: list[str], extra_ext: list[str] | None) -> list[Path]:
    """Expand directories into files, keeping explicit file paths as given."""
    suffixes = set(DEFAULT_EXTENSIONS)
    for item in extra_ext or []:
        suffixes.add(item if item.startswith(".") else "." + item)
    out: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                if any(part in SKIP_DIR_NAMES for part in child.parts):
                    continue
                if child.suffix.lower() in suffixes:
                    out.append(child)
            continue
        if not path.exists():
            raise UsageError(f"no such path: {raw}")
        out.append(path)
    return out


def load_documents(args: argparse.Namespace) -> list[Document]:
    """Read every requested input into a Document."""
    raw_paths = list(args.paths)
    if not raw_paths or raw_paths == ["-"]:
        text = sys.stdin.read()
        is_markdown = args.treat_as != "text"
        return [Document(args.stdin_name, text, is_markdown)]
    documents: list[Document] = []
    for path in expand_paths(raw_paths, getattr(args, "ext", None)):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise UsageError(f"cannot read {path}: {exc}") from exc
        if args.treat_as == "markdown":
            is_markdown = True
        elif args.treat_as == "text":
            is_markdown = False
        else:
            is_markdown = path.suffix.lower() in MARKDOWN_SUFFIXES
        documents.append(Document(str(path), text, is_markdown))
    return documents


def snippet_for(line: str, start: int, end: int, width: int = 60) -> str:
    """Return a trimmed one line excerpt centred on the match."""
    left = max(0, start - width // 2)
    right = min(len(line), end + width // 2)
    excerpt = line[left:right].strip()
    return re.sub(r"\s+", " ", excerpt)[:160]


def emit(
    findings: list[Finding],
    output_format: str,
    tool: str,
    inventory: dict | None = None,
    stream=None,
) -> int:
    """Print findings and return the process exit code."""
    stream = stream or sys.stdout
    if output_format == "json":
        payload = {
            "tool": tool,
            "ok": not findings,
            "count": len(findings),
            "findings": [finding.as_dict() for finding in findings],
            "authorship_verdict": None,
            "note": DISCLAIMER,
        }
        if inventory is not None:
            payload["inventory"] = inventory
        print(json.dumps(payload, indent=2, sort_keys=True), file=stream)
    else:
        for finding in sorted(findings, key=lambda f: (f.path, f.line, f.column, f.rule)):
            print(
                f"{finding.path}:{finding.line}:{finding.column}: "
                f"[{finding.rule}] {finding.severity}: {finding.message}"
                f"  ::  {finding.snippet}",
                file=stream,
            )
        if findings:
            print(f"\nFAIL: {tool} found {len(findings)} mechanical defect(s).", file=stream)
        else:
            print(f"OK: {tool} found no mechanical defects.", file=stream)
        print(f"NOTE: {DISCLAIMER}", file=stream)
    return EXIT_FINDINGS if findings else EXIT_CLEAN


def run_cli(main_function, argv: list[str] | None = None) -> int:
    """Run a scanner main and map UsageError to exit code 2."""
    try:
        return main_function(argv)
    except UsageError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_CLEAN
