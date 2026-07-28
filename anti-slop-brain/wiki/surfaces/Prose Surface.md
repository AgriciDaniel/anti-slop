---
type: "surface"
title: "Prose Surface"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/surface"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]"
  - "[[The Em Dash|Em Dash Population Prevalence]]"
  - "[[Evidence Tiers]]"
  - "[[The Deletion Test]]"
  - "[[The Stranger Test]]"
  - "[[The Attribution Test]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Marker Cohort Rot]]"
  - "[[Humanizers|Humanizer Quality Degradation]]"
  - "[[The Firewall]]"
source_urls:
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2606.29540"
  - "https://arxiv.org/abs/2604.19768"
  - "https://arxiv.org/abs/2605.19936"
  - "https://arxiv.org/abs/2512.09292"
  - "https://arxiv.org/abs/2604.22142"
---

# Prose Surface

Essays, blog posts, reports, grant text, literature reviews, and the narrative
parts of documentation share one property that makes them the hardest surface
in this vault to work on honestly: the training corpus for every frontier model
is largely made of edited formal prose, so competent edited formal prose is the
thing the models were taught to imitate. A well-revised human paragraph and a
model paragraph converge because they are aiming at the same target. Everything
below is written around that fact.

## Where the defect actually sits

Prose slop is rarely a vocabulary problem. It is a claim-density problem. A
padded paragraph asserts nothing that a reader could disagree with, cites
nothing a reader could check, and survives deletion without loss. The markers
are how you find the paragraph. [[The Deletion Test]] and [[The Stranger Test]]
are how you convict it. That ordering is not optional here, because the marker
base rates on this surface are genuinely high in human writing.

The corpus evidence sets the scale. `kobak-excess-vocabulary` measured at least
13.5 percent of 2024 PubMed abstracts as LLM-processed, rising to 40 percent in
some subcorpora, using a detector-free method that compares observed against
extrapolated word frequencies. The excess words were overwhelmingly stylistic
verbs and adjectives, not content words. That is the single most important
structural fact about this surface: the shift shows up in the connective tissue
of a sentence, not in what the sentence claims.

## Marker routing for long-form prose

Each row names the marker, the tier it sits in under [[Evidence Tiers]], the
procedure that has to convict before anything is edited, and the false-positive
class that is specific to this surface.

| Marker | Tier | Procedure that must convict | Surface-specific false positive |
| --- | --- | --- | --- |
| [[Puffery and Undue Emphasis]] | 1 | [[The Inversion Test]] | book jackets, grant abstracts, and obituary prose are puffed by genre |
| [[Excess Vocabulary]] | 1 | [[The Stranger Test]] | technical registers where `robust` and `interplay` are terms of art |
| [[Puffery and Undue Emphasis|Superficial Participial Analysis]] | 1 | [[The Deletion Test]] | narrative writing where the participle carries real sequence |
| [[The Attribution Test|Vague Attribution]] | 1 | [[The Attribution Test]] | genuine literature surveys that summarise many sources at once |
| [[Tricolon and Rule of Three|Rule of Three]] | 1 | [[The Deletion Test]] | rhetoric taught in every composition class since Cicero |
| [[Negative Parallelism]] | 1 | [[The Inversion Test]] | contrastive argument where the negated half is the point |
| [[Hedging and Hesitancy|Hedging Density]] | 1 | [[The Attribution Test]] | scientific caution, where hedging is a correctness requirement |
| [[The Em Dash|Em Dash Density]] | 2 | none, routes only | house style, typographic training, and editorial software |
| [[Evidence Tiers|Uniform Sentence Length]] | 2 | [[The Deletion Test]] | plain-language and accessibility rewrites target uniformity |
| [[Documentation Surface|Section Inflation]] | 2 | [[The Deletion Test]] | reports with a mandated section list |
| [[Puffery and Undue Emphasis|Generic Positive Conclusion]] | 1 | [[The Deletion Test]] | opinion pieces that legitimately end on a position |

