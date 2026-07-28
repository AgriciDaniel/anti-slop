---
type: "concept"
title: "Corpus Study Method"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/concept"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]"
  - "[[The Em Dash|Em Dash Population Prevalence]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Superseded Figures]]"
  - "[[Why Detection Fails]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Moving Baseline Objection]]"
  - "[[Signs Are Not The Problem|Signs of AI Writing]]"
source_urls:
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2606.29540"
  - "https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/"
  - "https://arxiv.org/abs/2501.15654"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
---

# Corpus Study Method

Excess vocabulary is an epidemiological method borrowed for linguistics. It
answers a population question with arithmetic instead of a classifier, and that
single design choice is why it carries more weight in this vault than any
detector output.

## The borrowed design

Excess mortality analysis does not diagnose a cause of death. It counts deaths,
compares them against the number a pre-event trend predicts, and reports the
gap. No individual death is attributed to anything. The excess is a property of
the population.

kobak-excess-vocabulary applies the identical shape to word frequency. It fits
the frequency of every word across more than 15 million PubMed abstracts from
2010 to 2024, extrapolates each word's pre-2023 trajectory forward, and
subtracts the extrapolation from the observed 2024 count. Words whose observed
frequency exceeds the extrapolation by a large margin are the excess set. From
the size of that excess it derives a lower bound: at least 13.5 percent of 2024
PubMed abstracts were processed with an LLM, reaching 40 percent in some
subcorpora.

| Component | Excess mortality | Excess vocabulary |
| --- | --- | --- |
| Unit counted | deaths per week | word occurrences per corpus year |
| Counterfactual | pre-event mortality trend | pre-2023 frequency trajectory |
| Quantity reported | observed minus expected | observed minus extrapolated |
| Attribution scope | population only | corpus only |
| Individual verdict | none | none |
| Main failure mode | wrong baseline window | a word that shifted for unrelated reasons |

The word "processed" in the Kobak result is load bearing. The method registers
a text that a model touched. It cannot separate a model that generated the
abstract from a model that copyedited a human draft, and the paper does not
claim otherwise.

## Why the placebo split matters

czuma-em-dash-prevalence is the second exemplar and it adds the validity check
that makes the family credible. Working across 69,632 medRxiv preprints, it
measures em-dash prevalence in Discussion sections rising from 4.23 percent
before ChatGPT to 11.58 percent after, a 7.35 point rise with a 95 percent
confidence interval of 6.94 to 7.77 and an odds ratio of 2.96. The trajectory
runs at roughly 4 percent through 2023, 8.0 percent in 2024, and 20.3 percent
in 2025.

The check is the placebo: the same split applied to two windows entirely inside
the pre-LLM era moves the number by plus 0.13 points. A method that produced a
large effect on the placebo would be measuring drift in the corpus rather than
drift in the writing. The study is pre-registered on OSF as HFT8C, which is the
reason [[Evidence Quality Ladder]] places it above every vendor claim about the
same punctuation mark.

Its author states the conclusion this vault adopts verbatim: the em dash is a
population-level indicator, not a per-paper detector of LLM use.

## What the method establishes

1. That the aggregate rate of LLM involvement in a defined corpus rose, with a
   quantified lower bound and an interval.
2. That the rise is concentrated in stylistic vocabulary. kobak-excess-vocabulary
   reports the excess words are overwhelmingly stylistic verbs and adjectives
   rather than content words, which is the empirical basis for treating style
   markers as a signal at all.
3. That the marker set is dated. Every excess-vocabulary result belongs to the
   model cohort and corpus that produced it, which is the mechanism behind
   [[Marker Cohort Rot]].
4. That a baseline exists. Without a corpus baseline, a claim that some phrase
   is an AI tell is unfalsifiable folklore.

## What the method cannot establish

- Per-document origin. A 13.5 percent corpus rate says nothing about the
  document in front of you. Applying a population rate to one case is the base
  rate fallacy, and it is the exact move [[The Firewall]] forbids.
- Which model. Corpus prevalence is model-agnostic by construction.
- Depth of involvement. A one-pass grammar fix and a fully generated abstract
  both register.
- Quality. Nothing in the arithmetic ranks the writing. [[The Accessibility Objection]]
  covers the evidence that model-touched text can be rated better by expert
  readers.
- Durability. The counterfactual assumes human usage would have continued its
  old trajectory. [[The Moving Baseline Objection]] documents why that
  assumption decays.

## Why this outranks detector prevalence

A detector-based prevalence estimate inherits every error of the detector and
adds a sampling error on top. The failure is documented at both ends. On the
vendor side, openai-classifier-withdrawal records OpenAI's own classifier
catching 26 percent of AI text while mislabelling human text 9 percent of the
time, withdrawn on 2023-07-20 for low accuracy. On the human side,
russell-expert-detectors found a majority vote of five expert annotators
misclassified only 1 of 300 articles, beating commercial and open-source
detectors even under paraphrase evasion, which means the automated tools were
not near the ceiling of the task.

A corpus method has no classifier to be wrong. Its errors are baseline errors,
which are visible, arguable, and testable with a placebo. That is a different
class of uncertainty, and a smaller one.

## Reading a corpus figure without over-reading it

1. Find the corpus. PubMed abstracts and medRxiv preprints are academic
   writing under length pressure. Neither generalises to email or code.
2. Find the baseline window and ask what else changed in it.
3. Check for a placebo or negative control. If there is none, treat the effect
   size as an upper bound on confidence, not on magnitude.
4. Check whether the headline is a bound or a point estimate. "At least 13.5
   percent" is a floor, and quoting it as "13.5 percent of papers are AI" is a
   misquote.
5. Check the publication state. Peer-reviewed and pre-registered are separate
   properties and both matter, per [[Evidence Tiers]].
6. Refuse to carry the number down to a single document, no matter how strong
   it is.

wikipedia-signs-of-ai-writing makes the same point from the practitioner side
when it warns that the listed patterns are only potential signs of a problem
and not the problem itself. Corpus evidence tells you which signs are worth
looking for. It never tells you what any one document is.

## Related

- [[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]
- [[The Em Dash|Em Dash Population Prevalence]]
- [[Evidence Quality Ladder]]
- [[Superseded Figures]]
- [[Why Detection Fails]]
- [[The Firewall]]
- [[Marker Cohort Rot]]
- [[The Moving Baseline Objection]]
- [[The Accessibility Objection]]
- [[Signs Are Not The Problem|Signs of AI Writing]]
