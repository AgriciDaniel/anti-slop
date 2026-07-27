---
type: "entity"
title: "Synthesis Module synthesize findings"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/entity"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[wiki/entities/_index|Entities Hub]]"
  - "[[Index]]"
  - "[[Dashboard]]"
  - "[[CONVENTIONS]]"
  - "[[Tag Taxonomy]]"
  - "[[Source Intake Workflow]]"
  - "[[Research Refresh Workflow]]"
  - "[[Claim Verification Flow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
  - "[[Source Manifest Guide]]"
  - "[[Best Practices Kernel]]"
  - "[[Health Scorecard]]"
  - "[[Action Roadmap]]"
  - "[[Weekly Report]]"
  - "[[Approval Queue]]"
source_urls: []
---

# Synthesis Module synthesize findings

## Adapter Evidence

This synthesis module note was folded from `references/adapter-manifest.json`, section `synthesis_modules`.

- id: `synthesize-findings`
- path: `scripts/synthesize_findings.py`
- lane: `review-run`
- emits: `schemas/findings.schema.json`
- description: `The firewall enforcement point. Emits separate severity and confidence, attaches the structural procedure that convicted each finding, orders by severity then confidence, refuses any finding with no evidence span, never lets a Tier 2 or Tier 3 marker convict on its own, and emits no authorship field of any kind.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
