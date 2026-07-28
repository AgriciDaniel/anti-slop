# Changelog

**This directory does not version separately. The changelog is the repository
changelog: [`../CHANGELOG.md`](../CHANGELOG.md).** This file is a pointer so
nobody reads a stale second history by walking into the subdirectory first.

The version here tracks the repository version, currently 0.1.0. See the root
changelog for what 0.1.0 contains, what an adversarial verification pass found
and corrected before release, and the limitations carried into it.

## [0.1.0] - 2026-07-28

Ships as part of the `anti-slop` repository release 0.1.0. This directory does
not carry an independent version; the number above mirrors the repository so a
reader who lands here first knows which release they are looking at.

## What this directory contributed to 0.1.0

Ledger and vault figures below are the ones a reader can check, and they are
the figures the root changelog uses. The earlier version of this file quoted 42
ledger entries and 56 notes, which were the counts on 2026-07-27, before the
release-preparation pass.

| Piece | Current | How to check |
|---|---|---|
| Source ledger | 43 dated entries: 30 `primary`, 4 `vendor`, 3 `supporting`, 2 `official`, 2 `practitioner`, 1 `authority`, 1 `regulator`. Each carries a retrieval date, a refresh date, an evidence tier and stated limitations | `references/source-ledger.json` |
| Vault | 62 Markdown files: 58 content notes across ten folders plus four spine files (`index`, `hot`, `log`, `overview`) | `find wiki -name '*.md' \| wc -l` |
| Scanners | Six deterministic scanners, standard library only | `scripts/` |
| Adapter lanes | Two, review run and marker cohort refresh, with schemas, fixtures and determinism tests | `references/adapter-manifest.json` |
| Tests | 314 checks: 107 scanner, 207 adapter, plus the pipeline test | `tests/` |

Note on `source_type`: the ledger's `rules.accepted_primary_types` enum counts
`vendor`, `official`, `regulator` and `authority` alongside `primary`, which
totals 38. That enum governs whether a source is admissible, not whether it is
independent. The precise statement is 43 sources, 30 of them `primary`, plus
four vendor sources, none of which is tiered `EVIDENCE-BASED`: three
`PRACTITIONER` and one `FOLKLORE`, each with its limitations written out.

`scripts/score_substance.py` is a port and generalisation of the wiki substance
scorer from the sibling Claude Blog Brain, with thresholds retained unchanged.
Origin is credited in the module docstring and in `THIRD_PARTY_NOTICES.md`.
