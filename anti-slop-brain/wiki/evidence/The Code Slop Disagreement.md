---
type: "concept"
title: "The Code Slop Disagreement"
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
  - "[[Evidence Quality Ladder]]"
  - "[[Code Surface]]"
  - "[[Commit and Review Surface]]"
  - "[[Superseded Figures]]"
  - "[[Corpus Study Method]]"
  - "[[The Generation Verification Asymmetry]]"
  - "[[What This Brain Does Not Claim]]"
  - "[[The Moving Baseline Objection]]"
  - "[[Dependency Surface]]"
  - "[[Evidence Tiers]]"
source_urls:
  - "https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://arxiv.org/abs/2507.09089"
  - "https://arxiv.org/abs/2507.00788"
  - "https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/"
  - "https://arxiv.org/abs/2606.28438"
---

# The Code Slop Disagreement

Nobody reading this vault should come away believing the question of whether AI
assistance degrades code has been answered. It has not. This note lays the two
sides out at full strength, side by side, and deliberately stops short of
picking one. A brain that resolved this disagreement in 2026 would be asserting
more than its sources support.

## The two columns

| Question | Evidence that AI-assisted code is worse | Evidence that it is not |
| --- | --- | --- |
| Duplication | moved code 24.8 to 9.5 percent, copy-paste 8.3 to 12.3 percent (`gitclear-copilot-quality-2025`) | no duplication difference measured in a controlled setting (`borg-null-result`) |
| Duplicated blocks | eight-fold rise in blocks of five or more duplicated lines during 2024 (`gitclear-copilot-quality-2025`) | not replicated outside vendor telemetry |
| Maintainability trend | block duplication 40.3 to 73.0 per million changed lines, plus 81 percent (`gitclear-maintainability-gap`) | correlational, no control group, vendor sells the remedy |
| Developer speed | 19 percent slower against a forecast of 24 percent faster (`metr-developer-slowdown`) | 16 developers only; follow-up could not obtain a clean signal |
| Code quality and evolution | agent-only review shows a lower merge rate, figure not yet in this ledger | no significant differences across 151 participants (`borg-null-result`) |
| Maintainer burden | the 2025 open-source triage overload | "the slop situation is not a problem anymore" (`stenberg-high-quality-chaos`) |
| Self-review as a control | acceptance scores rise while correctness falls (`song-rubber-stamp-regime`) | preprint, abstract-level verification only |

## The column that says it is worse

**Telemetry at scale.** `gitclear-copilot-quality-2025` analysed **211 million
changed lines** from 2020 to 2024. Moved or refactored code, which is the
signature of a developer consolidating rather than accumulating, fell from
**24.8 percent in 2021 to 9.5 percent in 2024**. Copy-pasted code rose from
**8.3 percent to 12.3 percent** across the same window. Blocks containing five
or more duplicated lines rose **eight-fold** during 2024.

`gitclear-maintainability-gap` continues the series across **623 million
changes**, reporting block duplication rising from **40.3 per million changed
lines in 2023 to 73.0 in 2026 year to date, a rise of 81 percent**. Do not
attach the frequently quoted 7.1 percent churn figure to either report; it was a
discarded 2024 projection against an actual of 5.7 percent, and the correction
is logged in [[Superseded Figures]].

**A randomised trial.** `metr-developer-slowdown` gave 16 experienced developers
246 real tasks on repositories they already maintained and found that allowing
AI **increased completion time by 19 percent**. The perception result is the
part worth carrying forward: those same developers **forecast a 24 percent
speedup** and still estimated a 20 percent speedup after the fact, while
economists forecast 39 percent and machine learning experts 38 percent. Whatever
the sign of the productivity effect, self-report about it is measurably
unreliable.

**Agent-only review.** A peer-reviewed MSR 2026 study by Chowdhury and
colleagues reports pull requests handled only by code-review agents merging at
**45.20 percent against 68.37 percent** for human-only review. This vault holds
that finding at arm's length for a procedural reason rather than a substantive
one: it is recorded in `.research/verification-ledger.md` and has no entry in
`references/source-ledger.json`, so under the citation rules in
[[Note Conventions]] the number may not be repeated in a deliverable until the
entry exists. It is stated here rather than omitted, because a disagreement note
that hides one side's strongest recent result is not documenting a disagreement.

**Self-review does not fill the gap.** `song-rubber-stamp-regime` reports that
AI self-review gates enter a regime in which acceptance scores rise while
benchmark correctness falls. Preprint, abstract-level verification, tier
CONTESTED. It bears on the whole column because the usual response to a quality
worry is to add a model-based check, and that response has evidence against it.

