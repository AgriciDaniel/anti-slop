---
type: "concept"
title: "The Moving Baseline Objection"
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
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[Marker Cohort Rot]]"
  - "[[Excess Vocabulary]]"
  - "[[The Em Dash]]"
  - "[[Evidence Tiers]]"
  - "[[Distributional Convergence]]"
  - "[[Model Fingerprints]]"
  - "[[The ESL Objection]]"
  - "[[Superseded Figures]]"
  - "[[Vendor Residue Markers]]"
source_urls:
  - "https://arxiv.org/abs/2409.01754"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2604.19139"
  - "https://arxiv.org/abs/2603.27006"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
---

# The Moving Baseline Objection

A marker list is a photograph of a distribution that was already moving when
the shutter opened. The objection here is not that any particular marker is
wrong. It is that a marker can be measured correctly, published correctly, and
be stale by the time it is applied, because both things it compares are in
motion: what models emit changes with each release, and what humans write
changes as they read model output.

If that is true, a marker list does not describe the present. It describes the
period its corpus was drawn from.

## The measurement that makes this concrete

`yakura-spoken-convergence` is the sharpest available version of the human half.
The corpus is more than 740,000 hours of audio across 824,634 podcast episodes
and 20,000 academic YouTube channels, and the question is whether words
preferentially produced by ChatGPT show up in spontaneous human speech after
its release. They do, abruptly.

| Word | Rise in spontaneous human speech | Window |
| --- | --- | --- |
| delve | 48 percent | 18 months from ChatGPT's release |
| realm | 35 percent | 18 months from ChatGPT's release |
| adept | 51 percent | 18 months from ChatGPT's release |

Spontaneous speech is the load-bearing detail. These are not people editing a
document with a model open in another tab. A preregistered experiment with n
equal to 496 accompanies the corpus work and confirms entrenchment in active
vocabulary, which is what separates this from a fashion in written style.

The source is a preprint verified at abstract level, tiered `CONTESTED`, and
its corpus arm infers the causal direction rather than isolating it. This note
carries `contested` confidence for that reason and does not claim more.

Take the finding at its weakest reading and the objection still lands. Whatever
caused it, delve is now a more common human word than it was when it entered
the marker lists, and every list that still treats it as a signal is measuring
a gap that has partly closed.

## Two independent signs that cohorts are already dated

The human half is only half. Two further ledger sources show the model half
moving too, on a shorter clock.

`wikipedia-signs-of-ai-writing` maintains dated per-era vocabulary cohorts and
states directly that AI vocabulary shifts by model era. That is a practitioner
guide rather than a study, and it is a living document that changes
continuously, snapshot taken 2026-07-27. Its value here is that the people
maintaining the most-copied marker list in existence found it necessary to
version their vocabulary by period. They would not have done that if the list
were stable.

`wu-verbal-tics` supplies the per-model version. Its Verbal Tic Index across
eight frontier models runs from Gemini 3.1 Pro at 0.590, through GPT-5.4 at
0.411 and Claude Opus 4.7 at 0.317, down to DeepSeek V3.2 at 0.295, measured
over 160,000 responses. The ledger records the crucial limitation: the model
roster differs between versions of the paper, so the per-model numbers are
cohort-specific and will rot. A number attached to a model name expires when
that model is replaced, which in this field is measured in months.

`freeburg-last-fingerprint` shows the third and least intuitive mechanism. It
reports base Llama 3.1 8B at 0.49 em dashes per 1,000 words against its
instruction-tuned counterpart at 0.00. Fine-tuning eliminated the marker. The
paper's actual thesis is that em-dash rate is a signature of a particular
fine-tuning procedure rather than a universal tell. It is a single-author,
unaffiliated, non-peer-reviewed preprint and must carry that flag wherever it
appears beside peer-reviewed work. Read carefully, it says a vendor can zero a
marker in one release without telling anyone, and the list will keep looking
for it.

## What rots, and at what speed

| Marker class | What ages it | Observable symptom of rot | Ledger anchor |
| --- | --- | --- | --- |
| Single vocabulary items | human uptake of model vocabulary | human baseline rises, gap narrows | `yakura-spoken-convergence` |
| Per-era vocabulary cohorts | model releases | the cohort's words stop discriminating | `wikipedia-signs-of-ai-writing` |
| Per-model tic indices | roster turnover | the named model no longer exists | `wu-verbal-tics` |
| Punctuation density | fine-tuning changes | marker inverts or goes to zero | `freeburg-last-fingerprint` |
| Aggregate excess-vocabulary rates | corpus year advancing | the extrapolation base needs rebuilding | `kobak-excess-vocabulary` |
| Vendor residue tokens | vendor markup changes | token stops appearing; new one appears | `wikipedia-signs-of-ai-writing` |

