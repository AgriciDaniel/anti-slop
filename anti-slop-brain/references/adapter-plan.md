# Anti-Slop Brain Adapter Plan

Status: required before domain-adapted maturity.

## Raw Input Types

- Drafts, diffs, commit messages, pull request descriptions, agent transcripts, and documents supplied by the operator

## Required Implementation

- Define one schema per raw input type.
- Build at least one real domain importer or ingestion path.
- Build one domain-specific synthesis module.
- Build one report renderer with source citations.
- Add sanitized fixtures and tests for every supported input type.

## Safety Refusals

- No authorship verdict, ever; this brain reports defects, not origin
- No hard failure on a stylistic marker alone; markers route to structural tests
- No claim about detector accuracy, marker frequency, or prevalence without a current cited source
- No credentials, tokens, or private operator content in repo artifacts
- No model self-grading as a release gate; deterministic scanners re-run after every repair

## Completion Gate

This plan is complete only when domain-specific importer, synthesis, report,
fixtures, and tests replace the generic scaffold.
