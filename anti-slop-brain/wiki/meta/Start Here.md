---
type: "meta"
title: "Start Here"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/meta"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[hot|Hot]]"
  - "[[Note Conventions]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[Signs Are Not The Problem]]"
  - "[[What This Brain Does Not Claim]]"
source_urls: []
---

# Start Here

You are in a knowledge base about finding and repairing substance defects in
AI-assisted work. It reports defects. It never reports authorship, and it is
built so that it cannot.

## If you have five minutes

Read [[overview|Overview]]. It contains the one measurement the whole design
rests on: agreement between LLM judges and human slop labels is near zero, so
asking a model whether text looks like slop does not work, and the judge's
errors lean toward the very features that define slop.

## If you have an hour

| Order | Note | Why it comes here |
| --- | --- | --- |
| 1 | [[overview|Overview]] | The argument in one page |
| 2 | [[Signs Are Not The Problem]] | The doctrine everything follows from |
| 3 | [[Why Structural Not Judgmental]] | The measurement that forces the design |
| 4 | [[The Firewall]] | The four rules that constrain every procedure |
| 5 | [[Evidence Tiers]] | How a signal becomes an action, and when it may not |
| 6 | [[What This Brain Does Not Claim]] | The limits, stated flatly |

Read 6 before you rely on anything. It is the shortest route to knowing what
this brain will and will not stand behind.

## If you came to use it rather than read it

The five structural tests live in `procedures/`. Each is a mechanical operation
that produces an artifact you can inspect, not a rating you have to trust.

| Test | Run it when |
| --- | --- |
| [[The Deletion Test]] | A passage feels long and you cannot say why |
| [[The Inversion Test]] | A sentence sounds important and asserts nothing |
| [[The Stranger Test]] | Prose could have been written without the source |
| [[The Attribution Test]] | Something says "studies show" |
| [[The Load Bearing Test]] | Code has comments, wrappers, or tests you suspect are decoration |

The deterministic scanners in `../scripts/` run before any of this. They decide
what is decidable: residue tokens, placeholders, reference integrity, package
existence, house style.

## If you are going to edit this vault

Read [[Note Conventions]] first. The floors are measured, not judged, and
`../scripts/score_substance.py` fails the build when one is missed. In
particular: vary your heading structure. Notes written to a shared outline get
caught as template convergence, which is the vault's own instance of the
problem it documents.

## What is current

[[hot|Hot]] carries the live state, including which sources expire next.
[[log|Log]] carries what changed and when, including the corrections this brain
has had to make to itself.
