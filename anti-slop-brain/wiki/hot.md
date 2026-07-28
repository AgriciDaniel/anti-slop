---
type: "hot"
title: "Hot"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/hot"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[log|Log]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[Marker Cohort Rot]]"
  - "[[Note Conventions]]"
  - "[[What This Brain Does Not Claim]]"
source_urls: []
---

# Hot

The working set. What is live, what is about to expire, and what a returning
reader should look at before anything else.

## Live state as of 2026-07-28

| Item | State |
| --- | --- |
| Ledger sources | 43, of which 30 are `source_type: primary` and 4 are vendor |
| Vault notes | 62 Markdown files: 58 content notes plus 4 spine files |
| Earliest refresh due | 2026-08-26, affecting 14 sources |
| Open questions | 0 blocking, 1 resolved and retained |
| Known false claims | 0 outstanding |

## What expires next

Fourteen ledger sources fall due on 2026-08-26. They are the fast-moving tier:
model-specific marker cohorts, detector claims, and regulation. The audit warns
inside a 14 day band and only fails past 14 days overdue, so the window opens
2026-08-12 and closes hard on 2026-09-09.

The cohort figures are the ones that rot fastest. `wu-verbal-tics` carries
per-model indices that will not survive the next frontier release, and
[[Marker Cohort Rot]] gives the re-audit trigger conditions.

## Corrections made on 2026-07-28

An adversarial pass found and this brain fixed:

1. Five ledger entries carried invented descriptive titles that resolved to no
   paper. Identifiers were correct throughout; titles are now the real ones and
   each carries a `title_correction_note`.
2. [[What This Brain Does Not Claim]] asserted that every identifier had been
   confirmed to resolve to a matching title. That was false when written and is
   now recorded as a worked example of the brain's own failure mode.
3. A p-value was wrong by thirteen orders of magnitude and attached to a
   comparison the source never tested.
4. `borg-null-result` was presented as published and as a blanket null. It is a
   preprint, and its Phase 1 found a 30.7 percent median speedup.
5. The blocked MSR 2026 citation was resolved. The paper is real; an earlier
   pass had recorded the wrong identifier.

## Read next

[[overview|Overview]] for the argument, [[The Firewall]] for the rules that
constrain every procedure, [[log|Log]] for what changed and when.
