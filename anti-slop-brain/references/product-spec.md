# Anti-Slop Brain Product Spec

## Buyer

Writers, engineers, and agent operators who ship AI-assisted work and need a defensible, source-cited way to find and fix substance defects without accusing anyone of using AI.

## Domain

detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection

## Core Workflows

- Structural review of a draft, diff, or document
- Deterministic scan for residue, placeholders, and fabricated references
- Evidence-tiered marker triage that routes to structural tests
- Repair pass that consumes findings without re-deriving them
- Marker cohort refresh and evidence re-verification

## Deliverables

- Findings report with severity and confidence on separate axes
- Structural test worksheet showing the artifact for each test
- Deterministic scan report
- Repair diff with re-scan evidence
- Marker cohort refresh log

## Promise

Turn raw sources and recurring decisions into a persistent, source-cited
operating brain.

## Non-Promises

- No authorship verdict, ever; this brain reports defects, not origin
- No hard failure on a stylistic marker alone; markers route to structural tests
- No claim about detector accuracy, marker frequency, or prevalence without a current cited source
- No credentials, tokens, or private operator content in repo artifacts
- No model self-grading as a release gate; deterministic scanners re-run after every repair
