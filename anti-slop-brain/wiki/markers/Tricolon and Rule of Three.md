---
type: "marker"
title: "Tricolon and Rule of Three"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/marker"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Evidence Tiers]]"
  - "[[Why Pangram Is Not Cited]]"
  - "[[Negative Parallelism]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[The Stranger Test|Stranger Test]]"
  - "[[Puffery and Undue Emphasis]]"
  - "[[Distributional Convergence]]"
  - "[[Prose Surface]]"
  - "[[Documentation Surface]]"
  - "[[Marker Cohort Rot]]"
source_urls:
  - "https://arxiv.org/abs/2604.19768"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://www.pangram.com/supporting-evidence"
---

# Tricolon and Rule of Three

Three is the number that arrives when a model has nothing in particular to say.
Two items look thin. Four invites the reader to ask why those four. Three
sounds complete, closes with a cadence, and requires no argument about
membership. The result is prose where a list of three is the default container
for any idea, whether or not the idea has three parts:
"keynote sessions, panel discussions, and networking opportunities", followed
by "innovation, inspiration, and industry insights".

## What was measured

`bakhshi-saying-more` compared roughly 600,000 tokens across 225 texts against
an expert human comparison group and found that language models produce
tricolons at **nearly twice the expert human rate**. That is the figure this
note carries, and the phrasing "nearly twice" is deliberate: the paper reports a
comparative rate, and turning a comparative rate into a false precision would
be the same defect this brain exists to catch.

`wikipedia-signs-of-ai-writing` describes the same pattern independently, under
the shortcut RO3, and adds the functional observation that matters for repair:
the structure runs from adjective, adjective, adjective through to short
phrase, short phrase, and short phrase, and it is used to make superficial
analyses appear more comprehensive. The triple is a comprehensiveness costume.

Two independent observations of the same effect, one with a corpus and an
expert baseline, place this at Tier 1 in [[Evidence Tiers]]. The tier is a
statement about measurement quality only. It licenses routing, never a verdict.

## The figure this note does not use

`pangram-supporting-evidence` states that AI uses tricolons about four times as
often as humans. That figure is more dramatic, more quotable, and not used
here. The reasons, in order of severity:

| Requirement | `bakhshi-saying-more` | `pangram-supporting-evidence` |
| --- | --- | --- |
| Sample size stated | yes, 225 texts, roughly 600,000 tokens | no |
| Corpus described | yes, with an expert comparison group | no |
| Method published | yes | none published |
| Date on the claim | 2026-03-27 | none |
| Internally consistent | no contradiction found | states two different human baselines for its em dash claim on the same page |
| Commercial interest in the result | none stated | sells a detector the finding promotes |

The ledger's own downgrade rule settles it: a marketing page with no date and
no citation is tiered FOLKLORE and is never quoted as a measured figure. The
Pangram URL is listed in this note's `source_urls` so a reader can verify that
criticism, under the convention recorded in [[Evidence Tiers]] for citing a
source you are refusing to use. Nothing in this note rests on it. The full
argument, including the base-model result that undermines the vendor's core
product claim, is in [[Why Pangram Is Not Cited]].

A four-times figure would not even change the procedure below. Doubling and
quadrupling both route to the same test. Preferring the smaller, sourced number
costs nothing and keeps the brain honest, which is the point of the exercise.

## Counting rule

Density is the signal, so the count has to be reproducible. Otherwise two
reviewers produce two numbers and the marker becomes an opinion.

1. Count a tricolon only when three items are grammatically parallel and share
   one syntactic slot. Three sentences on a related topic are not a tricolon.
2. Count the sentence once, even when the triple is nested inside a longer
   list.
3. Do not count enumerations whose membership is fixed by the world: three
   branches of government, three primary colours, three retry attempts.
4. Do not count code, configuration, tables, or reference lists. Restrict to
   prose spans as defined in [[Prose Surface]].
5. Record instances per 1,000 words, with the spans attached. Report the raw
   count, never a normalised score.
6. Where a triple co-occurs with a corrective negative parallelism, record one
   finding, not two. See [[Negative Parallelism]].

## Density guidance

| Instances per 1,000 words | Interpretation | Action |
| --- | --- | --- |
| 0 to 1 | unremarkable in any register | record only |
| 2 to 3 | consistent with ordinary rhetorical writing | record, check the highest-value instance |
| 4 or more | above the comparative range implied by `bakhshi-saying-more` | route every instance to the deletion test |

These bands are an operating convention of this brain, derived from the
comparative rate rather than measured directly. They are labelled as such here
so nobody later quotes them as a finding.

## False positive class: who this marker wrongly flags

1. **Speechwriters and rhetoricians.** The tricolon is one of the oldest
   deliberate devices in the language. Its presence in persuasive human prose
   is a sign of craft.
2. **Legal drafters.** Enumerated conditions frequently come in threes because
   the statute has three conditions.
3. **Technical writers documenting three-part APIs.** Three parameters produce
   three items. The world supplied the number.
4. **Marketing and brand copy.** Triples are a house convention across the
   entire discipline.
5. **Children's writing, liturgy, and folklore.** Triples are structural in
   these genres.
6. **Second-language writers taught parallelism as a correctness rule.**
   Explicit instruction in parallel structure produces more parallel
   structures.

## Repair

A tricolon is not repaired by making it a pair. Cutting one item at random
produces the same empty sentence with a worse rhythm. The repair is:

1. Take each item to the [[The Deletion Test|Deletion Test]]. Remove it and state what the
   sentence stopped claiming.
2. Items that survive stay, however many there are. Two survivors give a pair,
   four give a list of four, and both are fine.
3. If no item survives, the whole triple is decoration and the sentence goes.
4. If exactly one item survives, ask the [[The Stranger Test|Stranger Test]] question about it:
   could someone who never read the source have written it? If yes, the
   sentence is generic even after repair, and the finding is the missing
   specific, not the triple.

## Related

- [[Evidence Tiers]]
- [[Why Pangram Is Not Cited]]
- [[Negative Parallelism]]
- [[Hedging and Hesitancy]]
- [[Puffery and Undue Emphasis]]
- [[The Deletion Test|Deletion Test]]
- [[The Stranger Test|Stranger Test]]
- [[Distributional Convergence]]
- [[Marker Cohort Rot]]
- [[Prose Surface]]
