---
type: "marker"
title: "Why Pangram Is Not Cited"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/marker"
  - "#confidence/contested"
confidence: "contested"
related:
  - "[[Evidence Tiers]]"
  - "[[The Em Dash]]"
  - "[[Tricolon and Rule of Three]]"
  - "[[Superseded Figures]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Corpus Study Method]]"
  - "[[Why Detection Fails]]"
  - "[[Note Conventions]]"
  - "[[Marker Cohort Rot]]"
  - "[[Humanizers]]"
source_urls:
  - "https://www.pangram.com/supporting-evidence"
  - "https://arxiv.org/abs/2606.29540"
  - "https://arxiv.org/abs/2603.27006"
  - "https://arxiv.org/abs/2605.19516"
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2604.19768"
---

# Why Pangram Is Not Cited

This is a case file rather than a marker description. The subject is one web
page, `pangram-supporting-evidence`, whose numbers circulate widely enough that
a reader arriving here will already have met them. The brain does not use them.
Recording the reasoning as a file, with the exhibits attached, is the only way
the decision stays checkable after everyone involved has forgotten it.

The file also serves a second purpose. The downgrade rules in the source ledger
were written in the abstract; this page is where they are applied to a real
artifact and shown to bite. If the rules are wrong, this is where the error
will be visible.

## Exhibit A: what the page asserts

Three claims, as captured at retrieval on 2026-07-27:

| Claim | As stated on the page |
| --- | --- |
| Human em-dash baseline, by-model section | 5 per 10,000 words |
| Model range, by-model section | 3 to 45 per 10,000 words |
| Human and AI baselines, summary table | 2 for humans against 17 for AI |
| Tricolon rate | AI uses tricolons about four times as often as humans |

What is absent is the whole of the apparatus. There is no sample size, no
corpus description, no method, no citation, and no date anywhere on the page.
It is a living marketing document, which means the figures above may not be the
figures a reader finds today, and there is no version history to check against.

## Exhibit B: the page contradicts itself

Rows one and three of the table above are on the same page. The human baseline
is 5 per 10,000 words in one place and 2 per 10,000 in another. Nothing on the
page reconciles them, distinguishes the corpora they were drawn from, or
indicates which supersedes which.

This is the exhibit that settles the file on its own. A disagreement between
two sources is an ordinary research problem, resolvable by reading both
methods. A disagreement between one source and itself, with no method attached
to either figure, is not resolvable at all. A reader cannot quote the page
correctly even in principle, because the page does not know what it claims.

Internal contradiction is also the cheapest defect in this entire brain to
check, and it is worth noticing that the check requires no expertise
whatsoever: read the whole page and compare the numbers to each other.

## Exhibit C: an independent measurement an order of magnitude away

`freeburg-last-fingerprint` measured a human em-dash baseline of 3.23 per 1,000
words, which is 32.3 per 10,000. Against the page's two baselines that is
roughly six times the higher figure and sixteen times the lower one.

Two sources cannot both be right about the same population by an order of
magnitude. One of them published a method: 12 models across 5 providers and
roughly 240,000 words. The other published none. That does not make the
preprint correct, and this file does not claim it is: `freeburg-last-fingerprint`
is a single-author, unaffiliated, non-peer-reviewed preprint, capped at
`CONTESTED` by the ledger's own rules, and it must carry that flag every time
it appears beside peer-reviewed work.

The contrast that matters is with `czuma-em-dash-prevalence`, which is what a
citable measurement of this marker looks like. It is pre-registered on OSF as
HFT8C, covers 69,632 medRxiv preprints, reports a rise in Discussion-section
prevalence from 4.23 percent before ChatGPT to 11.58 percent after, states a 95
percent confidence interval of 6.94 to 7.77 on the 7.35 point rise, gives an
odds ratio of 2.96, and runs a placebo split inside the pre-LLM era that moved
0.13 points. Every one of those is a commitment made in advance or a control
that could have failed. The vendor page makes no commitments and runs no
controls, so there is nothing in it that could have come out the other way.
See [[The Em Dash]] for what the marker itself is worth once measured properly,
and [[Corpus Study Method]] for the general shape.

## Exhibit D: the detector rated a base model as human

`xu-base-models-look-human` ran output from the Llama3-8B base model through
Pangram and recorded a rating of 98.8 percent human. The authors conclude that
detectors capture artifacts of instruction tuning rather than machine
generation. The same paper reports that iterative paraphrasing reaches 100
percent human probability by round 10, while semantic preservation collapses
from a 99 to 100 range down to a 33 to 99 range.

