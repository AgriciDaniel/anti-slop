# Build status, 2026-07-27

Nine parallel agents were killed mid-write by a session usage limit. This file
records exactly what landed, what did not, and how to resume.

## Where the build stands

`brainstein audit-brain` reports **uncapped anatomy 95/100**, held at maturity
`researched` (capped score 74) by one failing category.

| Category | Score |
|---|---|
| spec | 6/6 |
| sources | 10/10 |
| adapters | 6/9 |
| vault | 10/12 |
| demo | 9/9 |
| release | 11/11 |
| brand | 10/10 |
| substance | 33/33 |

The vault scores **100/100 on the ported substance scorer**: zero near-duplicate
pairs, max heading-skeleton reuse 1, max anchor reuse 2, specific-citation
coverage 1.0, table-or-procedure coverage 1.0, density floor 912 note-specific
words against a floor of 120.

Scanner suite: **76 checks passing**.

## Done

- Brainstein v3 spec, scaffold, git repo, first commit.
- `references/source-ledger.json`: 42 entries, 37 primary-type, every one with
  `retrieved`, `last_verified`, `refresh_due`, `evidence_tier`, `claims`, and
  explicit `limitations`. No expired refresh dates.
- `wiki/sources/research-pack-2026-07-27.md`: 67 URLs, 112 dates, plus the
  four sources that could not be read and why.
- `references/current-requirements.md` and `market-research.md` rewritten with
  real content and the superseded-figure corrections.
- 34 wiki notes, mean 169 lines and 28.6 wikilinks each.
- Six deterministic scanners plus a shared helper: `scan_residue.py`,
  `scan_placeholders.py`, `scan_refs.py`, `scan_packages.py`, `lint_voice.py`,
  `score_substance.py`, `scan_common.py`, with `tests/test_scanners.py`.
- `score_substance.py` patched to accept a comma-separated `--note-type` list,
  because this vault splits content across concept, marker, procedure and
  surface rather than the single `spoke` type the original assumed.
- CHANGELOG, THIRD_PARTY_NOTICES, plugin.json `allowed-tools`, curator
  workflow coverage, deterministic sample-vault checksums.
- Plugin skeleton: five SKILL.md files, two subagents, one reference file.

## Not done

### 1. Nineteen wiki notes (blocks rubric C4.3)

369 dead wikilinks remain, almost all pointing at these:

| Folder | Missing notes |
|---|---|
| `markers/` | Why Pangram Is Not Cited, Vendor Residue Markers, Marker Cohort Rot |
| `procedures/` | The Stranger Test, The Attribution Test, The Load Bearing Test |
| `surfaces/` | Agent Output Surface, Knowledge Base Surface |
| `detection/` | Model Fingerprints, Humanizers, Regulation and Governance |
| `evidence/` | The Code Slop Disagreement, Package Hallucination Evidence, Sycophancy Evidence |
| `counterarguments/` | all five: The ESL Objection, The Accessibility Objection, The Moral Panic Objection, The Moving Baseline Objection, What This Brain Does Not Claim |

Three of the five structural tests are among these, so the flagship content is
incomplete. The full briefs are in the conversation history; the constraints
are in `wiki/meta/Note Conventions.md`.

A second pass must also normalise link-name variants the agents invented:
`Deletion Test` versus `The Deletion Test`, `Model Fingerprints` versus
`Model Specific Fingerprints`, `The Load-Bearing Test` versus
`The Load Bearing Test`.

### 2. Domain adapters (blocks rubric C3.1 and the maturity ladder)

Nothing was written. `references/adapter-manifest.json` still declares
`generic_only: true`, which caps maturity at `researched`. Needs two symmetric
ingest, synthesize, render lanes (review run and marker cohort refresh), JSON
schemas, fixtures, and `tests/test_adapters.py` asserting determinism.

### 3. Plugin completion

Correction to an earlier version of this file: `.claude-plugin/plugin.json`
does exist and is valid JSON. It was missed because `ls -R` does not list
hidden directories.

Frontmatter has now been validated across all seven files. All five SKILL.md
files and both agents parse, `name` matches the parent directory in every
case, no description contains an angle bracket, and no file contains a long
dash. `slop-review` correctly carries `disallowed-tools` rather than
`allowed-tools`, which is the trap in the v2.1.220 contract. Agents correctly
use camelCase `maxTurns` while skills use kebab-case.

Still missing: `README.md`, a `hooks/hooks.json` file (the directory is
empty), and five of six `references/` files. Only `structural-tests.md` was
written.

### 4. Verification pass

Never started. Nothing has independently checked that every citation resolves
and supports the claim attached to it.

## Resume order

1. Adapters. Single largest score gain and it unblocks the maturity ladder.
2. The nineteen notes, counterarguments and the three tests first.
3. Link-name normalisation, then re-run the audit.
4. Plugin completion and frontmatter validation.
5. Fresh-context adversarial verification, then `--require market-ready`.

## Standing constraints for any resumed work

- No em dash and no en dash anywhere. Verified clean across the repo so far.
- No authorship verdicts.
- Only cite ids present in `references/source-ledger.json`.
- Vary heading structure per note; the substance scorer fails on template
  convergence and it currently passes at 100.
