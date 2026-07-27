---
type: "concept"
title: "Model Fingerprints"
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
  - "[[Why Detection Fails]]"
  - "[[The Firewall]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Distributional Convergence]]"
  - "[[Evidence Tiers]]"
  - "[[Marker Cohort Rot]]"
  - "[[Signs Are Not The Problem]]"
  - "[[The ESL Objection]]"
  - "[[What This Brain Does Not Claim]]"
  - "[[Human Expert Review]]"
source_urls:
  - "https://arxiv.org/abs/2502.12150"
  - "https://arxiv.org/abs/2604.03136"
  - "https://arxiv.org/abs/2604.19139"
  - "https://arxiv.org/abs/2512.09292"
  - "https://arxiv.org/abs/2605.19516"
---

# Model Fingerprints

Working out which model produced a piece of text is a solved problem to an
uncomfortable degree. That sentence is the whole difficulty of this note. Most
of `detection/` documents things that do not work; this one documents something
that does, and then explains why this brain will not use it.

## The capability, measured

Two studies carry the claim. Neither is a vendor product page.

`sun-idiosyncrasies`, published at ICML 2025, reports **97.1 percent accuracy on
five-way model attribution** across ChatGPT, Claude, Grok, Gemini, and DeepSeek.
The result that makes it interesting is not the headline number but its
robustness: the signal survives rewriting, translation, and summarization. A
paraphrase pass that walks an origin detector out of its decision boundary, the
effect reported in `xu-base-models-look-human` at 100 percent human probability
by round 10, does not remove the family signature.

`russell-storyscope` approaches the same question from narrative structure
rather than surface form. Across **61,608 stories**, it separates human from AI
authorship at **93.2 percent macro-F1 using narrative and discourse features
alone**, with no lexical or punctuation features involved, and reaches **68.4
percent on six-way model attribution**. Its per-family finding is worth stating
because it is specific rather than atmospheric: the Claude signature is
**notably flat event escalation**, meaning the tension curve of a story rises
less steeply than a human writer's does.

| Study | Task | Result | Robustness | Ledger id |
| --- | --- | --- | --- | --- |
| Idiosyncrasies in LLMs | five-way model attribution | 97.1 percent accuracy | survives rewriting, translation, summarization | `sun-idiosyncrasies` |
| Idiosyncrasies in LLMs | families covered | ChatGPT, Claude, Grok, Gemini, DeepSeek | not stated beyond the five | `sun-idiosyncrasies` |
| StoryScope | human against AI, narrative features only | 93.2 percent macro-F1 | not tested under paraphrase attack | `russell-storyscope` |
| StoryScope | six-way model attribution | 68.4 percent accuracy | same | `russell-storyscope` |
| StoryScope | Claude-specific signature | flat event escalation | structural, not lexical | `russell-storyscope` |
| Verbal Tic Index | per-model tic density | Gemini 3.1 Pro 0.590, Claude Opus 4.7 0.317 | cohort-specific, rots with releases | `wu-verbal-tics` |

`sun-idiosyncrasies` is `high` confidence and tier EVIDENCE-BASED.
`russell-storyscope` and `wu-verbal-tics` are preprints verified at abstract
level, capped at `medium` and tier CONTESTED, which is why this note is tagged
`practitioner` overall.

## Where the capability stops

Family attribution and authorship are different questions, and the gap between
them is not narrow.

- Attribution assumes the text came from one of the candidate models. Given
  five choices and a text from a sixth model or from a person, a five-way
  classifier still returns one of five answers.
- The StoryScope numbers come from a fiction corpus. Nothing in the ledger
  establishes that a 68.4 percent six-way result transfers to a pull request
  description or a support email.
- Model cohorts turn over every few months. The Verbal Tic Index entry in the
  ledger carries the warning explicitly: the model roster differs between
  versions, so per-model numbers are cohort-specific and will rot. That is the
  same decay documented in [[Marker Cohort Rot]].
- A fingerprint identifies a generator, not a workflow. Text drafted by a
  person and edited by a model, or drafted by a model and rewritten by a
  person, has no single correct label.

## Why this brain refuses it anyway

