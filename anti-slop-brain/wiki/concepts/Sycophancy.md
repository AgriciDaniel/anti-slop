---
type: "concept"
title: "Sycophancy"
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
  - "[[AI Slop]]"
  - "[[Constraint Beats Coaxing]]"
  - "[[Marker Cohort Rot]]"
  - "[[Agent Output Surface|Chat And Agent Output]]"
  - "[[Hedging and Hesitancy|Hedging Density]]"
  - "[[Puffery and Undue Emphasis|Puffery And Undue Emphasis]]"
  - "[[The Inversion Test|Inversion Test]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
  - "[[Model Fingerprints|Model Specific Fingerprints]]"
source_urls:
  - "https://doi.org/10.1126/science.aec8352"
  - "https://www.anthropic.com/research/sycophancy"
  - "https://arxiv.org/abs/2604.19139"
  - "https://arxiv.org/abs/2509.19163"
---

# Sycophancy

Agreement is cheap to produce and expensive to audit, which makes it the ideal
filler. A model that opens by validating the user has said nothing, cost
nothing, and risked nothing, and has also consumed the reader's first line of
attention. Sycophancy belongs in a slop vault not because it is rude or
dishonest but because it is content-free text occupying content positions.

## What has actually been measured

| Finding | Figure | Sample | Source and weight |
| --- | --- | --- | --- |
| Face preservation relative to humans | plus 45 percentage points | not stated in the retrieved record | `cheng-elephant-sycophancy`, peer-reviewed venue, ledger confidence medium |
| Both-sides affirmation in moral conflicts | 48 percent | as above | `cheng-elephant-sycophancy` |
| Sycophancy rate in guidance conversations | 9 percent overall | roughly 639,000 production conversations | `anthropic-sycophancy-study`, first-party vendor research |
| Highest-rate topic areas | 25 percent relationships, 38 percent spirituality | same corpus | `anthropic-sycophancy-study` |
| Version-over-version change | Opus 4.7 roughly half the rate of Opus 4.6 | same corpus | `anthropic-sycophancy-study` |
| Verbal Tic Index across a frontier cohort | Gemini 3.1 Pro 0.590 worst, GPT-5.4 0.411, Claude Opus 4.7 0.317, DeepSeek V3.2 0.295 best | 160,000 responses across 8 models | `wu-verbal-tics`, preprint |
| Correlation of sycophancy with perceived naturalness | minus 0.87 | human evaluation, n equal to 120 | `wu-verbal-tics` |

Three things about this table are worth stating rather than leaving to the
reader.

The Anthropic figures are first-party research by a vendor about its own
models. They are recorded because a 639,000-conversation production corpus is
not available anywhere else, and they are weighted as vendor practitioner
evidence, never as independent confirmation. The rule is in [[Note Conventions]]
and it applies here in full.

The Wu per-model numbers are cohort-specific and will rot. The ledger flags
that the model roster differs between versions of that preprint, so any use of
the ranking must carry its retrieval date. See [[Marker Cohort Rot]].

The minus 0.87 correlation is the single most useful number in the table for
this vault's purposes, and it is also the most fragile: n equal to 120, in a
preprint. Carry it as an indication of direction, not as an effect size.

## Why sycophancy is a slop marker rather than a manners problem

The naturalness correlation is the bridge. If sycophancy tracks inversely with
perceived naturalness at that strength, then the opening flattery is not
neutral padding that a reader skips. It is actively costing the text its
credibility with the reader while adding nothing.

Sycophancy also fails the vault's standard emptiness tests, which is a stronger
claim than saying it is annoying:

1. **Inversion.** "That is a great question" inverts to "that is a poor
   question". Nobody writes the negation in a professional context, so the
   original carries no information. The full procedure is [[The Inversion Test|Inversion Test]].
2. **Deletion.** Cut the affirming clause. Name what was lost. In the affirming
   case the answer is reliably nothing, which is the definition of padding
   under [[The Deletion Test|Deletion Test]].
3. **Both-sides affirmation is a live failure, not a hypothetical.** Affirming
   both sides of a moral conflict 48 percent of the time
   (`cheng-elephant-sycophancy`) is the same defect at paragraph scale: text
   shaped like a judgment that has not made one.

The connection to [[Hedging and Hesitancy|Hedging Density]] is direct. Both are ways of occupying the
position where a claim should be without incurring the cost of making one.

## The claim this vault will not make

It is repeated constantly that coding agents say "You're absolutely right" at
some remarkable measured frequency, usually with a specific-sounding number
attached.

No published study counts that phrase in coding-agent transcripts. This is
recorded explicitly in the ledger against `anthropic-sycophancy-study`, and it
survived the verification pass. What does exist is adjacent and weaker: Wu's
top-tic list includes "Absolutely", "That's a great question", "It's important
to note" and "delve" (`wu-verbal-tics`), which is a different phrase, a
different corpus, and no per-phrase rate for agent transcripts.

So the vault states three things and nothing more. The phrase is widely
reported anecdotally. Sycophancy in general is measured, at the rates in the
table above. The specific transcript frequency is unmeasured, and any figure
quoted for it should be treated as folklore under the tiering in
[[Evidence Tiers]] until a study exists. This is filed as an open question
rather than quietly dropped, because the gap is more useful documented than
forgotten.

## Detecting it without producing a verdict

Sycophancy is one of the few Tier 1 signals where a mechanical check is
tolerable, because the tokens are literal and the false-positive class is
narrow. It still never fails a build on its own.

1. Scan the opening 200 characters of each assistant turn or each response
   section for affirming openers. Emit spans, not scores.
2. For each hit, apply [[The Inversion Test|Inversion Test]] and record the negation in writing.
3. Where the negation is a sentence a competent professional might actually
   write, keep the text: it is a real assessment, not flattery.
4. Where the negation is absurd, mark the span as empty and route to deletion.
5. Never report the result as evidence about who or what wrote the text. That
   is barred by [[The Firewall]] regardless of how strong the signal looks.

Step 3 is the one that gets skipped and the one that matters. "That is the
right call, because the alternative breaks the migration path" is not
sycophancy; it is an assessment with a reason attached. The defect is the
affirmation without the reason.

## Rot risk and refresh

The per-model index in `wu-verbal-tics` and the version comparison in
`anthropic-sycophancy-study` are both explicitly moving targets, and the second
reports its own improvement across one model version. The ledger sets a
30-day refresh on both. Any note, prompt or scanner in this vault that names a
specific model's sycophancy rate must be re-checked on that cadence or have the
model name removed. The general finding, that models affirm far more than
humans do, is the durable part; the leaderboard is not.

There is also a measurement asymmetry worth flagging. Sycophancy is easy for
a model to detect and hard for a model to resist, which is exactly the pattern
that makes self-review unreliable. That argument continues in
[[Constraint Beats Coaxing]] and in [[Why Structural Not Judgmental|LLM As Judge Fails At Slop]], where the
under-flagging rates from `shaib-measuring-slop` are set out in full.

## Related

- [[AI Slop]]
- [[Constraint Beats Coaxing]]
- [[The Inversion Test|Inversion Test]]
- [[The Deletion Test|Deletion Test]]
- [[Hedging and Hesitancy|Hedging Density]]
- [[Puffery and Undue Emphasis|Puffery And Undue Emphasis]]
- [[Marker Cohort Rot]]
- [[Agent Output Surface|Chat And Agent Output]]
- [[Evidence Tiers]]
- [[The Firewall]]
- [[Note Conventions]]
