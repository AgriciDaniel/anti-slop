---
type: "meta"
title: "Answer Engine Citability Policy"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "seed"
created: "{{date}}"
updated: "{{date}}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/meta"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[CONVENTIONS]]"
  - "[[Index]]"
  - "[[Dashboard]]"
  - "[[Tag Taxonomy]]"
  - "[[Source Manifest Guide]]"
  - "[[Claim Verification Flow]]"
  - "[[Research Refresh Workflow]]"
  - "[[Source Intake Workflow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
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
  - "[[wiki/questions/_index|Questions Hub]]"
  - "[[wiki/gaps/_index|Gaps Hub]]"
  - "[[wiki/experiments/_index|Experiments Hub]]"
source_urls: []
---

# Answer Engine Citability Policy

Confidence tag: practitioner.

Answer-engine policy: useful crawlable primary-source passages, no GEO hacks. Public passages should be useful, crawlable, source-clear, and free of tricks.

## Operating Contract

- Operator: fill domain-specific examples only after source intake.
- Keep claims advisory until the claim ledger and source ledger support them.
- Cite source notes, raw hashes, or official URLs for domain claims.

## Review Loop

1. Check [[Dashboard]] for notes whose status, confidence, or freshness conflicts with this policy.
2. Check [[Tag Taxonomy]] when a note needs a new domain, type, or confidence tag.
3. Check [[Source Intake Workflow]] before turning raw material into a wiki claim.
4. Check [[Claim Verification Flow]] before moving a claim into a deliverable.
5. Check [[Research Refresh Workflow]] before relying on time-sensitive evidence.
6. Update [[Log]] when this policy changes a release gate or operator workflow.

## Failure Signals

- A deliverable cites no source note, raw hash, or official URL.
- A confidence value in body text disagrees with frontmatter.
- A note says evidence-based while the source ledger is empty.
- A public-facing page contains copied source text without attribution.
- A workflow asks an agent to mutate an external system in V1.
- A source is old enough to require refresh but no stale callout exists.

## See Also

- [[CONVENTIONS]] for the full vault contract.
- [[Tag Taxonomy]] for graph and Dataview tag rules.
- [[Dashboard]] for status and confidence queries.
- [[Source Manifest Guide]] for source note requirements.
- [[Claim Verification Flow]] for evidence promotion.

## Related

- [[CONVENTIONS]]
- [[Index]]
- [[Dashboard]]
- [[Source Manifest Guide]]
- [[Claim Verification Flow]]
- [[Research Refresh Workflow]]