Two rows deserve their citations stated inline. `bakhshi-saying-more` measured
LLM tricolon production at nearly twice the expert human rate and hesitancy
markers at roughly twice human density across 225 texts and about 600,000
tokens, which is what places [[Tricolon and Rule of Three|Rule of Three]] and [[Hedging and Hesitancy|Hedging Density]] in tier
1 rather than in folklore. `czuma-em-dash-prevalence` is pre-registered on OSF
as HFT8C across 69,632 medRxiv preprints and its own conclusion is adopted
verbatim in this vault: the em dash is a population-level indicator, not a
per-paper detector. That is why the em-dash row has no procedure attached. It
routes attention and nothing else. See [[Why Pangram Is Not Cited]] for the
vendor figures this vault refuses to quote.

## The trained-on-edited-prose problem

This is the false-positive risk that belongs to prose and to no other surface
in this vault. Three separate findings converge on it.

First, detector behaviour. `stowe-detector-bias` ran 16 detection models over
student essays labelled for demographics and found English-language-learner
essays disproportionately flagged, and non-White ELL students disproportionately
flagged relative to White ELL peers, while human annotators showed no
significant demographic bias on the same essays. The defect is in the
instrument, not in the writers. This is the load-bearing reason for the
no-authorship-verdict rule in [[The Firewall]].

Second, the baseline is moving. `yakura-spoken-convergence` found words
preferentially generated by ChatGPT rising abruptly in spontaneous human speech,
with `delve` up 48 percent, `realm` up 35 percent, and `adept` up 51 percent
within 18 months of release, corroborated by a preregistered experiment with n
equal to 496. A marker list calibrated in 2024 will misfire on 2026 humans.
[[Marker Cohort Rot]] is the standing policy for that.

Third, the premise itself is contested. `miletic-lexical-diversity` examined
over 37,000 ACL Anthology papers and found LLM-modified text lower in lexical
diversity, yet expert readers rated the same modified text as more
understandable and more exciting. Lower diversity is measurable; worse is a
judgement the measurement does not support. [[The Accessibility Objection|Slop Is Not Always Worse]] holds
this argument.

## Repair on this surface degrades voice by default

Surface-level rewriting is not a safe default action here. `masrour-damage-humanizers`
states that all humanizers tend to degrade the quality of the original text, with
a fluency win rate against the original of 26.0 percent for best-tier tools,
14.67 percent for medium, and 2.67 percent for the worst, and documents
hallucinated citations and comment leakage as failure modes.
`vannuenen-voice-under-revision` adds the mechanism: LLM revision decreases
function words, contractions, and first-person pronouns while increasing
vocabulary diversity and word length, the shift persists under explicit
instructions to preserve the author's voice, and rewritten texts converge in
feature space regardless of where they started. Both are preprints verified at
abstract level, so they are cited as direction rather than as magnitude.

The operating consequence is a rule, not a preference: on the prose surface,
repair only what a procedure convicted, and never run a whole-document rewrite
as a first move. A convicted padded paragraph gets cut. An unconvicted
paragraph with an em dash in it gets left alone.

## Calibrate against the author, not against a mean

The honest answer to the ELL false-positive problem is per-author calibration.
Collect a sample of the author's own pre-2023 or otherwise unassisted writing,
measure their sentence-length variance, hedging rate, and punctuation habits,
and compare the draft against that baseline rather than against a population
mean. Wikipedia's guide, captured as `wikipedia-signs-of-ai-writing`, reaches
the same place from a different direction: it maintains an ineffective-indicators
list precisely so that formal vocabulary and perfect grammar are not treated as
evidence. The prior-art skill `blader-humanizer` also gets this right in one
respect worth copying, giving a user-supplied writing sample precedence over its
own style rules.

## What a prose pass emits

1. A residue and placeholder scan result, before any judgement is formed.
2. A marker inventory with tier and count, explicitly labelled as routing
   information rather than as a finding.
3. One worksheet row per structural test actually run, carrying its artifact:
   the cut span and the named loss, the written-out negation, or the resolved
   citation.
4. A repair diff limited to convicted spans, with the scanners re-run after.

Anything that skips step 3 is a style opinion wearing a report's clothes. See
[[The Firewall|Severity and Confidence]] for how the two axes are kept apart in the output.

## Related

- [[Code Surface]]
- [[Documentation Surface]]
- [[Knowledge Base Surface]]
- [[Distributional Convergence]]
- [[Why Detection Fails]]
- [[Signs Are Not The Problem|Signs of AI Writing]]
- [[Note Conventions]]
- [[AI Slop|Slop as a Category]]