The last row behaves differently from the five above it and is the exception
this note exists to protect. A residue token such as a leftover citation marker
or a tracking parameter in a pasted URL is not a stylistic tendency measured
against a baseline. It is a literal artifact, present or absent, decidable by a
scanner. Its list of tokens goes out of date, but it does not degrade
gracefully into noise the way a vocabulary marker does: an obsolete token
simply stops matching, and a false positive on it is close to impossible. That
is why [[Vendor Residue Markers]] is the one class permitted to gate anything,
and why every stylistic class is capped at routing, per [[Evidence Tiers]].

## Why the rot runs one way

Rot is not symmetric, and the asymmetry matters for maintenance planning.

A marker weakens when the human baseline rises toward the model rate, when the
model rate falls toward the baseline, or both. `yakura-spoken-convergence`
documents the first. `freeburg-last-fingerprint` documents a case of the second.
Nothing in this ledger documents a marker strengthening over time without a new
model behaviour appearing to drive it.

There is a corollary for anyone tempted to publish a marker list as a product.
The publication itself accelerates the rot. Once a signal is named, it enters
prompts, style guides and post-processing filters, and the behaviour it measured
is trained or edited away. A marker's usefulness and its fame are inversely
related, which is the structural version of the argument in
[[Signs Are Not The Problem]].

## What refresh_due does about it

The ledger runs two cadences, and the split is itself the answer to this
objection. Fast-moving entries carry a 30-day `refresh_due`; stable
peer-reviewed entries carry roughly 90 days.

| Cadence | Which entries get it | Why |
| --- | --- | --- |
| about 30 days | living documents, vendor pages, per-model preprints, current-rate claims | the underlying thing changes without notice |
| about 90 days | peer-reviewed corpus studies with fixed corpora | the finding does not move, only its currency does |

The maintenance procedure keyed to those dates:

1. List every ledger entry whose `refresh_due` has passed. That set is the work
   queue, not a judgement about which findings feel stale.
2. For each, re-retrieve the source and compare the claim strings in the ledger
   against the current document. Living documents change silently.
3. For any per-model figure, check whether the named models still exist in the
   vendor's current lineup. A figure attached to a retired model is history,
   and is recorded as history rather than deleted.
4. For any vocabulary marker, look for a newer human-baseline measurement. If
   the gap has narrowed, demote the marker's tier and record the demotion.
5. Where a figure has been superseded, add the correction to
   [[Superseded Figures]] with the replacement and its ledger id. Never
   overwrite silently, because a quietly deleted number returns.
6. Update `refresh_due` and `last_verified` on the entry, then re-run
   `scripts/score_substance.py` before release.
7. If a source could not be retrieved, record the barrier rather than guessing,
   and leave the claim demoted for the current cycle.

Step 4 is the one that answers this objection directly. Demotion is a normal
operation here, not a failure. A brain that never demotes a marker is a brain
whose markers are all from the year it was written.

## What the objection does not reach

Two things survive a moving baseline intact.

Structural procedures do not compare against any baseline. Whether a paragraph
survives deletion with no named loss, whether a cited identifier resolves to the
paper it claims, whether a dependency exists in the registry: none of these
needs a reference distribution, so none of them rots. That is the deeper reason
this vault routes markers into procedures rather than scoring markers directly,
and it is argued in [[Why Structural Not Judgmental]].

Per-author calibration also survives, because both sides of the comparison drift
together. A writer whose vocabulary absorbs the same words everyone else is
absorbing moves with their own baseline and registers no change. The mechanics
are in [[The ESL Objection]].

## Related

- [[Marker Cohort Rot]]
- [[Excess Vocabulary]]
- [[The Em Dash]]
- [[Evidence Tiers]]
- [[Distributional Convergence]]
- [[Model Fingerprints]]
- [[Vendor Residue Markers]]
- [[Signs Are Not The Problem]]
- [[Why Structural Not Judgmental]]
- [[The ESL Objection]]
- [[Superseded Figures]]
