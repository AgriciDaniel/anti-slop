---
type: "platform"
title: "Input Schema findings.schema"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/platform"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[wiki/platforms/_index|Platforms Hub]]"
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

# Input Schema findings.schema

## Adapter Evidence

This input schema note was folded from `references/adapter-manifest.json`, section `input_schemas`.

- id: `findings`
- path: `schemas/findings.schema.json`
- lane: `review-run`
- description: `Output contract for the findings report. Severity and confidence are separate required fields, additionalProperties is false at every level, and no authorship property exists anywhere in the schema.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