Every limit above is a reason for caution. None of them is the reason for the
refusal, because all of them could be fixed by better work and the refusal
would still stand.

The refusal is rule 1 of [[The Firewall]]: never emit an authorship verdict.
Attribution **is** an authorship verdict. A five-way model attribution is not
adjacent to the forbidden output, it is the forbidden output with a model name
attached instead of a probability. Reporting "this text is 97 percent likely to
be Claude output" and reporting "this text is 97 percent likely to be machine
written" are the same act, and the second one is what [[Why Detection Fails]]
exists to rule out.

The cost of being wrong lands where it always lands. `stowe-detector-bias`, peer
reviewed at ACL 2026, ran sixteen detection models over student essays labelled
for demographic attributes and found English-language-learner essays
disproportionately flagged, and non-White ELL students disproportionately
flagged relative to their White ELL peers, while human annotators on the same
essays showed no significant demographic bias. Fingerprinting is a more accurate
instrument pointed at the same target. Improving accuracy does not remove the
victim; it makes the accusation harder to argue with. See
[[Detector Bias Against Language Learners]] and [[The ESL Objection]].

**Capability is not licence.** A brain that adopts a technique because the
technique works, without asking what the output would be used for, has no
principle left to refuse anything with. This note exists so that the refusal is
recorded next to the strongest evidence against it rather than in its absence,
which is the standard [[What This Brain Does Not Claim]] sets.

## What the capability is legitimately good for

Attribution research is not wasted work. It is aimed at the wrong consumer when
it is aimed at accusation.

| Use | Who benefits | Why the firewall does not bite |
| --- | --- | --- |
| Model evaluation and release comparison | the lab shipping the model | the generator is known, so nothing is being inferred about a person |
| Measuring stylistic convergence between families | corpus researchers | the unit of analysis is a population, not a document |
| Detecting training-data contamination between models | model developers | the subject is a model, not an author |
| Auditing whether a fine-tune drifted toward a base family | teams running fine-tunes | the ground truth is already known internally |
| Quantifying how a marker decays across cohorts | this vault, for [[Marker Cohort Rot]] | the output is a decay rate, not a label on a text |

The distinction is the identity of the subject. When the subject is a model,
attribution is measurement. When the subject is a person holding a document,
attribution is an allegation. `sun-idiosyncrasies` and `russell-storyscope` are
excellent at the first job. This brain uses their findings the way it uses
[[Distributional Convergence]]: as evidence that outputs cluster, which is a
population fact, and never as a per-document label.

## If someone asks this brain to attribute

1. State that the request is for an authorship or origin verdict, in those
   words, so the person can confirm that is what they meant.
2. Decline the verdict and cite rule 1 of [[The Firewall]], not a capability
   limitation. Declining on capability grounds is dishonest here, because the
   capability exists.
3. Offer the substitute: a defect report naming location, severity, confidence,
   and the artifact that convicted, under [[Evidence Tiers]].
4. If the underlying worry is quality rather than origin, run the structural
   procedures against the artifact and report what survives deletion and what
   does not. That answers the real question.
5. If the underlying need is genuinely adjudicative, for example an academic
   integrity case, route to [[Human Expert Review]], where five expert
   annotators voting by majority misclassified 1 of 300 articles, and record
   that the process is human and contestable.
6. Never store the model's guess about origin, even unreported. A stored guess
   leaks into the next answer.

## The narrower reading this vault does take

One thing from `russell-storyscope` is usable without touching origin. If a
93.2 percent separation is achievable from narrative and discourse features
with no lexical features at all, then the differences that matter are
**structural**, not decorative. Flat event escalation is a story problem, not a
punctuation problem. That is the same conclusion [[Signs Are Not The Problem]]
reaches from the opposite direction, and it is why [[Why Structural Not Judgmental]]
governs the procedures rather than any marker list.

## Related

- [[Why Detection Fails]]
- [[The Firewall]]
- [[Detector Bias Against Language Learners]]
- [[Distributional Convergence]]
- [[Evidence Tiers]]
- [[Marker Cohort Rot]]
- [[Signs Are Not The Problem]]
- [[The ESL Objection]]
- [[Human Expert Review]]
- [[Note Conventions]]
- [[overview|Overview]]
