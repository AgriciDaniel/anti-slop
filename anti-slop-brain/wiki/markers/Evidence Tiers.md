---
type: "concept"
title: "Evidence Tiers"
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
  - "[[Note Conventions]]"
  - "[[The Firewall]]"
  - "[[Excess Vocabulary]]"
  - "[[The Em Dash]]"
  - "[[Vendor Residue Markers]]"
  - "[[Why Pangram Is Not Cited]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Firewall|Severity and Confidence]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[The Inversion Test|Inversion Test]]"
source_urls:
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2604.19768"
  - "https://arxiv.org/abs/2606.29540"
  - "https://arxiv.org/abs/2604.19139"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2509.19163"
---

# Evidence Tiers

A tier in this vault is a statement about the strength of the evidence behind a
marker, and nothing else. It is not a severity, not a confidence that a given
document is defective, and above all not a probability that a human wrote it.
Two markers can sit in the same tier and matter wildly differently to a reader.
Severity and certainty are tracked on separate axes, described in
[[The Firewall|Severity and Confidence]]; this note only answers the question "how well is
this pattern actually measured, and by whom".

## Why tiers exist at all

Without tiers, a marker list flattens. Every prior-art list this brain examined
has the same defect: a pattern backed by a peer-reviewed corpus study of
15 million abstracts sits in the same numbered sequence, with the same weight,
as a stylistic preference somebody added because they were tired of reading it.
The reader cannot tell which is which, so the whole list gets treated either as
gospel or as noise.

Tiering also creates somewhere to put claims the brain does not believe. A
marker that fails to earn a tier is not deleted. It is recorded at Tier 3 with
its defect attached, so the next person who encounters the claim in the wild
finds an argument here rather than a silence.

## The three tiers

### Tier 1, corpus-validated

A named study, a stated corpus, a stated sample size, and a stated method,
where the effect is measured against a human baseline drawn from the same
corpus. `kobak-excess-vocabulary` is the archetype: over 15 million PubMed
abstracts from 2010 to 2024, a detector-free method comparing observed word
frequencies against frequencies extrapolated from prior years, published in
Science Advances 11(27) on 2025-07-02. `bakhshi-saying-more` is weaker but
still qualifies on structure: 225 texts, roughly 600,000 tokens, with an expert
human comparison group.

### Tier 2, measured but high false-positive

The effect is real at population scale and the measurement is sound, but the
per-document error rate is unacceptable or unmeasured. `czuma-em-dash-prevalence`
is the case study: pre-registered on OSF as HFT8C, 69,632 medRxiv preprints,
and an author who states in the paper that the marker is a population-level
indicator rather than a per-paper detector. A Tier 2 marker is true about a
corpus and close to useless about a paragraph.

### Tier 3, folk wisdom

Widely repeated, plausible, and unmeasured. Individual vocabulary words seen in
isolation live here. So does burstiness, uniform sentence length, and every
pattern this brain inherited from prior art that carries no citation. Under the
confidence mapping in [[Note Conventions]], a claim with no ledger entry is
folklore by definition, and that is a mechanical outcome rather than a
judgement about whether the claim feels right.

## Tier assignment for every marker class in this folder

| Marker class | Tier | Primary ledger source | Note |
| --- | --- | --- | --- |
| Excess vocabulary density | 1 | `kobak-excess-vocabulary` | [[Excess Vocabulary]] |
| Puffery and undue emphasis | 1 | `wikipedia-signs-of-ai-writing` | [[Puffery and Undue Emphasis]] |
| Vague attribution and over-attribution | 1 | `wikipedia-signs-of-ai-writing` | [[Puffery and Undue Emphasis]] |
| Negative parallelism | 1 | `wikipedia-signs-of-ai-writing` | [[Negative Parallelism]] |
| Tricolon density | 1 | `bakhshi-saying-more` | [[Tricolon and Rule of Three]] |
| Hedging and hesitancy density | 1 | `bakhshi-saying-more` | [[Hedging and Hesitancy]] |
| Sycophantic verbal tics | 2 | `wu-verbal-tics` | [[Sycophancy]] |
| Em dash density | 2 | `czuma-em-dash-prevalence` | [[The Em Dash]] |
| Burstiness, uniform sentence length | 3 | none in ledger | [[Marker Cohort Rot]] |
| Single AI-vocabulary word in isolation | 3 | `wikipedia-signs-of-ai-writing` | [[Excess Vocabulary]] |
| Curly quotation marks alone | 3 | `wikipedia-signs-of-ai-writing` | [[Marker Cohort Rot]] |
| Boldface density | 3 | `wikipedia-signs-of-ai-writing` | [[Prose Surface]] |
| Vendor residue tokens | not a style tier | `wikipedia-signs-of-ai-writing` | [[Vendor Residue Markers]] |

