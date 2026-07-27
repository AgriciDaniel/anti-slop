---
type: "entity"
title: "Synthesis Module synthesize cohort diff"
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

# Synthesis Module synthesize cohort diff

## Adapter Evidence

This synthesis module note was folded from `references/adapter-manifest.json`, section `synthesis_modules`.

- id: `synthesize-cohort-diff`
- path: `scripts/synthesize_cohort_diff.py`
- lane: `marker-cohort-refresh`
- emits: `schemas/cohort-diff.schema.json`
- description: `Computes added, removed, tier changed and routing changed markers between two snapshots, and flags every marker whose source refresh_due has passed relative to --reference-date.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
