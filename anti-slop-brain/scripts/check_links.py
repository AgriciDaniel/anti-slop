#!/usr/bin/env python3
"""Dead wikilink check for the shipped vault.

`lint_vault.py` validates a distributable client vault and expects a client
vault's furniture: CODEX.md, shipping-rules.md, a .raw manifest. Pointing it at
the repository-root wiki reports those as errors even though the repository
root is not a client vault, which buries the one finding that does matter.

This script checks the thing that matters and nothing else: every `[[target]]`
in the vault resolves to a note that exists.

An adversarial pass on 2026-07-28 found 36 dead wikilinks in the shipped vault
that no build step was checking, because the only link check in the repository
ran against `assets/template-brain` instead. This exists so that cannot recur.

Exit codes: 0 clean, 1 dead links found, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]\|#]+)")


def note_names(vault: Path) -> set[str]:
    return {p.stem for p in vault.rglob("*.md")}


def target_of(raw: str) -> str:
    """Normalise a link target the way Obsidian resolves it."""
    target = raw.strip()
    if "/" in target:
        target = target.split("/")[-1]
    if target.endswith(".md"):
        target = target[:-3]
    return target


def find_dead(vault: Path) -> tuple[Counter[str], list[tuple[Path, int, str]]]:
    names = note_names(vault)
    counts: Counter[str] = Counter()
    where: list[tuple[Path, int, str]] = []
    for path in sorted(vault.rglob("*.md")):
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            for match in WIKILINK.finditer(line):
                target = target_of(match.group(1))
                if target and target not in names:
                    counts[target] += 1
                    where.append((path, lineno, target))
    return counts, where


def find_self_links(vault: Path) -> list[tuple[Path, str]]:
    """A note that links to itself is noise, not navigation."""
    found = []
    for path in sorted(vault.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in WIKILINK.finditer(text):
            if target_of(match.group(1)) == path.stem:
                found.append((path, path.stem))
                break
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that every wikilink in a vault resolves.",
        epilog="Example: python3 scripts/check_links.py --vault wiki",
    )
    parser.add_argument("--vault", required=True, help="Directory holding the notes.")
    parser.add_argument(
        "--allow-self-links",
        action="store_true",
        help="Do not fail on notes that link to themselves.",
    )
    args = parser.parse_args(argv)

    vault = Path(args.vault)
    if not vault.is_dir():
        print(f"ERROR: not a directory: {vault}", file=sys.stderr)
        return 2

    notes = list(vault.rglob("*.md"))
    if not notes:
        print(f"ERROR: no markdown notes under {vault}", file=sys.stderr)
        return 2

    counts, where = find_dead(vault)
    self_links = [] if args.allow_self_links else find_self_links(vault)

    if not counts and not self_links:
        print(f"OK: {len(notes)} notes, every wikilink resolves.")
        return 0

    if counts:
        total = sum(counts.values())
        print(f"FAIL: {total} dead wikilinks across {len(counts)} distinct targets.")
        for target, count in counts.most_common():
            print(f"  {count:4d}  {target}")
        print()
        for path, lineno, target in where[:20]:
            print(f"  {path}:{lineno}: [[{target}]]")
        if len(where) > 20:
            print(f"  ... and {len(where) - 20} more")

    if self_links:
        print(f"FAIL: {len(self_links)} notes link to themselves.")
        for path, stem in self_links:
            print(f"  {path}: [[{stem}]]")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
