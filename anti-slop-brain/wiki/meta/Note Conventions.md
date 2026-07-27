---
type: "meta"
title: "Note Conventions"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/meta"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
source_urls: []
---

# Note Conventions

The rules every note in this vault follows. They exist because this vault is
graded by its own subject matter: a brain about padded, generic, uncited
writing that is itself padded, generic and uncited would refute its own thesis.
The conventions are enforced mechanically by `scripts/score_substance.py`, not
by good intentions.

## Frontmatter contract

Every note opens with a YAML block containing all ten keys below, in this
order. Two of them, `type` and `title`, are checked by the Brainstein audit;
the rest are checked by the vault linter and by review.

| Key | Required | Allowed values |
| --- | --- | --- |
| `type` | yes | one of the 18 type values in [[Tag Taxonomy]] |
| `title` | yes | matches the filename without extension |
| `domain` | yes | the brain-wide domain string, verbatim |
| `status` | yes | `active`, `seed`, `evergreen`, `draft`, `proposed` |
| `created` | yes | ISO date, `YYYY-MM-DD` |
| `updated` | yes | ISO date, bumped on every substantive edit |
| `tags` | yes | exactly one `#domain/`, one `#type/`, one `#confidence/` |
| `confidence` | yes | `evidence-based`, `practitioner`, `contested`, `folklore` |
| `related` | yes | list of wikilinks, at least eight per spoke note |
| `source_urls` | yes | list, empty on hub and index notes |

## Confidence mapping

A note inherits the weakest confidence of the sources it depends on. Promoting
a note above its sources is the single most common way a knowledge base starts
asserting things it cannot support.

| Ledger `confidence` | Note `confidence` | Tag |
| --- | --- | --- |
| `high` | `evidence-based` | `#confidence/evidence-based` |
| `medium` | `practitioner` | `#confidence/practitioner` |
| `low` | `contested` | `#confidence/contested` |
| no ledger entry | `folklore` | `#confidence/folklore` |

Folklore is recorded so it can be argued with, never asserted as true. A
popular claim is not evidence. The Pangram em-dash figures live at this tier
for exactly that reason: see [[Why Pangram Is Not Cited]].

## Substance floors

These are measured, not judged. `scripts/score_substance.py` fails the build
when any of them is missed.

| Floor | Threshold | What it prevents |
| --- | --- | --- |
| Note length | 80 lines mean across the vault | thin stubs padded out with headings |
| Wikilinks | 8 mean per note | orphan notes that never join the graph |
| Note-specific words | 120 minimum per note | boilerplate shared across many notes |
| Distinct ledger citations | 2 minimum per spoke | single-source assertions |
| Table or procedure | present in every spoke | prose that never commits to specifics |
| Near-duplicate similarity | below 0.82 between any pair | two notes saying the same thing |
| Heading skeleton reuse | at most 3 notes share one | template convergence |
| Anchor line reuse | at most 2 notes share one | copy-pasted opening sentences |
| Generic citation bundle | at most 3 notes share a set of 6 or more | pasted reference blocks |

The heading-skeleton and anchor-reuse floors deserve emphasis. They are the
mechanical expression of [[Distributional Convergence]]: when many notes are
written to the same outline, the outline becomes the content and the notes stop
carrying information. Vary the structure per note. A note about a corpus study
should not have the same headings as a note about a repair procedure.

## Citation rules

1. Every numeric claim carries a ledger source id in the body text, written as
   a bare id such as `kobak-excess-vocabulary`, and the matching URL in
   `source_urls`.
2. A claim with one source is marked as single-source in the text. Market,
   comparative, current, and numeric claims require a second source or an
   explicit note that one is missing.
3. Never attach a practitioner impact claim to an official vendor URL. The URL
   supports what the vendor said, not whether the vendor is right.
4. Figures that were superseded are recorded with the correction attached, not
   silently replaced. See [[Superseded Figures]].

## Prose rules

- No em dash and no en dash anywhere, including inside code comments and SVG
  assets, where the Brainstein audit checks mechanically. Use commas, periods,
  colons, parentheses.
- No authorship verdicts. This vault documents defects, not origin. The
  reasoning is in [[The Firewall]] and the evidence is in
  [[Detector Bias Against Language Learners]].
- No claim that a stylistic marker proves anything on its own. Markers route to
  procedures; see [[Evidence Tiers]].

## Related

- [[Tag Taxonomy]]
- [[Provenance Trace Policy]]
- [[Evidence Tiers]]
- [[The Firewall]]
- [[Distributional Convergence]]
- [[Superseded Figures]]
- [[Why Pangram Is Not Cited]]
- [[Detector Bias Against Language Learners]]
