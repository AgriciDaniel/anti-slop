#!/usr/bin/env python3
"""Layer 0 scanner: wiki substance scoring for a note vault.

Origin and credit. This is a port of the wiki substance scorer written for
Claude Blog Brain, `scripts/audit_brain.py`, functions `check_wiki_substance`
and `score_wiki_substance` plus their helpers `load_source_index`,
`load_spoke_notes`, `find_near_duplicate_pairs`, `largest_reuse_group`,
`largest_anchor_reuse`, `largest_bundle`, `shared_body_lines`,
`note_specific_word_count` and `compile_source_id_pattern`. The thresholds,
the shingle size, the scoring weights and the citation-bundle reasoning are
carried over unchanged. What is new here is that it stands alone: it takes
a vault path and a ledger path instead of assuming one repository layout.

What it measures, all mechanically:

- Near duplicate note pairs, by 8 token shingle Jaccard similarity at 0.82.
- Heading skeleton reuse: how many notes share an identical H2/H3 outline.
- Anchor line reuse: how many notes repeat the same long line verbatim.
- Table or procedure coverage: the share of notes that contain a real table
  or a numbered procedure of at least three steps.
- Specific citation coverage: the share of notes citing at least two ledger
  sources without pasting the same oversized citation bundle everywhere.
- Note-specific word density: words on lines that appear in this note only.

Why this belongs in Layer 0: every one of those is a counting operation on
the text. None of them asks whether the writing is good, and none of them
asks who wrote it. A vault that pads notes to hit a line floor fails these
counts, which is the point.

Note types are not guessable, so they are not guessed. `--note-type` defaults
to `spoke`, which is the type the original scorer was written against. A vault
that uses other types must name them. If the filter selects nothing while the
vault does hold typed notes, this is a bad invocation and it exits 2 naming the
types actually present. A score of zero means measured and bad; it never means
the wrong flag was passed.

Usage:
    python3 scripts/score_substance.py --vault wiki \
        --ledger references/source-ledger.json \
        --note-type concept,marker,procedure,surface
    python3 scripts/score_substance.py --vault wiki \
        --note-type concept,marker,procedure,surface --format json

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import DISCLAIMER, UsageError, run_cli  # noqa: E402

TOOL = "score_substance"

SHINGLE_SIZE = 8
NEAR_DUPLICATE_THRESHOLD = 0.82
SKELETON_REUSE_THRESHOLD = 3
ANCHOR_REUSE_THRESHOLD = 2
TABLE_OR_PROCEDURE_THRESHOLD = 0.90
SPECIFIC_CITATION_THRESHOLD = 0.95
GENERIC_BUNDLE_REUSE_THRESHOLD = 3
GENERIC_BUNDLE_SOURCE_MIN = 6
DENSITY_WORD_THRESHOLD = 120

URL_RE = re.compile(r"https?://[^\s<>\]\"')]+")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)


def clean_string(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def canonical_source_url(value: str) -> str:
    if not value:
        return ""
    cleaned = value.strip().strip("<>\"'").rstrip(".,;:")
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    parsed = parsed._replace(netloc=parsed.netloc.lower(), fragment="")
    return parsed.geturl().rstrip("/")


def load_source_index(ledger_path: Path | None) -> tuple[set[str], dict[str, tuple[str, ...]]]:
    """Read source ids and canonical urls from a v1 style source ledger."""
    source_ids: set[str] = set()
    url_to_source_ids: dict[str, list[str]] = defaultdict(list)
    if ledger_path is None:
        return source_ids, {}
    if not ledger_path.exists():
        raise UsageError(f"no such ledger file: {ledger_path}")
    try:
        data = json.loads(ledger_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise UsageError(f"ledger is not valid JSON: {exc}") from exc
    sources = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(sources, list):
        return source_ids, {}
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = clean_string(source.get("id")) or clean_string(source.get("source_id"))
        if not source_id:
            continue
        source_ids.add(source_id)
        url = canonical_source_url(clean_string(source.get("url")))
        if url and source_id not in url_to_source_ids[url]:
            url_to_source_ids[url].append(source_id)
    return source_ids, {url: tuple(ids) for url, ids in url_to_source_ids.items()}


def compile_source_id_pattern(source_ids: set[str]) -> re.Pattern[str] | None:
    if not source_ids:
        return None
    alternatives = "|".join(
        re.escape(source_id) for source_id in sorted(source_ids, key=len, reverse=True)
    )
    return re.compile(r"(?<![A-Za-z0-9_-])(" + alternatives + r")(?![A-Za-z0-9_-])")


def split_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def frontmatter_type(frontmatter: str) -> str:
    match = re.search(r"(?m)^type:\s*[\"']?([^\"'\n#]+)[\"']?", frontmatter)
    return match.group(1).strip().lower() if match else ""


def normalize_body(body: str) -> str:
    return collapse_whitespace(body.lower())


def stable_shingle_hash(tokens: list[str]) -> int:
    digest = hashlib.blake2b(" ".join(tokens).encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def make_shingles(tokens: list[str], size: int = SHINGLE_SIZE) -> frozenset[int]:
    if not tokens:
        return frozenset()
    if len(tokens) < size:
        return frozenset({stable_shingle_hash(tokens)})
    return frozenset(
        stable_shingle_hash(tokens[index:index + size])
        for index in range(len(tokens) - size + 1)
    )


def heading_skeleton(body: str) -> tuple[str, ...]:
    headings = []
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}(#{2,3})\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1) + " " + collapse_whitespace(match.group(2)).lower())
    return tuple(headings)


def has_table_or_procedure(body: str) -> bool:
    lines = body.splitlines()
    for index, line in enumerate(lines[:-1]):
        if "|" in line and re.match(
            r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[index + 1]
        ):
            return True
    step_count = 0
    for line in lines:
        if re.match(r"^\s*(?:\d+[\.)]|step\s+\d+\b)\s+", line, re.I):
            step_count += 1
            if step_count >= 3:
                return True
    return False


def extract_source_ids(
    text: str,
    source_id_pattern: re.Pattern[str] | None,
    url_to_source_ids: dict[str, tuple[str, ...]],
) -> set[str]:
    found: set[str] = set()
    if source_id_pattern:
        found.update(source_id_pattern.findall(text))
    for match in URL_RE.finditer(text):
        source_ids = url_to_source_ids.get(canonical_source_url(match.group(0)))
        if not source_ids:
            continue
        if any(source_id in found for source_id in source_ids):
            continue
        found.add(source_ids[0])
    return found


def load_spoke_notes(
    vault_root: Path,
    source_id_pattern: re.Pattern[str] | None,
    url_to_source_ids: dict[str, tuple[str, ...]],
    note_type: str | frozenset[str],
) -> list[dict[str, Any]]:
    spoke_notes: list[dict[str, Any]] = []
    for path in sorted(vault_root.rglob("*.md")):
        if path.name == "_index.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = split_frontmatter(text)
        wanted = {note_type} if isinstance(note_type, str) else note_type
        if frontmatter_type(frontmatter) not in wanted:
            continue
        body_lines = [collapse_whitespace(line) for line in body.splitlines()]
        normalized = normalize_body(body)
        tokens = normalized.split()
        citation_set = frozenset(extract_source_ids(text, source_id_pattern, url_to_source_ids))
        spoke_notes.append(
            {
                "path": path,
                "rel_path": display_path(path, vault_root),
                "body": body,
                "body_lines": body_lines,
                "normalized_body": normalized,
                "tokens": tokens,
                "shingles": make_shingles(tokens),
                "skeleton": heading_skeleton(body),
                "has_table_or_procedure": has_table_or_procedure(body),
                "citation_set": citation_set,
            }
        )
    return spoke_notes


def present_note_types(vault_root: Path) -> list[str]:
    """Return every frontmatter type value that actually occurs in the vault."""
    found: set[str] = set()
    for path in sorted(vault_root.rglob("*.md")):
        if path.name == "_index.md":
            continue
        frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        note_type = frontmatter_type(frontmatter)
        if note_type:
            found.add(note_type)
    return sorted(found)


def find_near_duplicate_pairs(spoke_notes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inverted: dict[int, list[int]] = defaultdict(list)
    for index, note in enumerate(spoke_notes):
        for shingle in note["shingles"]:
            inverted[shingle].append(index)

    intersections: Counter[tuple[int, int]] = Counter()
    for indexes in inverted.values():
        if len(indexes) < 2:
            continue
        for left_pos, left in enumerate(indexes):
            for right in indexes[left_pos + 1:]:
                intersections[(left, right)] += 1

    pairs = []
    for (left, right), intersection in intersections.items():
        left_shingles = spoke_notes[left]["shingles"]
        right_shingles = spoke_notes[right]["shingles"]
        union = len(left_shingles) + len(right_shingles) - intersection
        similarity = 1.0 if union == 0 else intersection / union
        if similarity >= NEAR_DUPLICATE_THRESHOLD:
            pairs.append(
                {
                    "paths": [spoke_notes[left]["rel_path"], spoke_notes[right]["rel_path"]],
                    "similarity": round(similarity, 4),
                }
            )
    return sorted(pairs, key=lambda item: (-item["similarity"], item["paths"]))


def largest_reuse_group(spoke_notes: list[dict[str, Any]], key: str) -> dict[str, Any]:
    groups: dict[Any, list[str]] = defaultdict(list)
    for note in spoke_notes:
        groups[note[key]].append(note["rel_path"])
    candidates = list(groups.items())
    if not candidates:
        return {}
    value, paths = max(candidates, key=lambda item: (len(item[1]), sorted(item[1])[0]))
    return {"count": len(paths), "value": list(value), "paths": sorted(paths)}


def largest_anchor_reuse(spoke_notes: list[dict[str, Any]]) -> dict[str, Any]:
    anchors: dict[str, list[str]] = defaultdict(list)
    for note in spoke_notes:
        seen_in_note = set()
        for line in note["body_lines"]:
            if line and len(WORD_RE.findall(line)) >= 12:
                seen_in_note.add(line)
        for line in seen_in_note:
            anchors[line].append(note["rel_path"])
    candidates = list(anchors.items())
    if not candidates:
        return {}
    line, paths = max(candidates, key=lambda item: (len(item[1]), item[0]))
    return {"count": len(paths), "line": line, "paths": sorted(paths)}


def largest_bundle(bundle_counts: Counter[frozenset[str]]) -> tuple[frozenset[str], int]:
    if not bundle_counts:
        return frozenset(), 0
    bundle, count = max(
        bundle_counts.items(), key=lambda item: (item[1], len(item[0]), sorted(item[0]))
    )
    return bundle, count


def shared_body_lines(spoke_notes: list[dict[str, Any]]) -> set[str]:
    counts: Counter[str] = Counter()
    for note in spoke_notes:
        counts.update({line for line in note["body_lines"] if line})
    return {line for line, count in counts.items() if count > 1}


def note_specific_word_count(body_lines: list[str], shared_lines: set[str]) -> int:
    specific_lines = [line for line in body_lines if line and line not in shared_lines]
    return len(WORD_RE.findall("\n".join(specific_lines)))


def score_wiki_substance(metrics: dict[str, Any], spoke_count: int) -> int:
    if spoke_count <= 0:
        return 0
    score = 100.0
    if metrics["max_skeleton_reuse"] > SKELETON_REUSE_THRESHOLD:
        overage = metrics["max_skeleton_reuse"] - SKELETON_REUSE_THRESHOLD
        score -= 10.0 * min(1.0, overage / max(1, spoke_count - SKELETON_REUSE_THRESHOLD))
    if metrics["max_anchor_reuse"] > ANCHOR_REUSE_THRESHOLD:
        overage = metrics["max_anchor_reuse"] - ANCHOR_REUSE_THRESHOLD
        score -= 10.0 * min(1.0, overage / max(1, spoke_count - ANCHOR_REUSE_THRESHOLD))
    if metrics["generic_bundle_reuse"] > GENERIC_BUNDLE_REUSE_THRESHOLD:
        overage = metrics["generic_bundle_reuse"] - GENERIC_BUNDLE_REUSE_THRESHOLD
        score -= 10.0 * min(1.0, overage / max(1, spoke_count - GENERIC_BUNDLE_REUSE_THRESHOLD))
    if metrics["table_or_procedure_coverage"] < TABLE_OR_PROCEDURE_THRESHOLD:
        shortfall = TABLE_OR_PROCEDURE_THRESHOLD - metrics["table_or_procedure_coverage"]
        score -= 15.0 * min(1.0, shortfall / TABLE_OR_PROCEDURE_THRESHOLD)
    if metrics["specific_citation_coverage"] < SPECIFIC_CITATION_THRESHOLD:
        shortfall = SPECIFIC_CITATION_THRESHOLD - metrics["specific_citation_coverage"]
        score -= 20.0 * min(1.0, shortfall / SPECIFIC_CITATION_THRESHOLD)
    if metrics["density_floor_below_count"]:
        score -= 15.0 * min(1.0, metrics["density_floor_below_count"] / spoke_count)
    if metrics["near_duplicate_pairs"] > 0:
        score = min(score, 40.0)
    return round(max(0.0, min(100.0, score)))


def check_wiki_substance(
    vault_root: Path,
    ledger_path: Path | None,
    note_type: str | frozenset[str] = "spoke",
) -> dict[str, Any]:
    """Audit whether notes have real, note-specific substance.

    A note citation set is the sorted set of ledger source ids cited anywhere
    in the note, including frontmatter and body text. Topical reuse of a
    compact authoritative source set is allowed: a 2 to 5 source set can be
    correct scholarship for a folder. The boilerplate defect is an oversized
    pasted bundle, so generic bundle reuse measures the largest group of notes
    sharing an identical citation set of at least 6 sources.
    """
    if not vault_root.exists():
        raise UsageError(f"no such vault directory: {vault_root}")
    notes: list[str] = []
    critical: list[str] = []

    source_ids, url_to_source_ids = load_source_index(ledger_path)
    source_id_pattern = compile_source_id_pattern(source_ids)
    spoke_notes = load_spoke_notes(vault_root, source_id_pattern, url_to_source_ids, note_type)
    if not spoke_notes:
        wanted = sorted({note_type} if isinstance(note_type, str) else note_type)
        available = present_note_types(vault_root)
        if available:
            raise UsageError(
                "--note-type "
                + ",".join(wanted)
                + f" matched no notes under {vault_root}, but the vault does contain "
                + f"typed notes. Types present: {', '.join(available)}. "
                + "Rerun with --note-type "
                + ",".join(available)
                + ". A score is only reported for a population that was measured."
            )
        return {
            "ok": False,
            "score": 0,
            "notes": [f"no typed notes at all found under {vault_root}"],
            "critical": [],
            "metrics": {},
            "offenders": {},
        }

    near_pairs = find_near_duplicate_pairs(spoke_notes)
    skeleton = largest_reuse_group(spoke_notes, "skeleton")
    anchor = largest_anchor_reuse(spoke_notes)
    table_or_procedure_failures = [
        note["rel_path"] for note in spoke_notes if not note["has_table_or_procedure"]
    ]

    citation_set_counts: Counter[frozenset[str]] = Counter(
        note["citation_set"] for note in spoke_notes
    )
    bundle_counts: Counter[frozenset[str]] = Counter(
        note["citation_set"]
        for note in spoke_notes
        if len(note["citation_set"]) >= GENERIC_BUNDLE_SOURCE_MIN
    )
    generic_bundle, generic_bundle_count = largest_bundle(bundle_counts)
    identically_reused_sets = {
        citation_set
        for citation_set, count in citation_set_counts.items()
        if (
            len(citation_set) >= GENERIC_BUNDLE_SOURCE_MIN
            and count > GENERIC_BUNDLE_REUSE_THRESHOLD
        )
    }
    citation_failures = [
        note["rel_path"]
        for note in spoke_notes
        if len(note["citation_set"]) < 2 or note["citation_set"] in identically_reused_sets
    ]

    shared_lines = shared_body_lines(spoke_notes)
    density_failures = []
    density_values: dict[str, int] = {}
    for note in spoke_notes:
        count = note_specific_word_count(note["body_lines"], shared_lines)
        density_values[note["rel_path"]] = count
        if count < DENSITY_WORD_THRESHOLD:
            density_failures.append({"path": note["rel_path"], "note_specific_words": count})

    table_or_procedure_coverage = 1.0 - (len(table_or_procedure_failures) / len(spoke_notes))
    specific_citation_coverage = 1.0 - (len(citation_failures) / len(spoke_notes))
    density_floor = min(density_values.values()) if density_values else 0
    max_skeleton_reuse = skeleton["count"] if skeleton else 0
    max_anchor_reuse = anchor["count"] if anchor else 0

    metrics = {
        "spoke_count": len(spoke_notes),
        "near_duplicate_pairs": len(near_pairs),
        "max_skeleton_reuse": max_skeleton_reuse,
        "max_anchor_reuse": max_anchor_reuse,
        "table_or_procedure_coverage": round(table_or_procedure_coverage, 4),
        "specific_citation_coverage": round(specific_citation_coverage, 4),
        "generic_bundle_reuse": generic_bundle_count,
        "density_floor": density_floor,
        "density_floor_below_count": len(density_failures),
    }
    offenders = {
        "near_duplicate_pairs": near_pairs,
        "max_skeleton_reuse": skeleton if max_skeleton_reuse > SKELETON_REUSE_THRESHOLD else {},
        "max_anchor_reuse": anchor if max_anchor_reuse > ANCHOR_REUSE_THRESHOLD else {},
        "table_or_procedure_coverage": table_or_procedure_failures,
        "specific_citation_coverage": citation_failures,
        "generic_bundle_reuse": {
            "count": generic_bundle_count,
            "source_ids": sorted(generic_bundle),
            "paths": [
                note["rel_path"] for note in spoke_notes if note["citation_set"] == generic_bundle
            ] if generic_bundle_count > GENERIC_BUNDLE_REUSE_THRESHOLD else [],
        },
        "density_floor": density_failures,
    }

    if near_pairs:
        first = near_pairs[0]["paths"]
        critical.append(
            f"near_duplicate_pairs={len(near_pairs)}: {first[0]} and {first[1]}"
        )
        notes.append(f"near duplicate note pairs: {len(near_pairs)}")
    if max_skeleton_reuse > SKELETON_REUSE_THRESHOLD:
        notes.append(f"H2/H3 skeleton reused by {max_skeleton_reuse} notes")
    if max_anchor_reuse > ANCHOR_REUSE_THRESHOLD:
        notes.append(f"anchor line reused by {max_anchor_reuse} notes")
    if table_or_procedure_coverage < TABLE_OR_PROCEDURE_THRESHOLD:
        notes.append(
            f"table/procedure coverage {table_or_procedure_coverage:.2f} below "
            f"{TABLE_OR_PROCEDURE_THRESHOLD:.2f}"
        )
    if specific_citation_coverage < SPECIFIC_CITATION_THRESHOLD:
        notes.append(
            f"specific citation coverage {specific_citation_coverage:.2f} below "
            f"{SPECIFIC_CITATION_THRESHOLD:.2f}"
        )
    if generic_bundle_count > GENERIC_BUNDLE_REUSE_THRESHOLD:
        notes.append(f"generic source bundle reused by {generic_bundle_count} notes")
    if density_failures:
        notes.append(
            f"{len(density_failures)} notes below {DENSITY_WORD_THRESHOLD} note-specific words"
        )

    ok = (
        len(near_pairs) == 0
        and max_skeleton_reuse <= SKELETON_REUSE_THRESHOLD
        and max_anchor_reuse <= ANCHOR_REUSE_THRESHOLD
        and table_or_procedure_coverage >= TABLE_OR_PROCEDURE_THRESHOLD
        and specific_citation_coverage >= SPECIFIC_CITATION_THRESHOLD
        and generic_bundle_count <= GENERIC_BUNDLE_REUSE_THRESHOLD
        and not density_failures
    )
    return {
        "ok": ok,
        "score": score_wiki_substance(metrics, len(spoke_notes)),
        "notes": notes,
        "critical": critical,
        "metrics": metrics,
        "offenders": offenders,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="score_substance.py",
        description="Score a note vault for note-specific substance. Ported from "
                    "Claude Blog Brain scripts/audit_brain.py.",
    )
    parser.add_argument("--vault", required=True, help="Directory holding the notes.")
    parser.add_argument("--ledger", default=None, help="Path to a source ledger JSON file.")
    parser.add_argument(
        "--note-type",
        default="spoke",
        help=(
            "Comma separated frontmatter type: values to score. Default spoke. "
            "A vault that splits content across several types, for example "
            "concept,marker,procedure,surface, must name them all. If the filter "
            "selects nothing while the vault does hold typed notes, this exits 2 "
            "and names the types present rather than reporting a score of zero."
        ),
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    ledger_path = Path(args.ledger) if args.ledger else None
    note_types = frozenset(
        part.strip().lower() for part in args.note_type.split(",") if part.strip()
    )
    result = check_wiki_substance(Path(args.vault), ledger_path, note_types)

    if args.format == "json":
        payload = dict(result)
        payload["tool"] = TOOL
        payload["authorship_verdict"] = None
        payload["note"] = DISCLAIMER
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"substance score: {result['score']}")
        for key, value in sorted(result["metrics"].items()):
            print(f"  {key}: {value}")
        for item in result["critical"]:
            print(f"CRITICAL: {item}")
        for item in result["notes"]:
            print(f"FINDING: {item}")
        for pair in result["offenders"].get("near_duplicate_pairs", [])[:10]:
            print(f"  near duplicate {pair['similarity']}: {pair['paths'][0]} and {pair['paths'][1]}")
        for entry in result["offenders"].get("density_floor", [])[:10]:
            print(f"  thin note: {entry['path']} has {entry['note_specific_words']} specific words")
        if result["ok"]:
            print(f"OK: {TOOL} found no substance defects.")
        else:
            print(f"FAIL: {TOOL} found substance defects.")
        print(f"NOTE: {DISCLAIMER}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
