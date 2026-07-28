---
type: "meta"
title: "dashboard"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/meta"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[hot|Hot]]"
  - "[[log|Log]]"
  - "[[Note Conventions]]"
  - "[[Tag Taxonomy]]"
  - "[[Provenance Trace Policy]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
source_urls: []
---

# dashboard

Counts are materialised statically rather than queried, so this vault reads
correctly in any Markdown editor with no plugins installed. Regenerate by
counting; do not add a Dataview block.

## Vault shape, 2026-07-28

| Folder | Notes | Scored for substance |
| --- | --- | --- |
| `concepts/` | 8 | Yes |
| `counterarguments/` | 5 | Yes |
| `detection/` | 8 | Yes |
| `evidence/` | 6 | Yes |
| `markers/` | 10 | Yes |
| `procedures/` | 7 | Yes |
| `surfaces/` | 7 | Yes |
| `meta/` | 5 | No |
| `questions/` | 1 | No |
| `sources/` | 1 | No |
| **Content notes** | **58** | |
| spine: `index`, `hot`, `log`, `overview` | 4 | No |
| **Total Markdown files** | **62** | |

Check it with `find wiki -name '*.md' | wc -l`, which returns 62, and
`scripts/check_links.py --vault wiki`, which reports the same 62. Where a
count is quoted elsewhere it is the 62 total unless it says otherwise.

## Health

| Check | Command | State |
| --- | --- | --- |
| Substance | `score_substance.py --note-type concept,marker,procedure,surface` | 100 |
| Dead links | `scripts/check_links.py --vault wiki` | 0 |
| House style | `lint_voice.py` | clean |
| Rubric | `scripts/audit_brain.py --json` | 100, market-ready |

`check_links.py` is the dead-link check for the shipped wiki, and it reports
`OK: 62 notes, every wikilink resolves.` Do not substitute `lint_vault.py
--vault .` here: that script validates a *client* vault and expects `CODEX.md`,
`shipping-rules.md` and `.raw/.manifest.json`, none of which `wiki/` ships, so
against this repository it exits 1 by design rather than by defect.

## Where the confidence tag distribution sits

Most notes are `evidence-based`. The `contested` notes are the ones resting on
preprints verified at abstract level, and they are tagged that way deliberately
rather than promoted. See [[Evidence Quality Ladder]] and [[Tag Taxonomy]].

## Open items

One resolved question is retained as a worked record. Zero blocking questions.
Fourteen ledger sources fall due 2026-08-26; see [[hot|Hot]].
