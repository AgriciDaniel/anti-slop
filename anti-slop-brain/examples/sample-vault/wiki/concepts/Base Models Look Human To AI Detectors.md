---
type: "concept"
title: "Base Models Look Human To AI Detectors"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/concept"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[wiki/concepts/_index|Concepts Hub]]"
  - "[[Claim Verification Flow]]"
  - "[[Index]]"
  - "[[Dashboard]]"
  - "[[CONVENTIONS]]"
  - "[[Tag Taxonomy]]"
  - "[[Source Intake Workflow]]"
  - "[[Research Refresh Workflow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
  - "[[Source Manifest Guide]]"
  - "[[Best Practices Kernel]]"
  - "[[Health Scorecard]]"
  - "[[Action Roadmap]]"
  - "[[Weekly Report]]"
  - "[[Approval Queue]]"
source_urls:
  - "https://arxiv.org/abs/2605.19516"
---

# Base Models Look Human To AI Detectors

## What It Says

- For Llama3-8B continuations conditioned on human prefixes, GPTZero and Pangram assigned the base model 96.7 percent and 98.8 percent human probability, respectively
- The authors conclude that the tested detectors respond more to instruction-tuning artifacts and local context than to an invariant property of machine-generated text
- Across the tested Llama3 and Qwen3 families, HIP improves the reported tradeoff between semantic preservation and detector-assigned human probability; qualitative round-ten examples vary in both semantic score and detector outcome

## Source

Source: [Base Models Look Human To AI Detectors](https://arxiv.org/abs/2605.19516); type primary; retrieved 2026-09-11; refresh_due 2026-10-11.

> [!gap]
> Ledger confidence is medium/practitioner. Treat this as useful operating evidence, not settled authority, until stronger support is captured.

## Canon Backlink

- Canon ledger entry: [references/canon/022-base-models-look-human-to-ai-detectors.md](../../../../references/canon/022-base-models-look-human-to-ai-detectors.md)
- Source ledger: `references/source-ledger.json`

## Related

- [[Claim Verification Flow]]
- [[Source Intake Workflow]]
- [[Research Refresh Workflow]]
