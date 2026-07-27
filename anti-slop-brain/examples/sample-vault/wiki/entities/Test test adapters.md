---
type: "entity"
title: "Test test adapters"
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

# Test test adapters

## Adapter Evidence

This test note was folded from `references/adapter-manifest.json`, section `tests`.

- id: `test-adapters`
- path: `tests/test_adapters.py`
- covers: happy path for both lanes, importer to synthesis to renderer, determinism: every stage run twice and compared byte for byte, malformed JSON produces a structured error envelope and a non-zero exit, never a traceback, an invalid ISO date is rejected, in the document, on the flag and in a refresh_due, a non-http URL is rejected, for file, javascript and ftp schemes, a finding with no evidence span is refused, a Tier 2 marker alone produces no finding, only a routed procedure suggestion, no output object anywhere contains an authorship verdict key, no long dash characters in any adapter source, schema or fixture, this manifest resolves on disk and is marked domain adapted
- description: `Plain script with main() -> int, matching tests/test_pipeline.py and tests/test_scanners.py. Writes only inside tempfile.TemporaryDirectory.`
- status: `implemented`
- planned: `False`


## Manifest Backlink

- Adapter manifest: `references/adapter-manifest.json`

## Related

- [[Dashboard]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
