---
type: "entity"
title: "Report Renderer render cohort report"
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

# Report Renderer render cohort report

## Adapter Evidence

This report renderer note was folded from `references/adapter-manifest.json`, section `report_renderers`.

- id: `render-cohort-report`
- path: `scripts/render_cohort_report.py`
- lane: `marker-cohort-refresh`
- consumes: `schemas/cohort-diff.schema.json`
- description: `Renders the cohort diff as markdown, stale evidence first, then tier changes with their stated consequences, then routing changes, additions and removals.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
