---
type: "concept"
title: "Superseded Figures"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/concept"
  - "#confidence/contested"
confidence: "contested"
related:
  - "[[Note Conventions]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Why Pangram Is Not Cited]]"
  - "[[Corpus Study Method]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Package Hallucination Evidence]]"
  - "[[The Em Dash|Em Dash Population Prevalence]]"
  - "[[Marker Cohort Rot]]"
  - "[[Evidence Tiers]]"
  - "[[Provenance Trace Policy]]"
source_urls:
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://www.pangram.com/supporting-evidence"
  - "https://arxiv.org/abs/2501.03437"
  - "https://www.merriam-webster.com/wordplay/word-of-the-year"
  - "https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models/RfC"
  - "https://arxiv.org/abs/2603.27006"
---

# Superseded Figures

> **A correction to this note.** It previously said the Kobak figures came
> from a *withdrawn* preprint. arXiv 2406.07016 has five live versions and
> carries no withdrawal notice, so the figures were superseded by revision,
> not withdrawn. A note cataloguing other people's citation errors has to
> hold itself to the same standard, so the wording is corrected throughout
> and the change is recorded here rather than made silently.


Seven numbers and characterisations circulate widely in writing about AI slop.
This brain uses none of them. Each one is recorded here with the correction
attached rather than quietly dropped, because a figure that is deleted comes
back, and a figure that is contradicted in writing does not.

The `confidence` on this note is `contested` on purpose. Under the mapping in
[[Note Conventions]] a note inherits the weakest confidence of the sources it
depends on, and two of the sources catalogued below sit at `low`. A governance
register that discusses weak sources cannot outrank them.

## Register

| Id | Circulating figure | Status | Replacement |
| --- | --- | --- | --- |
| S1 | Kobak 10 percent and 30 percent | superseded preprint version | 13.5 percent floor, up to 40 percent |
| S2 | GitClear 7.1 percent code churn | discarded projection | 5.7 percent actual for 2024 |
| S3 | Pangram human em-dash baseline | self-contradictory vendor page | 32.3 per 10,000 words, independently measured |
| S4 | SynthID robustness "100 to 21 percent" | unverifiable | 87.6 to 5.4 percent from a named table |
| S5 | "tariff" as a Merriam-Webster runner-up | false | five named runners-up, none of them tariff |
| S6 | Wikipedia LLM rules called a policy | wrong status | content guideline |
| S7 | RLHF "only amplifies" markers | mischaracterisation | RLHF can also drive a marker to zero |

## S1. The Kobak preprint pair

The widely repeated pair is that 10 percent of 2024 biomedical abstracts showed
LLM involvement, rising to 30 percent in some subcorpora. Both numbers come from
the June 2024 preprint version, which the authors superseded. The peer-reviewed
version in Science Advances, recorded as kobak-excess-vocabulary, reports at
least 13.5 percent of 2024 PubMed abstracts processed with an LLM and up to 40
percent in some subcorpora. The ledger entry carries the instruction directly:
the 10 percent and 30 percent figures must not be used.

The correction moves in the direction that makes the finding stronger, which is
why it spreads slowly. People rarely go looking for a bigger number when the
small one already supports their argument.

## S2. The GitClear churn projection

gitclear-copilot-quality-2025 publishes a churn series: 3.1 percent in 2020,
3.3 percent in 2021 and 2022, 4.5 percent in 2023, a projection of 7.1 percent
for 2024, and an actual of 5.7 percent for 2024. The 7.1 percent number is the
projection. It was never measured, and the vendor's own report supplies the
actual that replaced it.

Two further distortions travel with it. The first is attribution to the wrong
report: the churn series is from the February 2025 report, not the 2026 one.
The second is that gitclear-maintainability-gap does not publish a churn level
at all; it reports two-week code churn at plus 15 percent, a rate of change
rather than a level. Quoting "7.1 percent churn in the latest GitClear report"
gets the number, the year, and the report wrong at once.

## S3. The Pangram em-dash baselines

pangram-supporting-evidence claims humans average 5 em dashes per 10,000 words
while model families range from 3 to 45. Elsewhere on the same page a summary
table gives a human figure of 2 against an AI figure of 17. The page states two
different human baselines, and supplies no sample size, no corpus description,
no methodology, no citation, and no date.

