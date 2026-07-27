---
type: "question"
title: "What Current Official Source Resolves The Highest Risk Claim"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "seed"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/question"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Index]]"
  - "[[CONVENTIONS]]"
  - "[[Dashboard]]"
  - "[[Tag Taxonomy]]"
  - "[[Claim Verification Flow]]"
  - "[[wiki/questions/_index|Questions Hub]]"
  - "[[Source Intake Workflow]]"
  - "[[Research Refresh Workflow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
  - "[[Source Manifest Guide]]"
  - "[[Best Practices Kernel]]"
  - "[[Health Scorecard]]"
  - "[[Action Roadmap]]"
  - "[[Weekly Report]]"
  - "[[Approval Queue]]"
  - "[[wiki/flows/_index|Flows Hub]]"
  - "[[wiki/sources/_index|Sources Hub]]"
  - "[[wiki/concepts/_index|Concepts Hub]]"
  - "[[wiki/decisions/_index|Decisions Hub]]"
  - "[[wiki/deliverables/_index|Deliverables Hub]]"
  - "[[wiki/reports/_index|Reports Hub]]"
  - "[[wiki/gaps/_index|Gaps Hub]]"
  - "[[wiki/experiments/_index|Experiments Hub]]"
source_urls: []
---

# What Current Official Source Resolves The Highest Risk Claim

Confidence tag: practitioner.

This question records a research decision that needs a dated source.

## Evidence Callouts

> [!gap]
> This seed marks an evidence gap until source intake records dated official, primary, vendor, regulator, standards-body, or API evidence.

> [!question]
> Which current source resolves this seed, and what claim-ledger row will it support or challenge?

> [!contradiction]
> If two trustworthy sources disagree, keep both sides visible here and leave confidence as contested until the operator resolves it.

> [!stale]
> Re-check this seed on the research refresh cadence before using it in a deliverable or report.

> [!done]
> Close this seed only after `references/source-ledger.json` and `references/claim-ledger.md` both carry the supporting evidence.

## Source Need

Operator: add dated official, primary, vendor, regulator, standards-body, or API evidence before turning this seed into a domain claim.

## Claim Ledger Link

Record any supported or challenged claim in `references/claim-ledger.md` and keep SINGLE-SOURCE status visible until a second source is recorded.

## Resolution Path

1. Start at [[Source Intake Workflow]] and capture the raw source or official URL.
2. Summarize what the source proves in [[Source Manifest Guide]] or a dedicated source note.
3. Use [[Claim Verification Flow]] to decide whether the claim remains practitioner, moves to evidence-based, or becomes contested.
4. Update `references/source-ledger.json` with retrieved date, source type, confidence, and refresh_due.
5. Update `references/claim-ledger.md` with the claim, verdict, and second-source status.
6. Link the supported result to [[Health Scorecard]], [[Action Roadmap]], or [[Weekly Report]] only after the evidence path is visible.
7. Leave this note as seed until the source and claim ledgers both support the closure.

## Decision Rules

- No source: keep the note open and say no data.
- One trustworthy source: keep SINGLE-SOURCE visible.
- Two independent trustworthy sources: consider evidence-based if the claim is narrow.
- Conflicting trustworthy sources: use contested and keep the contradiction callout.
- Old source in a fast-moving domain: use stale and run [[Research Refresh Workflow]].
- Popular but unsourced advice: use folklore and do not promote it into a deliverable.

## See Also

- [[Dashboard]] lists all seed notes that still need substance.
- [[Tag Taxonomy]] defines the confidence values and tags used here.
- [[Research Refresh Workflow]] governs stale evidence review.
- [[Synthesis Workflow]] turns sourced notes into useful outputs.

## Related

- [[Index]]
- [[CONVENTIONS]]
- [[Claim Verification Flow]]
- [[wiki/questions/_index|Questions Hub]]
