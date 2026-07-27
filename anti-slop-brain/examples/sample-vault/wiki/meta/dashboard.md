---
type: "dashboard"
title: "Dashboard"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "evergreen"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/detection-and-repair-of-ai-slop-in-prose-code-documentation-and"
  - "#type/dashboard"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Start Here]]"
  - "[[CONVENTIONS]]"
  - "[[Tag Taxonomy]]"
  - "[[Index]]"
  - "[[Overview]]"
  - "[[Hot]]"
  - "[[Log]]"
  - "[[No peer-reviewed study measures commercial humanizer output with human raters or]]"
  - "[[Which marker cohorts have shifted since the current ledger snapshot]]"
  - "[[Deletion-test spot check against a known-padded corpus sample]]"
  - "[[Dashboard]]"
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

# Dashboard

Dataview views over the vault require the Dataview community plugin. Without Dataview, use the linked seed lists and run `python3 scripts/audit_brain.py --json` for the same gate signals.

## Visual Map

![[brain-relationship-map.svg]]

## Notes by status

```dataview
TABLE status, domain, confidence, updated
FROM "wiki"
WHERE type != "meta"
SORT status ASC, updated DESC
```

## Seeds needing substance

```dataview
LIST
FROM "wiki"
WHERE status = "seed"
SORT file.name ASC
```

## Contested and low-confidence claims

```dataview
LIST
FROM "wiki"
WHERE confidence = "contested" OR contains(tags, "#confidence/contested") OR contains(tags, "#confidence/folklore")
SORT updated DESC
```

## Recently updated

```dataview
TABLE updated, status, confidence
FROM "wiki"
SORT updated DESC
LIMIT 15
```

## Seed Evidence Queue

### Gaps

- [[No peer-reviewed study measures commercial humanizer output with human raters or]]
- [[Evidence Coverage Not Yet Verified]]

### Questions

- [[Which marker cohorts have shifted since the current ledger snapshot]]
- [[What Current Official Source Resolves The Highest Risk Claim]]

### Experiments

- [[Deletion-test spot check against a known-padded corpus sample]]
- [[Source To Claim Spot Check Probe]]

Watch for `> [!gap]`, `> [!question]`, `> [!contradiction]`, `> [!stale]`, and `> [!done]` callouts in seed notes.

## Operating Links

- [[Source Intake Workflow]]
- [[Research Refresh Workflow]]
- [[Claim Verification Flow]]
- [[Explore Plan Code Commit]]
- [[Multi-Agent Fan-Out Research Flow]]
- [[Context Compaction Routine]]
- [[Synthesis Workflow]]
- [[Reporting Workflow]]
- [[Approval Queue]]
- [[Health Scorecard]]
- [[Action Roadmap]]
