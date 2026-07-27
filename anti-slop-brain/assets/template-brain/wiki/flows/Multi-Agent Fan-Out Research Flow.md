---
type: "flow"
title: "Multi-Agent Fan-Out Research Flow"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "seed"
created: "{{date}}"
updated: "{{date}}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/flow"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Index]]"
  - "[[Dashboard]]"
  - "[[Tag Taxonomy]]"
  - "[[Source Intake Workflow]]"
  - "[[Research Refresh Workflow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
  - "[[Best Practices Kernel]]"
  - "[[CONVENTIONS]]"
  - "[[Claim Verification Flow]]"
  - "[[Source Manifest Guide]]"
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
  - "[[wiki/questions/_index|Questions Hub]]"
  - "[[wiki/gaps/_index|Gaps Hub]]"
  - "[[wiki/experiments/_index|Experiments Hub]]"
source_urls: []
---

# Multi-Agent Fan-Out Research Flow

Confidence tag: practitioner.

## Trigger

A research task is broad, parallelizable, and worth isolated worker contexts.

## Prerequisites

- Read [[CONVENTIONS]].
- Read [[Hot]], [[Index]], and the relevant folder hub.
- Confirm `.raw/` remains immutable.
- Confirm the task is advisory and read-only under advisory-read-only-v1.

## Steps

1. Gather context from wiki notes and source ledgers.
2. Name the claim, change, or decision being handled.
3. Check source coverage and confidence tags.
4. Record gaps in [[wiki/gaps/_index|Gaps Hub]] or questions in [[wiki/questions/_index|Questions Hub]].
5. Produce the smallest useful output.
6. Verify the output against source notes, raw hashes, or official URLs.
7. Update [[Log]] and [[Hot]] when the run changes vault state.

## Outputs

- A sourced note, claim-ledger row, deliverable update, or next-action record.
- Confidence tags attached to every claim.
- Clear no data wording when evidence is missing.

## Gates

- No unsupported domain claim.
- No public release without `PUBLISHING_NOTICE.md` review.
- No external mutation without explicit approval and rollback.
- No deliverable or report without a source citation.

## Failure Modes

- Source is stale or absent: say no data and open a question note.
- Claim has only one source: keep SINGLE-SOURCE visible.
- Evidence conflicts: tag contested and keep both sides visible.
- Context is polluted: run the [[Context Compaction Routine]] or restart.

## Sources

- [[CONVENTIONS]]
- [[Source Intake Workflow]]
- [[Research Refresh Workflow]]
- [[Best Practices Kernel]]

## Rollback

Discard worker summaries and keep the source ledger unchanged.

## Related

- [[Index]]
- [[Dashboard]]
- [[Source Intake Workflow]]
- [[Research Refresh Workflow]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
- [[Best Practices Kernel]]
