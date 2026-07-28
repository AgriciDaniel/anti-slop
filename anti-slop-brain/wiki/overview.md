---
type: "overview"
title: "Overview"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/overview"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[Signs Are Not The Problem]]"
  - "[[Why Structural Not Judgmental]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[What This Brain Does Not Claim]]"
  - "[[The ESL Objection]]"
  - "[[research-pack-2026-07-27|Research Pack 2026-07-27]]"
source_urls:
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2512.09292"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
---

# Overview

This brain finds and repairs substance defects in AI-assisted work. It does not
identify who or what wrote anything, and it is built so that it cannot.

## The problem with the obvious approach

The obvious approach is to ask a model whether a piece of text looks like slop.
That approach is measurably broken. Agreement between LLM judges and human slop
labels sits at kappa 0.01 for GPT-5, minus 0.01 for DeepSeek-V3, and 0.03 for
o3-mini, with models under-flagging by roughly five times relative to human
annotators (source `shaib-measuring-slop`). Kappa near zero means the judge is
performing at chance.

The bias then runs the wrong way. GPT-4 preferred model-written pitches 89
percent of the time against human raters at 36 percent (`laurito-ai-ai-bias`,
peer reviewed in PNAS, though the human baseline is only n equal to 13 across
both datasets and the authors call the findings not definitive). Judge
preference does not track factuality or safety (`feuer-style-over-substance`).
Markdown-heavy formatting is preferred over plain text with a style bias up to
0.76 (`soumik-judging-the-judges`).

There is a related finding about self-gating, and it must be scoped carefully.
`song-rubber-stamp-regime` measures **recursive self-training across model
generations**, not single-pass self-review before delivery: when a code model
is repeatedly retrained on its own gated output, AI self-gating "degenerates to
ungated self-training" and enters a "rubber-stamp regime where acceptance
scores rise while benchmark correctness falls." That is a strong result about
training loops and a suggestive one about review loops, not a measurement of
the latter. It is tiered `CONTESTED` in the ledger. The same paper also finds
that human gates slow but do not stop the collapse, which cuts against the
obvious remedy.

So the judge is both inaccurate and biased toward the exact features that
define the thing it is supposed to catch. See [[Why Structural Not Judgmental]].

## What this brain does instead

Every check is a mechanical procedure that emits an artifact somebody can
inspect.

| Layer | Mechanism | Example output |
|---|---|---|
| 0 | Deterministic scanners | A line number and a matched residue token |
| 1 | Structural procedures | A deleted span and the named thing that was lost |
| 2 | Evidence-tiered signals | A routed procedure, never a verdict |

The five procedures are the deletion test, the inversion test, the stranger
test, the attribution test, and the load-bearing test. Each is documented in
`procedures/` with a worked artifact, not a description of an artifact.

## Why it refuses to detect authorship

Detectors fail, and they fail on identifiable people. Sixteen detection models
disproportionately flagged English-language-learner essays, and non-White ELL
students more than White ELL peers, while human annotators on the same essays
showed no significant demographic bias (`stowe-detector-bias`, ACL 2026).
OpenAI withdrew its own classifier at 26 percent true positive and 9 percent
false positive (`openai-classifier-withdrawal`).

Model attribution is technically achievable: 97.1 percent five-way accuracy,
surviving rewriting and translation (`sun-idiosyncrasies`). This brain still
refuses it. Capability is not licence. See [[Model Fingerprints]] and
[[The ESL Objection]].

## Why it refuses to be a humanizer

Wikipedia's guide, the source most of this field derives from, warns in bold
that the listed patterns are only potential signs of a problem and not the
problem itself, and that treating the signs as the thing to fix "could just
make detection harder" (`wikipedia-signs-of-ai-writing`). The measurement
agrees: humanizers degrade the text they edit, winning a fluency comparison
against the original only 26.0 percent of the time at best tier
(`masrour-damage-humanizers`). Those win rates are **GPT-4o judgements over 25
samples per tool, not human ratings**, which matters given everything above
about model judges; [[Humanizers]] sets out why the finding still carries
weight despite that and despite its detector-vendor authorship. See
[[Signs Are Not The Problem]].

## What it is graded by

This vault is measured by its own subject matter. `scripts/score_substance.py`
enforces near-duplicate similarity below 0.82, heading skeleton reuse of at
most 3, anchor reuse of at most 2, a floor of 120 note-specific words, and
citation coverage of 0.95. A brain about padded generic writing that was itself
padded and generic would refute its own thesis. See [[Knowledge Base Surface]].

## Limits

Stated in full in [[What This Brain Does Not Claim]]. The short version: marker
lists rot, the code-slop literature is genuinely unsettled, and several 2026
citations are preprints verified at abstract level only and tagged accordingly.