This exhibit is about the product rather than the marketing page, and it is
included because the page's authority rests on the product. If a detector rates
raw base-model output as almost certainly human, then what it has learned is
the fingerprint of a fine-tuning procedure, and a baseline it publishes for
human writing is a baseline for whatever its training data happened to contain.
That is a preprint verified at abstract level only, capped at `CONTESTED`, and
it is offered here as one exhibit rather than as a refutation.

## Applying the downgrade rules

The ledger's rules were not written for this page, and they decide it anyway.
That is the test of a rule set.

| Ledger downgrade rule | Triggered by | Outcome |
| --- | --- | --- |
| Marketing page with no date and no citation, tier FOLKLORE, never quoted as a measured figure | no date, no citation, no method anywhere on the page | tier FOLKLORE |
| Vendor study with no methodology or sample size, cap confidence at low | no sample size, no corpus description | confidence `low` |
| Vendor selling a product the finding would sell more of, record the conflict in limitations | a detector vendor publishing evidence that a detectable marker exists | conflict recorded |
| Preprint verified at abstract level only, cap tier at CONTESTED | applies to `xu-base-models-look-human`, an exhibit here | exhibit weighted accordingly |
| Single-author unaffiliated preprint, cap confidence at medium and tier at CONTESTED | applies to `freeburg-last-fingerprint` | exhibit weighted accordingly |

Under the confidence mapping in [[Note Conventions]], a ledger entry at `low`
maps to `contested` for any note that rests on it. This note carries
`contested` for that reason, as [[Evidence Tiers]] specifies for the one case
where the disputed source is the subject rather than a support.

## The ruling

The page is recorded in the ledger and never quoted as a measured figure. Its
claims may appear in this vault only as objects of description, always with the
absence of method attached, exactly as they appear above. Where an em-dash or
tricolon figure is needed, `czuma-em-dash-prevalence` and `bakhshi-saying-more`
are the citations, and their own stated limits travel with them.

The ruling is about this artifact, not about the vendor. `masrour-damage-humanizers`
is authored by Pangram employees, is published at GenAIDetect at COLING 2025,
states its method, and is cited throughout this brain, including its finding
that all humanizers tend to degrade the original text with fluency win rates of
26.0, 14.67 and 2.67 percent by tool tier. The ledger notes the sharper reason
to trust that particular result: the finding that humanizers evade detection
serves the authors' commercial interest and the finding that they degrade
quality does not. Same company, opposite treatment, because the artifacts are
different. See [[Humanizers]].

## What the ruling does not say: the false-positive class

Declining to cite is a statement about evidence, and it is routinely
over-read. Every item below is a conclusion this file does not support.

1. **It does not say the numbers are false.** They may be accurate summaries of
   real internal measurement. Unpublished is not the same as wrong, and if the
   method were published tomorrow the figures could survive intact.
2. **It does not say the detector is inaccurate.** Exhibit D is one contested
   preprint about one base model, not an evaluation of the product.
3. **It does not say vendor sources are inadmissible.** Both GitClear entries
   are vendor sources cited in this brain at `PRACTITIONER`, because they state
   a corpus and a method. Method, not affiliation, is the gate.
4. **It does not say the em dash is not a marker.** The marker is real at
   population scale on a pre-registered measurement. What the page cannot
   supply is a trustworthy human baseline to measure it against.
5. **It does not license an argument from the page's absence.** "Pangram says
   so" is not evidence here, and neither is "Pangram is not cited here".
6. **It carries no implication about anybody's writing.** Nothing in this file
   supports a judgment about who or what produced any document, which is rule 1
   of the firewall and the reason [[Why Detection Fails]] exists.

## Conditions for reopening

The file reopens, and the figures become citable, when any one of these appears:

1. A dated version of the page stating corpus, sample size, and method for each
   figure, with the two human baselines reconciled or one withdrawn.
2. A peer-reviewed or pre-registered publication reporting the same baselines
   with an independent corpus.
3. An independent replication of the human baseline that lands near 5 or 2 per
   10,000 words rather than near 32.3, which would shift the burden onto
   `freeburg-last-fingerprint` instead.

Until then the figures stay recorded and unused. Under [[Superseded Figures]]
the rejected numbers remain visible with the reason attached, so that the next
reader who meets them in the wild arrives at an argument rather than a gap.

## Related

- [[Evidence Tiers]]
- [[The Em Dash]]
- [[Tricolon and Rule of Three]]
- [[Superseded Figures]]
- [[Evidence Quality Ladder]]
- [[Corpus Study Method]]
- [[Why Detection Fails]]
- [[Detector Bias Against Language Learners]]
- [[Marker Cohort Rot]]
- [[overview|Overview]]
