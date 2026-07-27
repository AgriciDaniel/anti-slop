# Product Boundaries

Anti-Slop Brain is an advisory, read-only Obsidian brain for detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection.

## It Does

- Preserve raw sources under `.raw/`.
- Synthesize source-cited notes and deliverables.
- Maintain action queues, reports, and next actions.
- Keep decisions auditable through source links and rollback notes.
- Gate maturity through `references/source-ledger.json`,
  `references/adapter-manifest.json`, and `scripts/audit_brain.py`.

## It Does Not

- No authorship verdict, ever; this brain reports defects, not origin
- No hard failure on a stylistic marker alone; markers route to structural tests
- No claim about detector accuracy, marker frequency, or prevalence without a current cited source
- No credentials, tokens, or private operator content in repo artifacts
- No model self-grading as a release gate; deterministic scanners re-run after every repair

## Safety Risks

- False accusation of AI authorship, which peer-reviewed work shows falls hardest on English-language learners
- Marker lists rotting as model cohorts shift and human speech converges on LLM vocabulary
- Vendor marketing quoted as measured research
- Surface repair that removes the sign while leaving the substance defect intact
- Rubber-stamp regime where model self-review raises acceptance while correctness falls

## Maturity Boundary

This repo starts as `scaffolded`. Market-ready quality requires current
research, domain adapters, deterministic demo verification, source citations,
Obsidian graph hygiene, and release scans. The audit score is capped below 90
until those stages are complete.
