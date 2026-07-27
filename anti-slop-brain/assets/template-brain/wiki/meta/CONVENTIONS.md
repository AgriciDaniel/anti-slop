---
type: "meta"
title: "CONVENTIONS"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "evergreen"
created: "{{date}}"
updated: "{{date}}"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/meta"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Start Here]]"
  - "[[Index]]"
  - "[[Dashboard]]"
  - "[[Tag Taxonomy]]"
  - "[[Source Intake Workflow]]"
  - "[[Claim Verification Flow]]"
  - "[[Corpus Scope Policy]]"
  - "[[Memory Governance Policy]]"
  - "[[CONVENTIONS]]"
  - "[[Research Refresh Workflow]]"
  - "[[Synthesis Workflow]]"
  - "[[Reporting Workflow]]"
  - "[[Source Manifest Guide]]"
  - "[[Best Practices Kernel]]"
  - "[[Health Scorecard]]"
  - "[[Action Roadmap]]"
  - "[[Weekly Report]]"
  - "[[Approval Queue]]"
  - "[[wiki/flows/_index|Flows Hub]]"
  - "[[wiki/sources/_index|Sources Hub]]"
  - "[[wiki/concepts/_index|Concepts Hub]]"
  - "[[wiki/decisions/_index|Decisions Hub]]"
  - "[[wiki/deliverables/_index|Deliverables Hub]]"
  - "[[wiki/reports/_index|Reports Hub]]"
  - "[[wiki/questions/_index|Questions Hub]]"
  - "[[wiki/gaps/_index|Gaps Hub]]"
  - "[[wiki/experiments/_index|Experiments Hub]]"
source_urls: []
---

# Conventions

This is the master vault operating contract. Agent harness files summarize it, but this note owns note shape, frontmatter, tags, confidence, and release hygiene.

## Layers

- `.raw/` stores immutable source material with sha256 provenance in `.raw/.manifest.json`.
- `wiki/` stores curated notes, hubs, flows, concepts, questions, gaps, experiments, deliverables, and reports.
- `references/` stores source ledgers, adapter manifests, claim ledgers, canon, and release evidence.
- `agents/` stores grounded operating roles.

## Frontmatter Contract

Use flat YAML. Required fields for wiki notes: type, title, domain, status, created, updated, tags, confidence, related, and source_urls. Use ISO dates after client vault creation. Keep titles unique across the vault.

Tags are quoted YAML list items and include exactly one domain tag, one type tag, and one confidence tag:

- `#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and`
- `#type/<type>`
- `#confidence/evidence-based`, `#confidence/practitioner`, `#confidence/contested`, or `#confidence/folklore`

See [[Tag Taxonomy]] before adding a new tag family or graph color.

## Body Contract

Start with an answer-first summary. Then include sources, related links, confidence, caveats, and next action where relevant. Deliverables and reports must cite a wiki source note, `.raw/` path, or sha256.

## Confidence Contract

Confidence policy: evidence-based | practitioner | contested | folklore. Every claim uses exactly one lowercase confidence value and matching `#confidence/<level>` tag. Ledger confidence maps high -> evidence-based, med -> practitioner, and low -> contested. SINGLE-SOURCE rows stay visibly marked in `references/claim-ledger.md`.

## Quote And Paraphrase Contract

Prefer paraphrase with a source URL or source note. When exact words matter, use a short attributed quote, keep it visibly sourced, and do not copy long passages into wiki notes.

## Link Contract

Prefer resolving wikilinks to wiki notes. Use plain markdown links or code paths for reference files when a vault linter cannot resolve them.

## Publish Contract

Public publishing follows `PUBLISHING_NOTICE.md`, the `site/` sanitizer, and public exclusions. `.raw/` is never public.

## Related

- [[Start Here]]
- [[Index]]
- [[Dashboard]]
- [[Tag Taxonomy]]
- [[Source Intake Workflow]]
- [[Claim Verification Flow]]
- [[Corpus Scope Policy]]
- [[Memory Governance Policy]]
