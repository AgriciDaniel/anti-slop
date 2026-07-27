---
type: "platform"
title: "Importer ingest marker cohort"
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

# Importer ingest marker cohort

## Adapter Evidence

This importer note was folded from `references/adapter-manifest.json`, section `importers`.

- id: `ingest-marker-cohort`
- path: `scripts/ingest_marker_cohort.py`
- lane: `marker-cohort-refresh`
- validates: `schemas/marker-cohort.schema.json`
- description: `Validates and normalizes one dated marker cohort snapshot. Also refuses a Tier 1 or Tier 2 marker that names no ledger source, because a marker claiming measured evidence must name the measurement.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
