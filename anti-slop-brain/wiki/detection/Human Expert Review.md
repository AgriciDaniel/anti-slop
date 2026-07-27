---
type: "flow"
title: "Human Expert Review"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/flow"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Why Detection Fails]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[The Firewall]]"
  - "[[Signs Are Not The Problem|Signs of AI Writing]]"
  - "[[Evidence Tiers]]"
  - "[[The Stranger Test]]"
  - "[[The Deletion Test]]"
  - "[[Humanizers]]"
  - "[[Prose Surface]]"
  - "[[Marker Cohort Rot]]"
source_urls:
  - "https://arxiv.org/abs/2501.15654"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/"
  - "https://arxiv.org/abs/2512.09292"
---

# Human Expert Review

Five people reading carefully beat every automated system in the one study that
put them side by side. That result is the strongest positive finding in this
folder, and it is also the most easily misused, because it is a finding about
experienced readers working as a panel, not about anyone's confident hunch.

## The measurement

Russell, Karpinska and Iyyer, published at ACL 2025, recruited annotators who
frequently use ChatGPT for writing tasks and had them classify 300 articles. A
majority vote of five such annotators misclassified **1 of 300**
(`russell-expert-detectors`). The same paper reports that these expert humans
outperformed commercial and open-source detectors, and that the advantage held
under paraphrase evasion, which is the attack that collapses the automated
systems described in [[Humanizers]].

Three qualifiers keep this from being over-read:

- The unit is a **majority vote of five**, not one reader. A single annotator's
  accuracy is not the reported figure, and the vote is doing real work.
- The annotators were selected for **frequent hands-on use** of the tools. This
  is domain familiarity, not general intelligence or seniority.
- The task was **article-length text**. Nothing here supports sentence-level
  judgments, and this vault does not make them.

## The false-positive budget

The arithmetic below is what converts a percentage into a decision. Rates are
drawn from different corpora and different years, so this is a comparison of
scale, not a controlled head-to-head benchmark. Read it that way.

| Reviewer | Reported error | Wrong calls per 1,000 items | Ledger id |
| --- | --- | --- | --- |
| Majority vote of five experts | 1 misclassified of 300 | about 3 | `russell-expert-detectors` |
| OpenAI classifier on human text | 9 percent false positive | 90 | `openai-classifier-withdrawal` |
| Seven detectors on TOEFL essays | 61.3 percent flagged, n equals 91 | 613 on that population | `liang-gpt-detectors-biased` |

Now attach a cost. In a 1,000-item review where a wrong call triggers a formal
process, the expert panel generates roughly three of those processes and the
withdrawn classifier generates ninety. If each process costs the organisation
two hours and costs the accused person considerably more, the classifier is not
a cheaper option that trades a little accuracy for scale. It is an expensive
option whose costs are paid by someone who does not appear in the budget, and
whose distribution is skewed by the demographic disparity documented in
[[Detector Bias Against Language Learners]] (`stowe-detector-bias`).

The operational implications follow directly:

- Panels are affordable only for **rare, high-stakes** items. Five experts on
  every submission does not scale, and the study does not claim it should.
- For everything else, do not run an origin judgment at all. Run the structural
  procedures, which cost one reader and produce a checkable artifact.
- Never substitute one reader for the panel and keep the panel's accuracy claim.
  That is the most common misreading of this result.

## What Wikipedia does instead of buying software

Wikipedia's *Signs of AI writing* guide is the largest maintained
practitioner artefact in this space, and it is notable for what it does not
contain: it does not route editors to detector software
(`wikipedia-signs-of-ai-writing`, single-source for this practice claim,
practitioner tier). It documents patterns, and then explicitly warns that the
patterns listed are only potential **signs** of a problem rather than the
problem itself, and that treating the signs as the things to fix could just make
detection harder. It also maintains an ineffective-indicators list, a set of
signals editors are told not to treat as evidence, which is a governance move
almost no vendor makes.

The design lesson this vault takes from that guide is in [[Signs Are Not The Problem|Signs of AI Writing]]
and in [[Evidence Tiers]]: a marker is a routing device, never a conclusion.
The guide's markup and citation taxonomies, covering vendor residue such as
`oaicite` tokens and tracking parameters, and fabricated references with invalid
DOIs, are exactly the checks that are decidable, and they are handled
deterministically here rather than by any reader's judgment.

## Procedure: convening a review panel

Use this only when the item is high-stakes, the artifact-level checks have
already run, and a defect has been found that requires a judgment call about
seriousness. It is not an origin panel, and its output is never a verdict about
authorship.

1. Confirm the deterministic scans have already run and record their output.
   Residue, placeholders, unresolved references and non-existent packages are
   decided before anyone is convened.
2. State the question in artifact terms. Good: "does section 3 support its
   central claim". Not permitted: "was this generated".
3. Recruit five reviewers with hands-on familiarity with the tooling in the
   relevant surface, matching the selection criterion in
   `russell-expert-detectors`.
4. Give each reviewer the full item. Do not give them a detector score, a
   marker count, or each other's notes. Priming destroys the independence the
   majority vote depends on.
5. Require each reviewer to name a span and state what is wrong with it. A
   reviewer who cannot name a span has not produced a finding.
6. Aggregate by majority. Record dissent verbatim rather than resolving it.
7. Route every surviving finding to the matching structural procedure:
   [[The Deletion Test]] for suspected padding, [[The Stranger Test]] for
   suspected genericness, [[The Attribution Test]] for suspected
   over-attribution.
8. Report defects with severity and confidence on separate axes, per
   [[The Firewall]]. Merge them and the report becomes uninterpretable.
9. Log the panel's own error when the outcome is later known, and feed it into
   [[Marker Cohort Rot]] review. A panel that is never scored drifts.

## When not to convene one

- Routine drafts, internal documents, and anything reversible. The cost is not
  justified and the structural procedures already cover the ground.
- Anything where the real question is a policy question. Whether disclosure was
  required is answered in [[Regulation and Governance]], not by readers.
- Sentence-level or paragraph-level items. The evidence covers article-length
  text and does not transfer down.

## Related

- [[Why Detection Fails]]
- [[Detector Bias Against Language Learners]]
- [[The Firewall]]
- [[Signs Are Not The Problem|Signs of AI Writing]]
- [[Evidence Tiers]]
- [[The Stranger Test]]
- [[The Deletion Test]]
- [[The Attribution Test]]
- [[Humanizers]]
- [[Regulation and Governance]]
- [[Marker Cohort Rot]]
