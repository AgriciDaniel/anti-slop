---
type: "platform"
title: "Importer ingest review input"
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

# Importer ingest review input

## Adapter Evidence

This importer note was folded from `references/adapter-manifest.json`, section `importers`.

- id: `ingest-review-input`
- path: `scripts/ingest_review_input.py`
- lane: `review-run`
- validates: `schemas/review-input.schema.json`
- description: `Validates and normalizes one review input document into the canonical envelope. Refuses malformed JSON, schema violations, impossible ISO dates, non-http URLs, duplicate ids and dangling marker references with a structured error envelope and a non-zero exit.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
