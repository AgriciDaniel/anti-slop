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

1. The three forbidden prose characters, delegated in full to the already
   tested `lint_prose.py` shipped in claude-blog 2.1.0: U+2014, U+2013, and
   ASCII space-hyphen-hyphen-space. That module already solves fence
   awareness and backtick awareness, so this tool wraps it rather than
   reimplementing it. Locate it with `--lint-prose`, the
   ANTI_SLOP_LINT_PROSE environment variable, or plugin cache discovery.
2. Optional banned tokens from a voice file, one token per line, `#` starts
   a comment. Tokens are matched through the same fence-aware and
   backtick-aware machinery: the token is substituted for a sentinel
   character in a scratch copy and `lint_prose.lint_file` does the walking,
   so there is exactly one implementation of the masking rules.

Quoted source protection: lines that are markdown blockquotes are exempt by
default. You do not edit punctuation inside somebody else's sentence, so an
en dash in a quoted date range, or an em dash in a quoted citation, is not
a violation. Pass `--include-quotes` to lint them anyway.

Usage:
    python3 scripts/lint_voice.py [PATH ...] [--voice voice.txt]
    cat draft.md | python3 scripts/lint_voice.py --stdin-name draft.md

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import sys
import tempfile
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import (  # noqa: E402
    Finding,
    UsageError,
    emit,
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

SENTINEL = "\u2014"  # reuse the wrapped linter's own forbidden character

RULE_IDS = {
    "\u2014": "voice.em_dash",
    "\u2013": "voice.en_dash",
    "\x20--\x20": "voice.double_hyphen",
}

DISCOVERY_GLOBS = (
    ".claude/plugins/cache/*/claude-blog/*/scripts/lint_prose.py",
    ".claude/plugins/*/claude-blog/*/scripts/lint_prose.py",
    ".claude/plugins/cache/*/*/*/scripts/lint_prose.py",
)

BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>")


def version_key(path: Path) -> tuple:
    """Sort key that prefers the highest claude-blog version directory."""
    for part in reversed(path.parts):
        pieces = part.split(".")
        if len(pieces) >= 2 and all(piece.isdigit() for piece in pieces):
            return tuple(int(piece) for piece in pieces)
    return (0,)


def discover_lint_prose(explicit: str | None) -> Path:
    """Find the claude-blog lint_prose.py that this linter wraps."""
    candidates: list[Path] = []
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise UsageError(f"--lint-prose path does not exist: {path}")
        return path
    from_env = os.environ.get("ANTI_SLOP_LINT_PROSE")
    if from_env:
        path = Path(from_env).expanduser()
        if not path.is_file():
            raise UsageError(f"ANTI_SLOP_LINT_PROSE does not exist: {path}")
        return path
    home = Path.home()
    for pattern in DISCOVERY_GLOBS:
        candidates.extend(sorted(home.glob(pattern)))
    candidates = [path for path in candidates if path.is_file()]
    if not candidates:
        raise UsageError(
            "cannot find claude-blog lint_prose.py. Pass --lint-prose PATH or set "
            "ANTI_SLOP_LINT_PROSE. This linter wraps that module on purpose and "
            "does not reimplement its fence handling."
        )
    return sorted(candidates, key=version_key)[-1]


def load_lint_prose(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("anti_slop_lint_prose", path)
    if spec is None or spec.loader is None:
        raise UsageError(f"cannot import lint_prose from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for required in ("lint_file", "FORBIDDEN"):
        if not hasattr(module, required):
            raise UsageError(f"{path} does not expose {required}; wrong module?")
    return module


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
    escaped = re.escape(token)
    left = r"\b" if token[:1].isalnum() else ""
    right = r"\b" if token[-1:].isalnum() else ""
    return re.compile(left + escaped + right, re.IGNORECASE)


def neutralize(text: str) -> str:
    """Remove the wrapped linter's own forbidden sequences, preserving length."""
    text = text.replace("\u2014", " ").replace("\u2013", " ")
    return text.replace("\x20--\x20", "\x20\x20\x20\x20")


class Target:
    """One document to lint, materialised on disk for the wrapped module."""

    def __init__(self, label: str, text: str, path: Path) -> None:
        self.label = label
        self.text = text
        self.path = path
        self.lines = text.splitlines()


def collect_targets(paths: list[str], stdin_name: str, workdir: Path) -> list[Target]:
    targets: list[Target] = []
    if not paths or paths == ["-"]:
        text = sys.stdin.read()
        scratch = workdir / "stdin.md"
        scratch.write_text(text, encoding="utf-8")
        return [Target(stdin_name, text, scratch)]
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in {".md", ".markdown", ".py", ".txt"}:
                    targets.append(
                        Target(str(child), child.read_text(encoding="utf-8", errors="replace"), child)
                    )
            continue
        if not path.is_file():
            raise UsageError(f"no such path: {raw}")
        targets.append(Target(str(path), path.read_text(encoding="utf-8", errors="replace"), path))
    return targets


def lint_target(
    target: Target,
    lint_prose: ModuleType,
    tokens: list[str],
    workdir: Path,
    include_quotes: bool,
) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    exempt = 0
    for line_no, char, description, text in lint_prose.lint_file(target.path):
        if not include_quotes and BLOCKQUOTE_RE.match(text):
            exempt += 1
            continue
        column = text.find(char) + 1 if char in text else 1
        findings.append(
            Finding(
                path=target.label,
                line=line_no,
                column=max(1, column),
                rule=RULE_IDS.get(char, "voice.forbidden_character"),
                message=f"house style forbids {description}",
                snippet=snippet_for(text, max(0, column - 1), column + 1),
                severity="house-style",
            )
        )
    for index, token in enumerate(tokens):
        pattern = token_pattern(token)
        transformed = pattern.sub(SENTINEL, neutralize(target.text))
        if transformed == neutralize(target.text):
            continue
        scratch = workdir / f"token-{index}{target.path.suffix or '.md'}"
        scratch.write_text(transformed, encoding="utf-8")
        for line_no, _char, _description, _text in lint_prose.lint_file(scratch):
            original = target.lines[line_no - 1] if line_no <= len(target.lines) else ""
            if not include_quotes and BLOCKQUOTE_RE.match(original):
                exempt += 1
                continue
            match = pattern.search(original)
            start = match.start() if match else 0
            end = match.end() if match else len(original)
            findings.append(
                Finding(
                    path=target.label,
                    line=line_no,
                    column=start + 1,
                    rule="voice.banned_token",
                    message=f"house style banned token: {token}",
                    snippet=snippet_for(original, start, end),
                    severity="house-style",
                )
            )
    return findings, exempt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lint_voice.py",
        description="House style linter. Wraps claude-blog lint_prose.py. Not a slop verdict.",
    )
    parser.add_argument("paths", nargs="*", help="Files or directories. Use - or omit for stdin.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--voice", default=None, help="Voice file of banned tokens.")
    parser.add_argument("--lint-prose", default=None, help="Path to claude-blog lint_prose.py.")
    parser.add_argument("--stdin-name", default="<stdin>")
    parser.add_argument(
        "--include-quotes", action="store_true",
        help="Also lint markdown blockquote lines. Off by default: quoted source text "
             "is not yours to restyle.",
    )
    args = parser.parse_args(argv)

    lint_prose_path = discover_lint_prose(args.lint_prose)
    lint_prose = load_lint_prose(lint_prose_path)
    tokens = load_voice_tokens(Path(args.voice) if args.voice else None)

    findings: list[Finding] = []
    exempt_total = 0
    with tempfile.TemporaryDirectory(prefix="lint-voice-") as tmp:
        workdir = Path(tmp)
        for target in collect_targets(args.paths, args.stdin_name, workdir):
            target_findings, exempt = lint_target(
                target, lint_prose, tokens, workdir, args.include_quotes
            )
            findings.extend(target_findings)
            exempt_total += exempt

    inventory = {
        "rule_class": "house-style",
        "authorship_signal": False,
        "slop_verdict": False,
        "statement": HOUSE_STYLE_NOTE,
        "wrapped_module": str(lint_prose_path),
        "banned_tokens": tokens,
        "quoted_lines_exempt": exempt_total,
    }
    if args.format == "text":
        print(HOUSE_STYLE_NOTE)
        print(f"wrapped: {lint_prose_path}")
        if exempt_total:
            print(f"exempt: {exempt_total} finding(s) inside quoted source lines were not reported.")
    exit_code = emit(findings, args.format, TOOL, inventory=inventory)
    if args.format == "text":
        print(HOUSE_STYLE_NOTE)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