## The column that says it is not

**The strongest single study is a null result, in one of its two phases.**
`borg-null-result` had **151 participants** and was **pre-registered with
In-Principle Acceptance before data collection**. It is a **preprint**, arXiv
2507.00788, not a published paper: the In-Principle Acceptance was granted at
ICSME and it carries no journal reference. Its pre-registered Phase 2 found **no
significant differences in subsequent code evolution, completion time, or
quality** between AI-assisted and unassisted development. Phase 1, observational,
found the opposite direction: a **30.7 percent median reduction in completion
time** with an AI assistant, and an estimated **55.9 percent speedup** for
habitual AI users. A citation of this source that reports only the null is
incomplete, including on this page.

In-Principle Acceptance is the detail that makes this hard to dismiss. The venue
committed to publishing whatever the data showed, before the data existed. The
null result could not have been buried, the analysis plan could not have been
adjusted to chase an effect, and the authors had no publication incentive
pushing in either direction. On the rungs in [[Evidence Quality Ladder]] it sits
above every other item on this page.

**The maintainer narrative reversed.** The most cited real-world example of AI
slop was the collapse of open-source security triage under unverified reports.
`stenberg-high-quality-chaos`, written by the curl maintainer on 2026-04-22,
states that **the slop situation is not a problem anymore**. Report frequency
runs at about **double the rate seen through 2025**, the **confirmed-vulnerability
rate returned to 15 to 16 percent**, and **curl returned to HackerOne on
2026-03-01**, bounty-free.

That is a first-hand account rather than a controlled study, and it should be
weighted as one. It is nonetheless decisive against a specific widely repeated
claim, which is that curl abandoned bug bounties permanently because of AI. The
lesson it supports is procedural: raising the cost of submitting an unverified
artifact worked, and banning a tool was never what happened.

## The pattern in who publishes what

State it plainly, because it explains the shape of the disagreement better than
any individual result does.

**The strongest slop numbers come from vendors selling engineering-intelligence
products. The strongest null results come from academia.**

| Item | Source type | Sells a remedy | Pre-registered | Controlled |
| --- | --- | --- | --- | --- |
| `gitclear-copilot-quality-2025` | vendor | yes | no | no |
| `gitclear-maintainability-gap` | vendor | yes | no | no |
| `metr-developer-slowdown` | research organisation | no | not stated | yes, randomised |
| `borg-null-result` | academic | no | yes, with IPA | yes |
| `stenberg-high-quality-chaos` | practitioner account | no | no | no |

This is not an accusation. GitClear's telemetry is real, its sample is enormous,
and its method is published, which is why it earns rung 4 rather than rung 5.
But a correlational time series from a company whose product addresses the trend
it measures is a different kind of evidence from a pre-registered controlled
comparison, and the two should never be quoted as though they were the same
kind. The standing rule in this vault is that they are quoted **together or not
at all**.

## What would settle it

1. A **pre-registered controlled study powered for maintenance outcomes**, not
   completion time, following the same codebase for at least a year after the
   assisted changes land.
2. **Defect and revert rates as the outcome**, with the analysis plan fixed
   before the data is collected, so that duplication is a covariate rather than
   a proxy for quality.
3. **Independent replication of the vendor telemetry** by a party that sells
   nothing, using the same repository corpus and a published extraction method.
   [[Corpus Study Method]] describes what that write-up would have to contain.
4. **A cohort control.** Every figure above compares periods, not matched teams.
   Model capability, tooling, and hiring all changed across the same window, a
   confound the [[The Moving Baseline Objection]] treats in general.
5. **Separation of the agent-review question from the assistance question.**
   Whether an agent should review code and whether a person should use one to
   write it are different questions currently answered with the same numbers.
6. **A published human-rated quality comparison.** Every quality claim on this
   page is either mechanical, such as duplication counts, or self-reported.

Until several of those exist, this note holds. What survives the disagreement is
narrow and still actionable: duplication is measurably rising in at least one
large telemetry corpus, self-assessment of assisted speed is unreliable, and no
controlled evidence of a quality difference exists. That justifies mechanical
review of the kind [[Code Surface]] and [[Dependency Surface]] specify, and it
justifies nothing stronger.

## Related

- [[Evidence Quality Ladder]]
- [[Code Surface]]
- [[Commit and Review Surface]]
- [[Dependency Surface]]
- [[Superseded Figures]]
- [[Corpus Study Method]]
- [[The Generation Verification Asymmetry]]
- [[The Moving Baseline Objection]]
- [[What This Brain Does Not Claim]]
- [[Note Conventions]]
