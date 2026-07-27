---
type: "entity"
title: "Report Renderer render findings report"
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

# Report Renderer render findings report

## Adapter Evidence

This report renderer note was folded from `references/adapter-manifest.json`, section `report_renderers`.

- id: `render-findings-report`
- path: `scripts/render_findings_report.py`
- lane: `review-run`
- consumes: `schemas/findings.schema.json`
- description: `Renders the findings envelope as markdown, including the severity by confidence matrix, each finding's evidence span and procedure artifact, the routed procedures, the procedures that passed, and every refusal. Adds no judgement of its own.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
