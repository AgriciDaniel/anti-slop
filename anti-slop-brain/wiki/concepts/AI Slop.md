---
type: "concept"
title: "AI Slop"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/concept"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Signs Are Not The Problem]]"
  - "[[Distributional Convergence]]"
  - "[[Workslop]]"
  - "[[The Generation Verification Asymmetry]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
  - "[[The Accessibility Objection|Slop Is Not Always Worse]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Note Conventions]]"
  - "[[Marker Cohort Rot]]"
source_urls:
  - "https://simonwillison.net/2024/May/8/slop/"
  - "https://www.merriam-webster.com/wordplay/word-of-the-year"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2605.19936"
  - "https://arxiv.org/abs/2512.09292"
---

# AI Slop

Slop is the only load-bearing term in this vault that arrived from the open
internet rather than from a paper, and the three groups who use it most do not
mean the same thing by it. Getting the disagreement on the table first is not
pedantry. Each of the three readings implies a different tool, and two of them
imply tools this vault refuses to build.

## Three definitions in circulation

**The behavioural definition.** Simon Willison's May 2024 post is the canonical
origin, and it is deliberately not about quality. Its formulation is that not
all AI-generated content is slop, but content that is mindlessly generated and
thrust upon someone who did not ask for it earns the name
(`willison-slop`). The defect sits in the act of publication: low effort on the
sender's side, imposed cost on the receiver's side. Willison extended the
coinage the following day with `slom` for the AI-generated subset of spam, a
proposal that did not catch on. This source is an influential essay, not a
study, and is cited here only for the definition it established.

**The lexicographic definition.** Merriam-Webster selected slop as its 2025
Word of the Year on 2025-12-15 and defined it as digital content of low quality
that is produced usually in quantity by means of artificial intelligence
(`merriam-webster-woty-2025`). This packs three conditions into one phrase:
low quality, high volume, and machine origin. The American Dialect Society
independently selected the same word, voting 2026-01-09. Two cautions apply.
The announcement had to be verified through wire copy because the publisher
blocks automated retrieval, and the widely repeated claim that "tariff" was a
runner-up is false: the actual runners-up were gerrymander, performative, touch
grass, six seven, and Lake Chargoggagoggmanchauggagoggchaubunagungamaugg.

**The annotator's definition.** A third meaning is implicit in how slop is
actually measured. Shaib and colleagues treat slop as whatever trained human
annotators mark at span level in a labelled corpus (`shaib-measuring-slop`).
Under that operationalisation humans flag spans at a rate of 0.34 while models
flag at 0.03 to 0.08, and agreement between LLM judges and human labels is near
zero: kappa 0.01 for GPT-5, minus 0.01 for DeepSeek-V3, 0.03 for o3-mini. Slop
here is neither a property of origin nor a property of intent. It is a property
a competent reader can point at.

## Where the three definitions actually conflict

| Reading | Locus of the defect | Needs AI origin | Needs deception | Decidable from the artifact alone |
| --- | --- | --- | --- | --- |
| Behavioural (`willison-slop`) | the act of publishing | yes, in practice | no, imposition is enough | no, requires knowing how it was sent |
| Lexicographic (`merriam-webster-woty-2025`) | quality plus volume | yes, by definition | no | no, origin is not visible |
| Annotator (`shaib-measuring-slop`) | spans in the text | no | no | yes |

The table is the argument. Only the third row survives contact with a tool that
has to run on a file it was handed. The first two both require a fact about
provenance that is not recoverable from the artifact, and attempts to recover
it are exactly where the harm lives: detector-based origin inference
disproportionately flags English-language-learner essays, and flags non-White
ELL students more than their White ELL peers, while human annotators on the
same essays showed no significant demographic bias (`stowe-detector-bias`).

## The definition this vault adopts

Slop is a set of named, inspectable defects in an artifact, held independently
of who or what produced it.

That is the annotator's reading with the origin condition deleted. Three
reasons for the choice, in descending order of importance.

1. It is the only reading compatible with [[The Firewall]]. A rule that fires
   on origin is a rule that produces authorship verdicts, and this vault never
   emits one. See [[Detector Bias Against Language Learners]] for the harm
   ledger behind that rule.
2. It is the only reading that survives being wrong about provenance. A
   fabricated citation is a defect whether a person or a model wrote it. A
   hallucinated package import breaks the build either way.
3. It keeps the behavioural insight without needing to prove it. Willison's
   point about imposed cost is preserved downstream in
   [[The Generation Verification Asymmetry]] and measured concretely in
   [[Workslop]], where it belongs, rather than smuggled into the definition.

What the vault gives up by this choice is the ability to say a clean, correct,
well-sourced document is slop merely because a machine wrote it. That is a real
loss for some readers. It is accepted deliberately.

## The complication that should stop anyone declaring victory

Slop is usually assumed to be worse writing. That premise is not safe. Miletic
and Falk found that LLM-modified academic text shows lower lexical diversity
than the unmodified original, and that expert readers nonetheless rated the
modified text as more understandable and more exciting
(`miletic-lexical-diversity`). Lower diversity, higher reported comprehension.
The finding is a preprint verified at abstract level and should be carried at
that weight, but it is directly on point: a measurable stylistic flattening can
coexist with a reader-side improvement.

This is why the vault splits severity from confidence, and why it refuses to
treat any single stylistic feature as a defect on its own. The argument is
worked out in [[The Accessibility Objection|Slop Is Not Always Worse]] and the routing rule is in
[[Evidence Tiers]].

## What follows for everything downstream

- Markers never conclude. They route to a procedure. See
  [[Signs Are Not The Problem]] for the doctrine and the marker folder for the
  individual cohorts, including [[Excess Vocabulary]] and [[The Em Dash|Em Dash Density]].
- Anything that cannot be checked mechanically gets checked by a structural
  test with a written artifact, not by asking a model for a rating. The reason
  is the kappa figures above, developed further in
  [[Why Structural Not Judgmental|LLM As Judge Fails At Slop]].
- Volume, the "produced usually in quantity" half of the dictionary
  definition, is a distribution problem rather than a text problem. It is
  handled in [[Workslop]] and in the surface notes such as
  [[Commit and Review Surface|Pull Request Descriptions]] and [[Agent Output Surface|Chat And Agent Output]].
- The word itself will drift. Marker vocabulary already does, and the same
  pressure applies to the term. See [[Marker Cohort Rot]].

## Related

- [[Signs Are Not The Problem]]
- [[The Generation Verification Asymmetry]]
- [[Distributional Convergence]]
- [[Workslop]]
- [[The Accessibility Objection|Slop Is Not Always Worse]]
- [[Evidence Tiers]]
- [[The Firewall]]
- [[Detector Bias Against Language Learners]]
- [[Marker Cohort Rot]]
- [[Note Conventions]]
