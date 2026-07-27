---
type: "platform"
title: "Input Schema review input.schema"
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

# Input Schema review input.schema

## Adapter Evidence

This input schema note was folded from `references/adapter-manifest.json`, section `input_schemas`.

- id: `review-input`
- path: `schemas/review-input.schema.json`
- raw_input_type: `Drafts, diffs, commit messages, pull request descriptions, agent transcripts, and documents supplied by the operator`
- lane: `review-run`
- description: `One artifact under review with its scanner findings, marker hits and structural procedure artifacts. Draft 2020-12, with enums for severity, confidence, procedure, tier and surface.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