freeburg-last-fingerprint measures a human baseline of 3.23 em dashes per 1,000
words, equal to 32.3 per 10,000, roughly six to sixteen times the vendor
figures. That measurement carries its own caveats, recorded in S7. The point
here is narrower: a page that contradicts itself cannot be quoted as a measured
figure regardless of which of its two numbers happens to be closer to the truth.
[[Why Pangram Is Not Cited]] holds the longer argument, and
czuma-em-dash-prevalence is the citation this brain uses instead.

## S4. The unverifiable SynthID figure

A robustness claim circulates that SynthID detection falls from 100 percent to
21 percent under paraphrase, sourced to trade press. The underlying figure could
not be verified against any primary source and must not be cited.

There is a verified figure that does the same work. masrour-damage-humanizers
reports SynthID-Text true positive rate at a 5 percent false positive rate
falling from 87.6 percent to 5.4 percent after DIPPER paraphrase. It is a
sharper result than the unverifiable one and it comes with a named method. The
lesson is that dropping an unsourced number usually costs nothing, because if
the effect is real somebody measured it properly.

## S5. The Merriam-Webster runner-up

merriam-webster-woty-2025 records slop as the 2025 Word of the Year, defined as
digital content of low quality that is produced usually in quantity by means of
artificial intelligence. The runners-up were gerrymander, performative, touch
grass, six seven, and Lake Chargoggagoggmanchauggagoggchaubunagungamaugg. The
frequently repeated claim that "tariff" was a runner-up is false.

This is a small error with a useful property: it is trivially checkable, so a
document that contains it is a document whose easy claims were not checked.

## S6. Guideline, not policy

wikipedia-llm-guideline records an RfC that closed on 2026-03-20 by a 44 to 2
margin under SNOW, prohibiting the use of LLMs to generate or rewrite article
content, with two surviving exceptions: copyediting your own writing, and
LLM-assisted translation, both under mandatory human review.

It is a content guideline, not a policy. On Wikipedia the distinction is
substantive rather than cosmetic, and it changes what the document can be cited
for. Describing it as a policy overstates the authority of the very source you
are leaning on, which is the failure mode this register exists to catch.

## S7. What The Last Fingerprint actually says

freeburg-last-fingerprint is regularly summarised as showing that reinforcement
learning from human feedback amplifies stylistic markers such as the em dash.
That is half of it. The same preprint reports base Llama 3.1 8B at 0.49 em
dashes per 1,000 words against its instruction-tuned counterpart at 0.00. RLHF
eliminated the marker in that pair.

The paper's actual thesis is that em-dash rate is a signature of a specific
fine-tuning procedure rather than a universal AI tell. Read correctly it is an
argument for [[Marker Cohort Rot]], not an argument that markers are reliable.
It is also a single-author, unaffiliated, non-peer-reviewed preprint, and the
ledger requires that flag whenever it appears next to peer-reviewed work.

## Two standing caveats that are not corrections

- liang-gpt-detectors-biased must carry its sample size. The 61.3 percent
  false-positive rate on TOEFL essays comes from 91 essays across seven
  detectors, all written before 2020. The finding stands; the n travels with it.
- metr-developer-slowdown has a February 2026 follow-up that is a blog post
  rather than a paper, and it could not obtain a clean signal because developers
  increasingly refused to work without AI. Cite the randomized trial, describe
  the follow-up as what it is.

## Adding a row

1. Show the figure in circulation with at least one place it is used.
2. Retrieve the primary source and read the table the number came from.
3. Classify the defect: withdrawn version, projection quoted as measurement,
   self-contradiction, unverifiable, factually false, status error, or
   mischaracterisation.
4. Record the replacement figure and its ledger id, or record explicitly that
   no replacement exists.
5. Add the row above, then add a `limitations` line to the affected entry in
   `references/source-ledger.json` so the correction survives this note.
6. Re-run `scripts/score_substance.py` and the vault linter before release.

## Related

- [[Note Conventions]]
- [[Evidence Quality Ladder]]
- [[Why Pangram Is Not Cited]]
- [[Corpus Study Method]]
- [[The Code Slop Disagreement]]
- [[Package Hallucination Evidence]]
- [[Marker Cohort Rot]]
- [[Evidence Tiers]]
- [[Provenance Trace Policy]]
- [[What This Brain Does Not Claim]]
