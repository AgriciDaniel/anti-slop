---
type: "concept"
title: "Distributional Convergence"
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
  - "[[AI Slop]]"
  - "[[Model Collapse]]"
  - "[[Signs Are Not The Problem]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Em Dash|Em Dash Density]]"
  - "[[Excess Vocabulary]]"
  - "[[Model Fingerprints|Model Specific Fingerprints]]"
  - "[[The Moving Baseline Objection|Human Speech Is Converging Too]]"
  - "[[Evidence Tiers]]"
  - "[[Why Pangram Is Not Cited]]"
source_urls:
  - "https://arxiv.org/abs/2603.27006"
  - "https://arxiv.org/abs/2502.12150"
  - "https://arxiv.org/abs/2604.23178"
  - "https://arxiv.org/abs/2604.22142"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2409.01754"
---

# Distributional Convergence

Ask ten different people to describe a tradeoff and you get ten shapes of
sentence. Ask one model ten times and the shapes narrow. Distributional
convergence is the name for that narrowing: the tendency of generated text to
cluster around the high-probability centre of its training distribution rather
than spread across the range a population of humans would produce.

## The mechanism, stated as a chain

1. **Next-token prediction rewards the likely continuation.** A decoder trained
   to minimise prediction loss is trained, in effect, to prefer the phrasing
   that most often followed this context in the corpus. Unusual phrasing is
   penalised by construction, not by accident.
2. **Decoding narrows it further.** Sampling strategies that trim the tail
   (temperature below one, top-p, top-k) trade variance for coherence. The
   trade is deliberate and usually correct for the user, and it is also a
   second contraction of the output distribution on top of the first.
3. **Preference tuning applies a third contraction.** Post-training on human or
   model preference data pulls output toward whatever the preference signal
   rewarded. The direction is not neutral: judge style preference has been
   measured at 0.10 to 0.76 across models, with markdown-formatted answers
   preferred over the same content in plain text, against a position bias of
   0.04 or less (`soumik-judging-the-judges`). Verbosity bias is
   family-specific in the same work: Gemini and Llama at plus 0.24 to plus
   0.44, Claude at minus 0.12, GPT-4o at minus 0.04.
4. **The result is a mode, not a voice.** What survives three contractions is
   the average of a genre, which is why generated text across unrelated topics
   feels like it came from one writer.

Steps one and two are architectural facts about how these systems are built and
sampled. Step three is measured. Step four is the observation this vault is
built to act on, and it is the point where evidence gets thin enough that the
note carries a `contested` confidence.

## What is actually measured, and what is inference

| Claim | Status | Source |
| --- | --- | --- |
| Model output carries stable, attributable stylistic signatures | measured, 97.1 percent five-way attribution accuracy, signal survives rewriting, translation and summarization | `sun-idiosyncrasies` |
| Preference judges systematically favour markdown-heavy formatting | measured, style bias 0.10 to 0.76 | `soumik-judging-the-judges` |
| Revision by a model pulls texts toward a shared point in feature space | measured on 300 personal narratives across 3 models | `vannuenen-voice-under-revision` |
| Vocabulary in a real-world corpus shifted toward model-preferred words | measured, at least 13.5 percent of 2024 PubMed abstracts LLM-processed, up to 40 percent in some subcorpora | `kobak-excess-vocabulary` |
| Markdown-heavy training data is the cause of the prose style | not established, argued | `freeburg-last-fingerprint` |

The bottom row is the one to be careful with, and it is the reason this note
does not lead with the markdown story even though the markdown story is the
most satisfying version of the argument.

## The markdown hypothesis, with its caveat attached

Freeburg's preprint argues that em-dash rate is the signature of a specific
fine-tuning procedure rather than a universal property of machine text, and
reports a measured human baseline of 3.23 em dashes per 1,000 words, equal to
32.3 per 10,000 (`freeburg-last-fingerprint`). It also reports the direction
that is usually left out: instruction tuning can remove the marker as easily as
add it, with base Llama 3.1 8B at 0.49 per 1,000 words and the
instruction-tuned variant at 0.00.

That last figure is the useful part, because it breaks the folk model in which
markers accumulate monotonically. It is also, and this must travel with every
use of the source, a single-author, unaffiliated, non-peer-reviewed preprint.
The vault records it at low ledger confidence, and it must never be quoted
shoulder to shoulder with peer-reviewed work without that flag. Where it is
used to contradict vendor marketing it is doing honest work, as set out in
[[Why Pangram Is Not Cited]]. Where it is used to explain causation it is
carrying more weight than one preprint can bear.

## Convergence is not uniformity

Two findings cut against the naive reading that all models converge on the same
point. First, attribution works: five-way model identification reaches 97.1
percent accuracy and the signal survives paraphrase, translation and
summarization (`sun-idiosyncrasies`). If every model produced the same
distribution, no attribution would be possible at all. Models converge within
themselves more than a human population does, while remaining separable from
each other.

Second, the target moves. Words preferentially generated by ChatGPT rose
abruptly in spontaneous human speech, with delve up 48 percent, realm up 35
percent and adept up 51 percent within 18 months of release, and a
preregistered experiment with n equal to 496 confirmed the entrenchment in
active vocabulary (`yakura-spoken-convergence`). The corpus that defines the
baseline is being reshaped by the thing being measured against it. That is a
convergence between populations, not just within one, and it is the strongest
argument in the vault against treating any word list as durable. The
consequence is worked out in [[Marker Cohort Rot]] and
[[The Moving Baseline Objection|Human Speech Is Converging Too]].

## The sibling note in the Gogh vault

This idea has an older home. The Gogh vault, at
the Gogh vault (a sibling brain covering visual and frontend slop), carries a
`wiki/concepts/Distributional Convergence.md` that treats the same mechanism in
the visual domain: unguided frontend generation collapsing onto a recognisable
default of one neutral sans-serif, purple-to-blue gradients on white, rounded
cards and minimal motion. The two vaults share a mechanism and split a scope.
Gogh owns the visual surface, generated interfaces and design output. This
vault owns prose, code, documentation and agent output. Neither should restate
the other's evidence; cross-link instead. The Gogh treatment is also where
[[Constraint Beats Coaxing]] originates.

## What follows for repair

Convergence explains why signs cluster, which is exactly why removing signs is
not repair. If the flatness is a property of the sampling process, then editing
the surface leaves the process untouched and produces a text that is flat and
harder to notice. Van Nuenen's result is the mechanical demonstration: LLM
revision reduces function words, contractions and first-person pronouns while
raising vocabulary diversity and word length, and rewritten texts converge in
feature space regardless of where they started, even under explicit
instructions to preserve the author's voice (`vannuenen-voice-under-revision`).
The doctrine that follows is in [[Signs Are Not The Problem]], and the
structural tests that do the real work are [[The Deletion Test|Deletion Test]],
[[The Inversion Test|Inversion Test]] and [[The Stranger Test|Stranger Test]].

## Related

- [[AI Slop]]
- [[Signs Are Not The Problem]]
- [[Model Collapse]]
- [[Marker Cohort Rot]]
- [[Model Fingerprints|Model Specific Fingerprints]]
- [[The Moving Baseline Objection|Human Speech Is Converging Too]]
- [[The Em Dash|Em Dash Density]]
- [[Excess Vocabulary]]
- [[Why Pangram Is Not Cited]]
- [[Constraint Beats Coaxing]]
- [[Evidence Tiers]]