The last row is the important one. Residue tokens are not weak or strong
evidence of a style; they are pipeline artifacts, and they are handled by a
deterministic scanner rather than by this tiering system at all.

## What each tier licenses

| Tier | May be reported to the user | May trigger a structural procedure | May be counted in a density threshold | May cause a hard failure |
| --- | --- | --- | --- | --- |
| 1 | yes, with the figure and the source id | yes | yes | no |
| 2 | yes, with the population-level caveat stated | yes | only alongside a Tier 1 signal | no |
| 3 | yes, labelled folklore | only in a cluster of three or more | no | no |
| Residue | yes | not applicable, the token is the finding | not applicable | yes, by scanner |

## The routing rule

No tier licenses a hard failure on its own. A marker is a routing decision, not
a conclusion. When a marker fires, the following happens and nothing else
happens:

1. Record the span, the marker class, and the tier.
2. Select the structural procedure the marker class routes to: usually
   [[The Deletion Test|Deletion Test]], [[The Inversion Test|Inversion Test]], [[The Stranger Test|Stranger Test]], or
   [[The Attribution Test|Attribution Test]].
3. Run that procedure and emit its artifact. The artifact is the evidence, not
   the marker. A deletion test emits the cut span and the named loss; an
   inversion test emits the written-out negation.
4. If the procedure produces a finding, report the finding. The marker
   disappears from the output at this point; it did its job by pointing.
5. If the procedure produces nothing, the span survives. A marker that routed
   to a passing test is a false positive for that document, and saying so
   costs nothing.

This is why `shaib-measuring-slop` matters to a note about tiers. It measured
LLM-as-judge agreement with human slop labels at kappa 0.01 for GPT-5, minus
0.01 for DeepSeek-V3, and 0.03 for o3-mini, with models flagging at 0.03 to
0.08 against a human rate of 0.34. A model asked to rate slop holistically is
close to worthless. A model asked to delete a clause and state what was lost is
doing something checkable. Tiers exist to move work from the first activity to
the second.

## Citing a source you are refusing to use

Some notes in this folder list a source in `source_urls` that they explicitly
decline to rely on. `pangram-supporting-evidence` appears that way in
[[Tricolon and Rule of Three]] and [[The Em Dash]]. The convention is:

- A source cited as an object of critique is named in the body with the reason
  it is not used, and its URL is listed so the reader can check the criticism.
- It does not drag the note's `confidence` value down, because the note is not
  resting any claim on it.
- The exception is [[Why Pangram Is Not Cited]], where the source is the
  subject and the note carries `contested` accordingly.

## Promotion and demotion

Tiers are not permanent. A Tier 3 claim is promoted when a ledger entry appears
with a corpus, a sample size, and a method. A Tier 1 claim is demoted when its
cohort ages out, which is the whole subject of [[Marker Cohort Rot]], or when
its figures turn out to come from a withdrawn version, which is what happened
to the widely quoted excess-vocabulary numbers.

Demotion is recorded rather than performed silently. The superseded figure and
its correction both stay visible, per [[Superseded Figures]].

## Related

- [[The Firewall]]
- [[Note Conventions]]
- [[Marker Cohort Rot]]
- [[Vendor Residue Markers]]
- [[Why Pangram Is Not Cited]]
- [[Distributional Convergence]]
- [[Why Detection Fails|Why Detectors Fail]]
- [[Detector Bias Against Language Learners]]
- [[The Stranger Test|Stranger Test]]
- [[The Attribution Test|Attribution Test]]
