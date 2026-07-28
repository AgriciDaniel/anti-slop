---
type: "question"
title: "Unledgered Code Review Agent Figures"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "evergreen"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/question"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Commit and Review Surface]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Superseded Figures]]"
  - "[[Note Conventions]]"
  - "[[The Attribution Test]]"
  - "[[What This Brain Does Not Claim]]"
  - "[[research-pack-2026-07-27|Research Pack 2026-07-27]]"
source_urls: []
---

# Unledgered Code Review Agent Figures

**RESOLVED 2026-07-28.** Kept as the worked record of how a blocked citation
gets unblocked, because the resolution took two lookups and the block had
stood for a full build cycle.

## Resolution

The paper is real and the framing was correct all along. The block was a wrong
identifier, not a missing study.

| Item | Value |
| --- | --- |
| Correct identifier | arXiv 2604.03196 |
| Title | From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests |
| Authors | Kowshik Chowdhury, Dipayan Banik, K M Ferdous, Shazibul Islam Shamim |
| Venue | Accepted at the 23rd International Conference on Mining Software Repositories, MSR 2026 |
| Ledger id | `chowdhury-code-review-agents`, added 2026-07-28 |

All three figures appear verbatim in the abstract: a 45.20 percent merge rate
for agent-only pull requests, 23.17 percentage points below human-only at 68.37
percent, and 60.2 percent of closed agent-only pull requests in the 0 to 30
percent signal range.

The identifier that caused the block, arXiv 2603.28592, is Liu et al. on
technical debt. That attribution in the ledger was always correct. The error
was assigning the same identifier to this paper as well.

The figures are now quotable in deliverables.

## The original question, kept for the record

## What happened

During the build, writer agents were briefed to cite a source id
`chowdhury-code-review-agents` for two numbers: that pull requests handled only
by code review agents merge at 45.20 percent against 68.37 percent for human
only review, and that 60.2 percent of closed agent only pull requests fall in
the 0 to 30 percent signal range, attributed to MSR 2026.

That ledger id does not exist. It was named in the briefing by mistake and
never added to `references/source-ledger.json`.

Two independent writer agents hit the same missing id and both refused to
invent an entry for it. That refusal is the correct outcome and is worth
recording as evidence that the citation discipline in [[Note Conventions]]
holds under pressure rather than only on paper.

## Why it was not simply added

The underlying verification pass recorded the finding but flagged a problem:
the arXiv identifier associated with it, 2603.28592, is the same identifier
recorded for a different study, the Liu et al. work on technical debt in
AI authored commits. One of those two attributions is wrong and the pass could
not determine which before its search budget was exhausted.

Adding a ledger entry with an identifier known to be contested would fail this
brain's own [[The Attribution Test]] at rung two: a named, real looking source
that may not support the claim attached to it. That is the harder failure to
catch and the one the test exists for.

## Current handling

| Location | Treatment |
| --- | --- |
| `references/source-ledger.json` | No entry. The id does not exist. |
| [[The Code Slop Disagreement]] | Figures stated in prose, explicitly marked as not quotable in a deliverable until a ledger entry exists |
| [[Commit and Review Surface]] | Same treatment, set as precedent |
| Deliverables | Blocked. No adapter output may carry these numbers |

## Resolution procedure

1. Search for the MSR 2026 proceedings entry by title, "From Industry Claims to
   Empirical Reality", and by author surname Chowdhury.
2. Independently resolve arXiv 2603.28592 and record which study it actually
   is. Correct whichever of the two attributions is wrong.
3. If a stable primary URL is found, add a ledger entry at
   `evidence_tier: CONTESTED` and `confidence: medium` until the identifier
   conflict is fully resolved, then promote.
4. If no primary source is found, delete the figures from both notes rather
   than leaving them in prose. An unciteable number that survives two review
   passes becomes folklore by attrition.
5. Record the outcome in [[Superseded Figures]] either way.

## Why this note exists rather than a silent fix

A missing citation that is quietly dropped leaves no trace, and the next person
to want that figure will reintroduce it from memory. A missing citation that is
written down as an open question stays visible until somebody resolves it. The
same reasoning drives the unread sources list in
[[research-pack-2026-07-27|Research Pack 2026-07-27]] and the refusal register in
[[What This Brain Does Not Claim]].
