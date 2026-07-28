---
type: "marker"
title: "The Em Dash"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/marker"
  - "#confidence/contested"
confidence: "contested"
related:
  - "[[Evidence Tiers]]"
  - "[[Why Pangram Is Not Cited]]"
  - "House Style Voice File"
  - "[[The Firewall]]"
  - "[[Marker Cohort Rot]]"
  - "[[Why Detection Fails|Why Detectors Fail]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Superseded Figures]]"
  - "[[Prose Surface]]"
  - "[[The Firewall|Layer 0 Scanners]]"
source_urls:
  - "https://arxiv.org/abs/2606.29540"
  - "https://arxiv.org/abs/2603.27006"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://www.pangram.com/supporting-evidence"
  - "https://github.com/blader/humanizer"
---

# The Em Dash

This note is about one punctuation mark, and it is the reason the tier system
in [[Evidence Tiers]] exists. The character is U+2014. It is the single most
confidently asserted AI tell in public discourse, the one people accuse
strangers over, and the evidence for it says something narrower and more
interesting than the accusation does. Working through the gap is the point of
this note; the marker itself is almost incidental.

This vault never prints U+2014 or U+2013. That is a house rule, explained near
the end, and it is a different kind of claim from anything in the evidence
sections.

## What was actually measured

`czuma-em-dash-prevalence` is the citation that replaced the vendor numbers
everyone was quoting. It is pre-registered on OSF as HFT8C, which matters more
than any single figure in it, and it covers 69,632 medRxiv preprints. The
measurement is the prevalence of the character in Discussion sections.

| Quantity | Value |
| --- | --- |
| Prevalence before ChatGPT | 4.23 percent |
| Prevalence after | 11.58 percent |
| Rise | 7.35 percentage points |
| 95 percent confidence interval on the rise | 6.94 to 7.77 |
| Odds ratio | 2.96 |
| Trajectory through 2023 | about 4 percent |
| 2024 | 8.0 percent |
| 2025 | 20.3 percent |
| Placebo split inside the pre-LLM era | plus 0.13 points, no change |

The placebo split is the part that earns the study its confidence rating. A
within-era split that shows no movement rules out the most obvious alternative
explanation, that the character was drifting upward anyway.

## What the author concluded

The paper's own conclusion is adopted here verbatim in substance: the em dash
is a population-level indicator, not a per-paper detector of LLM use.

Read that carefully, because it is the whole finding. Prevalence roughly
tripled across a corpus of 69,632 documents. At 20.3 percent in 2025, roughly
four in five documents in the post-period still do not contain the character at
all, and its presence in any one of them tells you close to nothing. A marker
can be strongly real in aggregate and useless in the specific case. That is not
a weakness of this particular study; it is the normal relationship between a
population statistic and an individual instance, and it is the reason Tier 2
exists as a category.

## The finding that cuts the other way

`freeburg-last-fingerprint` measured 12 models across 5 providers over roughly
240,000 words and argues that the rate is a signature of a specific
fine-tuning procedure rather than a universal property of machine text. Its
sharpest data point: base Llama 3.1 8B produced 0.49 per 1,000 words, while the
instruction-tuned version of the same model produced 0.00.

Reinforcement learning from human feedback can therefore **eliminate** the
marker as easily as amplify it. A marker that a training decision can zero out
is a marker with an expiry date attached, which is the subject of
[[Marker Cohort Rot]]. `wikipedia-signs-of-ai-writing` records the same
direction of travel from the field side, noting that GPT-5.1 already suppresses
the character, that the AI-characteristic form is usually surrounded by spaces
contrary to typographic convention, and that the sign is far more common on
discussion pages than in article prose.

That source is a single-author, unaffiliated, non-peer-reviewed preprint. The
ledger requires that flag every time it appears beside peer-reviewed work, and
it is why this note carries `contested` rather than a stronger confidence. It
also measured a human baseline of 3.23 per 1,000 words, equal to 32.3 per
10,000, which is between roughly six and sixteen times the human baseline
asserted by `pangram-supporting-evidence`. Two sources disagreeing by an order
of magnitude is itself information: at least one of them is wrong, and only one
of them published a method. See [[Why Pangram Is Not Cited]].

## Two claims that keep getting merged

This is the distinction the note exists to make.

| | House style claim | Slop verdict claim |
| --- | --- | --- |
| Statement | This document does not use U+2014 | The presence of U+2014 indicates AI authorship |
| Who can make it | the owner of the document | nobody, on this evidence |
| Basis | preference, consistency, a linter | a population statistic misapplied to one case |
| Falsifiable by | grepping the file | not falsifiable as stated |
| Enforcement | deterministic scanner, hard fail is fine | prohibited under [[The Firewall]] |
| Consequence of being wrong | a comma appears where a dash would have | a person is accused of something |

The owner of this vault bans the character as house style. That ban is a taste
decision, enforced by `lint_voice.py` in [[The Firewall|Layer 0 Scanners]], and it is
explicitly not a claim about anybody's authorship. Prior art blurs exactly this
line: `blader-humanizer` states the ban as a hard constraint on the grounds
that the character is one of the most reliable AI tells, while its own
false-positive section says the character is evidence only when paired with
other patterns. Those two statements cannot both be operative. It also bans
U+2013 outright, which breaks legitimate numeric and date ranges, page ranges,
and score lines, none of which any source anywhere proposes as a marker.

Keep the two claims apart and both become usable. Merge them and the house
style starts making accusations.

## False positive class: who gets wrongly flagged

1. **Professional editors and typographers.** The character is standard
   punctuation with entries in every major style manual.
2. **Fiction and essay writers.** Parenthetical asides are a stylistic staple,
   and heavy users are common.
3. **macOS and Microsoft Word users.** Substitution can be automatic, so the
   character can appear without ever being typed.
4. **Anyone writing after 2023 who reads current prose.** Human style
   converges toward what people read.
5. **Publications with a house style that mandates it.** Several do.
6. **Anyone pasting from a CMS or a word processor** that normalises double
   hyphens on save.

The converse false negative is just as important and gets no attention: a
document with none of the character is not thereby human, because as
`freeburg-last-fingerprint` shows, an instruction-tuned model may emit none at
all.

## How to handle any contested marker

This is the generalisable part, and it applies well beyond punctuation.

1. Find the strongest measurement and read its own stated limits before reading
   anyone's summary of it.
2. Separate the population claim from the instance claim. Write both out. Check
   which one you are about to act on.
3. Check whether a training change can remove the marker. If it can, date the
   marker and put it on the refresh schedule.
4. Separate the style preference from the evidential claim. Enforce the
   preference deterministically. Never let it borrow authority from the
   evidence.
5. Record the vendor claim you rejected, with the reason, so that the next
   reader arrives at an argument rather than a gap.
6. Route the marker to a structural procedure. Under [[Evidence Tiers]], a
   Tier 2 signal may be counted only alongside a Tier 1 signal and may never
   fail a document on its own.

## Related

- [[Evidence Tiers]]
- [[Why Pangram Is Not Cited]]
- [[Marker Cohort Rot]]
- [[The Firewall]]
- House Style Voice File
- [[The Firewall|Layer 0 Scanners]]
- [[Why Detection Fails|Why Detectors Fail]]
- [[Superseded Figures]]
- [[Hedging and Hesitancy]]
- [[Prose Surface]]
