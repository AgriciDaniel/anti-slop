---
name: anti-slop-brain
description: >
  Scaffold and operate Anti-Slop Brain, a source-cited Obsidian brain for detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection.
  Use when the user says "anti-slop-brain", "Anti-Slop Brain", "create a detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection brain",
  "import sources", "synthesize plan", "render report", or wants a persistent
  vault-backed operating system for detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection.
argument-hint: "new | ingest | synthesize | report | visuals | lint | next"
license: Apache-2.0 AND CC-BY-SA-4.0 AND CC-BY-4.0
---

# Anti-Slop Brain

Operate the deployed vault first. Treat `CODEX.md`, `wiki/hot.md`, and
`wiki/index.md` as vault-root-relative paths, where the vault root is the
directory passed to `--vault` or opened in Obsidian. In this repo, the template
vault root is `assets/template-brain/` and the demo vault root is
`examples/sample-vault/`.

Secretary: use `agents/anti-slop-secretary.md` for grounded answers, claim review,
and vault maintenance. That secretary reads the brain first, cites a vault note
and an official URL, and stays advisory and read-only.

## Commands

```bash
/anti-slop-brain new <client-slug> --owner <name>
/anti-slop-brain ingest --vault <path> --file <source>
/anti-slop-brain synthesize --vault <path>
/anti-slop-brain report --vault <path>
/anti-slop-brain visuals --vault <path>
/anti-slop-brain lint --vault <path>
/anti-slop-brain next --vault <path>
```

Source checkout equivalent:

```bash
anti-slop-brain new <client-slug> --owner <name>
anti-slop-brain ingest --vault <path> --file <source>
anti-slop-brain synthesize --vault <path>
anti-slop-brain report --vault <path> --html-only
```

## Required Operating Rules

1. Read `<vault>/CODEX.md`.
2. Read `<vault>/wiki/hot.md`.
3. Read `<vault>/wiki/index.md`.
4. Preserve `.raw/` as immutable source material.
5. Never store credentials in the vault.
6. Never make domain-specific claims without dated trustworthy sources.
7. Keep `hot`, `index`, `overview`, and `log` current.
8. Record research evidence in `references/source-ledger.json`.
9. Record domain adapter completion in `references/adapter-manifest.json`.

## Script Mapping

- `new` -> `python scripts/scaffold_vault.py`
- `ingest` -> `python scripts/ingest_source.py`
- `synthesize` -> `python scripts/synthesize_brain.py`
- `report` -> `python scripts/render_brain_report.py`
- `visuals` -> `python scripts/generate_vault_visuals.py`
- `lint` -> `python scripts/lint_vault.py`
- `next` -> `python scripts/guide_next_action.py`

## Quality Gates

- No authorship verdict, ever; this brain reports defects, not origin
- No hard failure on a stylistic marker alone; markers route to structural tests
- No claim about detector accuracy, marker frequency, or prevalence without a current cited source
- No credentials, tokens, or private operator content in repo artifacts
- No model self-grading as a release gate; deterministic scanners re-run after every repair

Do not call this brain market-ready unless `scripts/audit_brain.py --require
market-ready` passes. A scaffold is not a finished brain.

## Research Refresh

30 days for model-specific marker cohorts and detector claims; 90 days for corpus studies and regulation; before every release for any numeric claim
