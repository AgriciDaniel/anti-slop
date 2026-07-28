#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reference_date import (  # noqa: E402
    ReferenceDateError,
    add_reference_date_argument,
    resolve_reference_date,
)


REPO = Path(__file__).resolve().parent.parent
DOMAIN = "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
DOMAIN_SLUG = "detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
CONFIDENCE_LEVELS = {"evidence-based", "practitioner", "contested", "folklore"}
CONFIDENCE_ALIASES = {
    "high": "evidence-based",
    "med": "practitioner",
    "medium": "practitioner",
    "low": "contested",
    "evidence": "evidence-based",
    "evidence based": "evidence-based",
}
SPINE_RELATED = [
    "[[Index]]",
    "[[Dashboard]]",
    "[[CONVENTIONS]]",
    "[[Tag Taxonomy]]",
    "[[Source Intake Workflow]]",
    "[[Research Refresh Workflow]]",
    "[[Claim Verification Flow]]",
    "[[Synthesis Workflow]]",
    "[[Reporting Workflow]]",
    "[[Source Manifest Guide]]",
    "[[Best Practices Kernel]]",
    "[[Health Scorecard]]",
    "[[Action Roadmap]]",
    "[[Weekly Report]]",
    "[[Approval Queue]]",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthesize source-cited starter deliverables.")
    parser.add_argument("--vault", required=True)
    parser.add_argument(
        "--canon-dir",
        default=None,
        help="Where to write the folded canon reference layer. Defaults to this "
             "repository's references/canon. Point it at a scratch directory when "
             "synthesizing a throwaway vault, so the run leaves the repository alone.",
    )
    add_reference_date_argument(parser)
    args = parser.parse_args(argv)
    try:
        stamp = resolve_reference_date(args.reference_date).isoformat()
    except ReferenceDateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    canon_dir = Path(args.canon_dir).expanduser().resolve() if args.canon_dir else REPO / "references" / "canon"
    vault = Path(args.vault).expanduser().resolve()
    manifest_path = vault / ".raw" / ".manifest.json"
    if not manifest_path.exists():
        print("ERROR: missing .raw/.manifest.json; run scaffold and ingest first", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = manifest.get("sources", [])
    source_rows = "\n".join(f"| `{item.get('path', '')}` | `{item.get('sha256', '')[:12]}` | {item.get('retrieved', '')} |" for item in sources) or "| No sources yet |  |  |"
    write(vault / "wiki" / "deliverables" / "Health Scorecard.md", f"""---
type: "deliverable"
title: "Health Scorecard"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "draft"
created: "{stamp}"
updated: "{stamp}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/deliverable"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Action Roadmap]]"
  - "[[Weekly Report]]"
  - "[[Source Manifest Guide]]"
  - "[[Dashboard]]"
source_urls: []
---

# Health Scorecard

## Source Coverage

| Source | Hash | Retrieved |
|---|---|---:|
{source_rows}

## Current Read

This is a source-cited scaffold. Domain-specific conclusions remain blocked
until current trustworthy research is captured in `references/`.

Related: [[Action Roadmap]] | [[Weekly Report]] | [[Source Manifest Guide]]
""")
    write(vault / "wiki" / "deliverables" / "Action Roadmap.md", f"""---
type: "deliverable"
title: "Action Roadmap"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "draft"
created: "{stamp}"
updated: "{stamp}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/deliverable"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Approval Queue]]"
  - "[[Health Scorecard]]"
  - "[[Best Practices Kernel]]"
  - "[[Dashboard]]"
source_urls: []
---

# Action Roadmap

## Immediate Actions

1. Complete source intake.
2. Refresh official/current requirements.
3. Replace scaffold claims with sourced domain notes.

## Approval Gate

Every action requires source, confidence, owner, approval status, and rollback.

Related: [[Approval Queue]] | [[Health Scorecard]] | [[Best Practices Kernel]]
""")
    write(vault / "wiki" / "reports" / "Weekly Report.md", f"""---
type: "report"
title: "Weekly Report"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "draft"
created: "{stamp}"
updated: "{stamp}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/report"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Reporting Workflow]]"
  - "[[Approval Queue]]"
  - "[[Health Scorecard]]"
  - "[[Action Roadmap]]"
source_urls: []
---

# Weekly Report

## Summary

Anti-Slop Brain is ready for source review. It has {len(sources)} raw source(s) in
the manifest.

## Evidence

- [[Health Scorecard]]
- [[Action Roadmap]]
- [[Source Manifest Guide]]

Related: [[Reporting Workflow]] | [[Approval Queue]]
""")
    folded_sources = fold_source_ledger(vault, stamp, canon_dir)
    folded_adapters = fold_adapter_manifest(vault, stamp)
    message = "Synthesized source-cited starter deliverables."
    if folded_sources:
        message += f" Folded {folded_sources} source-ledger canon entr{'y' if folded_sources == 1 else 'ies'}."
    if folded_adapters:
        message += f" Folded {folded_adapters} adapter manifest entr{'y' if folded_adapters == 1 else 'ies'}."
    append_log(vault, message, stamp)
    print("Synthesis complete")
    return 0


def fold_source_ledger(vault: Path, stamp: str, canon_dir: Path) -> int:
    ledger = load_json_object(REPO / "references" / "source-ledger.json") or load_json_object(vault / "references" / "source-ledger.json")
    if not ledger:
        return 0
    sources = ledger.get("sources")
    if not isinstance(sources, list):
        return 0
    real_sources = [item for item in sources if is_real_captured_source(item)]
    if not real_sources:
        return 0

    canon_dir.mkdir(parents=True, exist_ok=True)
    for path in canon_dir.glob("*.md"):
        if path.name != "_index.md":
            path.unlink()

    index_rows = []
    for index, source in enumerate(real_sources, start=1):
        title = safe_note_name(str(source.get("title", "")).strip(), f"Source {index:03d}")
        url = str(source.get("url", "")).strip()
        level = confidence_level(source.get("confidence", "medium"))
        canon_name = f"{index:03d}-{safe_slug(title, f'source-{index:03d}')}.md"
        concept_title = unique_concept_title(vault, title, index)
        write(canon_dir / canon_name, canon_source_note(index, title, source, level, concept_title, stamp))
        write(vault / "wiki" / "concepts" / f"{concept_title}.md", concept_source_note(index, title, source, level, canon_name, stamp))
        index_rows.append(f"| {index:03d} | [{title}]({canon_name}) | {level} | [[{concept_title}]] | captured | {url} |")

    write(canon_dir / "_index.md", canon_source_index(index_rows, stamp))
    return len(real_sources)


def fold_adapter_manifest(vault: Path, stamp: str) -> int:
    manifest = load_json_object(REPO / "references" / "adapter-manifest.json") or load_json_object(vault / "references" / "adapter-manifest.json")
    if not manifest or manifest.get("generic_only") is True:
        return 0
    sections = [
        ("input_schemas", "platforms", "platform", "Input Schema"),
        ("importers", "platforms", "platform", "Importer"),
        ("synthesis_modules", "entities", "entity", "Synthesis Module"),
        ("report_renderers", "entities", "entity", "Report Renderer"),
        ("fixtures", "entities", "entity", "Fixture"),
        ("tests", "entities", "entity", "Test"),
    ]
    count = 0
    hub_links: dict[str, list[str]] = {}
    for section, folder, type_, label in sections:
        entries = manifest.get(section)
        if not isinstance(entries, list):
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict) or not entry:
                continue
            title = adapter_title(label, entry, index)
            note_name = safe_note_name(title, f"{label} {index}")
            body = adapter_note_body(section, label, entry)
            urls = adapter_urls(entry)
            write(vault / "wiki" / folder / f"{note_name}.md", f"""{note_frontmatter(type_, title, stamp, status="active", confidence="practitioner", related=[f"[[wiki/{folder}/_index|{folder.title()} Hub]]"], source_urls=urls)}

# {title}

{body}

## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
""")
            hub_links.setdefault(folder, []).append(f"- [[wiki/{folder}/{note_name}|{title}]]")
            count += 1
    update_adapter_hub_links(vault, hub_links)
    return count


def update_adapter_hub_links(vault: Path, hub_links: dict[str, list[str]]) -> None:
    for folder in sorted(hub_links):
        hub = vault / "wiki" / folder / "_index.md"
        if not hub.exists():
            continue
        rows = sorted(unique_items(hub_links[folder]))
        section = "\n".join([
            "## Adapter Manifest Notes",
            "",
            "These vault notes were folded from `references/adapter-manifest.json`.",
            "",
            *rows,
        ])
        text = hub.read_text(encoding="utf-8")
        pattern = r"\n## Adapter Manifest Notes\n.*?(?=\n## |\Z)"
        if re.search(pattern, text, flags=re.S):
            text = re.sub(pattern, "\n" + section, text, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + section
        hub.write_text(text.rstrip() + "\n", encoding="utf-8")


def canon_source_index(rows: list[str], stamp: str) -> str:
    return f"""---
type: "reference"
title: "Canon Reference Layer"
created: "{stamp}"
updated: "{stamp}"
status: "active"
---

# Canon Reference Layer

Purpose: hold authoritative works, standards, docs, APIs, and methods for {DOMAIN} as distilled evidence files.

This index was folded from captured entries in `references/source-ledger.json`. It does not invent sources; empty ledgers keep the scaffold seed canon.

| # | Source | Confidence | Fold | Status | URL |
|---|---|---|---|---|---|
{chr(10).join(rows)}
"""


def canon_source_note(index: int, title: str, source: dict[str, Any], level: str, concept_title: str, stamp: str) -> str:
    source_lines = claim_lines(source)
    url = str(source.get("url", "")).strip()
    retrieved = str(source.get("retrieved", "")).strip()
    refresh_due = str(source.get("refresh_due", "")).strip()
    source_type = str(source.get("source_type", "")).strip()
    return f"""{note_frontmatter("canon", f"{index:03d}. {title}", stamp, status="active", confidence=level, related=[f"[[{concept_title}]]"], source_urls=[url])}

# {index:03d}. {title}

Ledger: {index:03d} | source: {title} | confidence: {level} | fold: [[{concept_title}]] | status: captured.

## What It Says

{source_lines}

## Source

Source: [{title}]({url}){source_suffix(retrieved, refresh_due, source_type)}.

## Brain Hooks

- Folded concept: [[{concept_title}]]
- Source ledger: `references/source-ledger.json`
- Verification path: [[Claim Verification Flow]]
"""


def concept_source_note(index: int, title: str, source: dict[str, Any], level: str, canon_name: str, stamp: str) -> str:
    url = str(source.get("url", "")).strip()
    retrieved = str(source.get("retrieved", "")).strip()
    refresh_due = str(source.get("refresh_due", "")).strip()
    source_type = str(source.get("source_type", "")).strip()
    caveat = confidence_callout(level)
    return f"""{note_frontmatter("concept", title, stamp, status="active", confidence=level, related=["[[wiki/concepts/_index|Concepts Hub]]", "[[Claim Verification Flow]]"], source_urls=[url])}

# {title}

## What It Says

{claim_lines(source)}

## Source

Source: [{title}]({url}){source_suffix(retrieved, refresh_due, source_type)}.

{caveat}

## Canon Backlink

- Canon ledger entry: [references/canon/{canon_name}](../../../../references/canon/{canon_name})
- Source ledger: `references/source-ledger.json`

## Related

- [[Claim Verification Flow]]
- [[Source Intake Workflow]]
- [[Research Refresh Workflow]]
"""


def confidence_callout(level: str) -> str:
    if level == "evidence-based":
        return ""
    if level == "contested":
        return "> [!contradiction]\n> Ledger confidence is low/contested. Keep disagreement or weak support visible before using this in a deliverable."
    return "> [!gap]\n> Ledger confidence is medium/practitioner. Treat this as useful operating evidence, not settled authority, until stronger support is captured."


def claim_lines(source: dict[str, Any]) -> str:
    claims = source.get("claims")
    if isinstance(claims, list):
        rows = [str(item).strip() for item in claims if str(item).strip()]
        if rows:
            return "\n".join(f"- {item}" for item in rows)
    for key in ("claim", "summary"):
        value = str(source.get(key, "")).strip()
        if value:
            return value
    return "> [!gap]\n> This ledger source did not record a claim or summary. Add one before citing it for a domain conclusion."


def source_suffix(retrieved: str, refresh_due: str, source_type: str) -> str:
    parts = []
    if source_type:
        parts.append(f"type {source_type}")
    if retrieved:
        parts.append(f"retrieved {retrieved}")
    if refresh_due:
        parts.append(f"refresh_due {refresh_due}")
    return "; " + "; ".join(parts) if parts else ""


def adapter_title(label: str, entry: dict[str, Any], index: int) -> str:
    for key in ("name", "title", "input", "produces", "path", "format"):
        value = str(entry.get(key, "")).strip()
        if value:
            if key == "path":
                value = Path(value).stem.replace("_", " ").replace("-", " ")
            return safe_note_name(f"{label} {value}", f"{label} {index:03d}")
    return f"{label} {index:03d}"


def adapter_note_body(section: str, label: str, entry: dict[str, Any]) -> str:
    rows = []
    for key, value in entry.items():
        if key in {"url", "source_url", "source_urls", "docs_url"}:
            continue
        if isinstance(value, (str, int, float, bool)):
            rows.append(f"- {key}: `{value}`")
        elif isinstance(value, list):
            clean = [str(item).strip() for item in value if str(item).strip()]
            if clean:
                rows.append(f"- {key}: {', '.join(clean)}")
    details = "\n".join(rows) or "- Manifest entry is present but carries no scalar details."
    return f"""## Adapter Evidence

This {label.lower()} note was folded from `references/adapter-manifest.json`, section `{section}`.

{details}
"""


def adapter_urls(entry: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for key in ("url", "source_url", "docs_url"):
        value = str(entry.get(key, "")).strip()
        if value:
            urls.append(value)
    values = entry.get("source_urls")
    if isinstance(values, list):
        urls.extend(str(item).strip() for item in values if str(item).strip())
    return unique_items(urls)


def load_json_object(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def is_real_captured_source(item: object) -> bool:
    if not isinstance(item, dict):
        return False
    title = str(item.get("title", "")).strip()
    url = str(item.get("url", "")).strip()
    if is_placeholder_value(title) or is_placeholder_value(url):
        return False
    if not (url.startswith("http://") or url.startswith("https://")):
        return False
    return True


def is_placeholder_value(value: str) -> bool:
    clean = value.strip().lower()
    if not clean:
        return True
    if clean in {"todo", "tbd", "placeholder", "example", "sample", "none", "n/a"}:
        return True
    return any(token in clean for token in ("example.com", "<", ">", "placeholder", "todo", "replace-me"))


def unique_concept_title(vault: Path, title: str, index: int) -> str:
    clean = safe_note_name(title, f"Source {index:03d}")
    path = vault / "wiki" / "concepts" / f"{clean}.md"
    if not path.exists():
        return clean
    return safe_note_name(f"{clean} {index:03d}", f"Source {index:03d}")


def note_frontmatter(
    type_: str,
    title: str,
    stamp: str,
    *,
    status: str = "active",
    confidence: str = "practitioner",
    related: list[str] | None = None,
    source_urls: list[str] | None = None,
) -> str:
    level = confidence_level(confidence)
    tags = unique_items([f"#domain/{DOMAIN_SLUG}", f"#type/{safe_slug(type_, 'note')}", f"#confidence/{level}"])
    links = unique_items([*(related or []), *SPINE_RELATED])
    urls = unique_items(source_urls or [])
    return "\n".join([
        "---",
        f"type: {yaml_scalar(type_)}",
        f"title: {yaml_scalar(title)}",
        f"domain: {yaml_scalar(DOMAIN)}",
        f"status: {yaml_scalar(status)}",
        f"created: {yaml_scalar(stamp)}",
        f"updated: {yaml_scalar(stamp)}",
        yaml_list("tags", tags),
        f"confidence: {yaml_scalar(level)}",
        yaml_list("related", links),
        yaml_list("source_urls", urls),
        "---",
    ])


def confidence_level(value: object) -> str:
    clean = re.sub(r"[_/]+", " ", str(value).lower()).strip()
    clean = clean.removeprefix("#confidence/").removeprefix("confidence/")
    clean = CONFIDENCE_ALIASES.get(clean, clean.replace(" ", "-"))
    return clean if clean in CONFIDENCE_LEVELS else "practitioner"


def yaml_scalar(value: object) -> str:
    return json.dumps(str(value))


def yaml_list(name: str, values: list[str]) -> str:
    if not values:
        return f"{name}: []"
    rows = [f"{name}:"]
    rows.extend(f"  - {yaml_scalar(value)}" for value in values)
    return "\n".join(rows)


def unique_items(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = str(value).strip()
        if clean and clean not in seen:
            out.append(clean)
            seen.add(clean)
    return out


def safe_note_name(value: str, fallback: str = "Seed Note") -> str:
    text = re.sub(r"\s+", " ", value).strip(" .")
    text = re.sub(r"[<>:\"/\\|?*]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text[:80].strip() or fallback


def safe_slug(value: str, fallback: str = "seed") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or fallback


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def append_log(vault: Path, message: str, stamp: str) -> None:
    log = vault / "wiki" / "log.md"
    if log.exists():
        log.write_text(log.read_text(encoding="utf-8").rstrip() + f"\n- {stamp} - {message}\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
