---
type: "concept"
title: "Detector Bias Against Language Learners"
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
  - "[[The Firewall]]"
  - "[[Why Detection Fails]]"
  - "[[Human Expert Review]]"
  - "[[Evidence Tiers]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Moving Baseline Objection|Human Speech Is Converging]]"
  - "[[Excess Vocabulary]]"
  - "[[Superseded Figures]]"
  - "[[Model Fingerprints]]"
  - "[[Regulation and Governance]]"
source_urls:
  - "https://arxiv.org/abs/2512.09292"
  - "https://doi.org/10.1016/j.patter.2023.100779"
  - "https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/"
---

# Detector Bias Against Language Learners

Firewall rule 1 does not exist because detectors are inaccurate. It exists
because their inaccuracy is not evenly distributed, and the people it lands on
are the people least able to contest it. A false positive rate is an average.
Averages hide who pays.

## The current citation

The peer-reviewed source to use is Stowe, Afanaseva, Raimundo, Sun and Patil,
*Identifying Bias in Machine-generated Text Detection*, published at ACL 2026
(`stowe-detector-bias`). The study ran 16 detection models over student essays
labelled for gender, race and ethnicity, English-language-learner status, and
socioeconomic status. Three findings matter here, and all three are stated by
the authors rather than inferred:

- ELL essays were more likely to be flagged by machine-generated text detectors.
- Non-White ELL students were disproportionately flagged relative to White ELL
  peers, so the disparity is not explained by ELL status alone.
- Human annotators, judging the same essays, showed no significant demographic
  bias.

The third finding is the one that changes the design. It rules out the
comfortable reading that the essays themselves simply looked machine-like and
that any careful reader would have made the same mistake. Careful readers did
not make the same mistake. The disparity is a property of the detectors.

## The older citation and the caveat that travels with it

The figure most people reach for is from Liang, Yuksekgonul, Mao, Wu and Zou,
*GPT detectors are biased against non-native English writers*, Patterns
4(7):100779 (`liang-gpt-detectors-biased`): seven detectors misclassified 61.3
percent of TOEFL essays as AI-generated, and 19.8 percent of those essays were
flagged unanimously by every detector tested.

That figure may not be quoted in this vault without its sample size. **The study
used 91 essays and seven detectors, and the essays predate 2020.** Ninety-one
items is a small enough sample that the confidence interval around 61.3 percent
is wide, and a 2023 detector cohort is three model generations stale. The
finding has held up directionally, which is exactly why it is worth stating
precisely rather than loosely. Handling of figures like this is governed by
[[Superseded Figures]].

| Property | `liang-gpt-detectors-biased` | `stowe-detector-bias` |
| --- | --- | --- |
| Published | 2023-07-10, Patterns 4(7):100779 | 2025-12-12 preprint, ACL 2026 |
| Detectors tested | 7 | 16 |
| Corpus | 91 TOEFL essays, all pre-2020 | student essays with demographic labels |
| Headline number | 61.3 percent flagged, 19.8 percent unanimous | no single headline rate; disparity by group |
| Demographic breakdown | non-native English writers as one group | ELL status crossed with race and ethnicity |
| Human comparison | none | human annotators, no significant bias |
| Use in this vault | historical, always with n equals 91 | current citation for detector bias |

Use Stowe for any current claim. Use Liang when the history matters, when a
reader arrives quoting the 61.3 percent figure, or when the point is that this
problem was documented in 2023 and shipped anyway.

## Why the accusation is worse than the error rate suggests

Consider the arithmetic on a single cohort. OpenAI's own withdrawn classifier
labelled human-written text as AI-written 9 percent of the time
(`openai-classifier-withdrawal`). At that rate, a department screening 600
student essays produces roughly 54 false accusations per assignment, before any
demographic skew. Stowe's result says the skew is real, so those 54 are not
drawn uniformly from the cohort. They concentrate on the students whose prose
is more formulaic because they are writing in a second language, and who are
correspondingly less equipped to argue in an appeals process conducted in that
same language.

The convergence problem compounds this. Vocabulary that reads as machine-like
is entering ordinary human usage, which is documented in
[[The Moving Baseline Objection|Human Speech Is Converging]] and is the reason [[Marker Cohort Rot]] exists as
a standing maintenance obligation. A learner drilled on formal academic register
is being penalised for producing the register they were taught.

## Sentences this brain will not write

| Never | Instead |
| --- | --- |
| "This was written by AI." | "Three claims in this draft resolve to no source." |
| "This reads 87 percent AI." | "Section 2 fails [[The Deletion Test]]: nothing is lost when it is cut." |
| "The detector flagged you." | "This citation's DOI resolves to an unrelated paper." |
| "Non-native phrasing suggests generation." | Nothing. Register is not a defect. |
| "Confirm whether a model was used." | "Confirm whether the claim is supported." |

Every row on the right is checkable by a third party without trusting this
brain's judgment. That is the whole substitution: replace an unfalsifiable claim
about origin with a falsifiable claim about the artifact. The mechanics are in
[[Evidence Tiers]] and the standing rules in [[The Firewall]].

## If an accusation has already been made

This procedure is for the case where someone arrives with a detector score and
a decision to make. It is written to be handed over as-is.

1. Ask what population the tool's false-positive rate was measured on, and
   whether it was broken out by first language. If the answer is unknown, the
   score has no interpretable error bar for this person.
2. Ask the tool to name the spans that produced the score. Detectors cannot,
   which is failure 1 in [[Why Detection Fails]].
3. Set the score aside and check the artifact instead: do the references
   resolve, do the quoted sources say what is claimed, do the numbers reconcile.
4. Run [[The Attribution Test]] on every "studies show" or "experts say"
   construction. A fabricated citation is a defect regardless of origin.
5. If the artifact holds up, there is no finding. A defect-free document is not
   evidence of misconduct, whatever produced it.
6. If the artifact does not hold up, report the specific defect, cite the
   evidence, and let the origin question stay unanswered. It was never the
   thing that mattered.
7. Record the outcome so the same tool is not re-consulted for the next case.

## Related

- [[The Firewall]]
- [[Why Detection Fails]]
- [[Human Expert Review]]
- [[Evidence Tiers]]
- [[Marker Cohort Rot]]
- [[The Moving Baseline Objection|Human Speech Is Converging]]
- [[Superseded Figures]]
- [[The Attribution Test]]
- [[The Deletion Test]]
- [[Regulation and Governance]]
