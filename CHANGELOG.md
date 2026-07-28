# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet.

## [0.1.0] - 2026-07-28

First public release.

### Added

- **anti-slop-plugin**, a Claude Code plugin with five skills (`anti-slop`,
  `slop-review`, `slop-rewrite`, `slop-code`, `slop-verify`), two subagents, and
  tiered marker references. `slop-grader` is read-only (`Read`, `Grep`, `Glob`).
  `slop-verifier` is not: it also holds `Bash` and `WebFetch`, so it can execute
  commands and reach the network.
- **anti-slop-brain**, an Obsidian knowledge base of 62 Markdown files, 58
  content notes plus 4 spine files, with a source ledger of 43 dated entries,
  30 of them `source_type: "primary"` and 4 vendor, each carrying an evidence
  tier and stated limitations.
- **Six deterministic scanners**: residue, placeholders, reference integrity,
  package existence, house voice, and vault substance. Offline by default; no
  third-party dependencies.
- **Two adapter lanes**, review run and marker cohort refresh, with JSON
  schemas, fixtures, and determinism tests.
- **The firewall**, enforced in the output schema rather than in prompts: no
  authorship verdict, no hard failure on a stylistic marker alone, severity and
  confidence on separate axes, no model self-gating.
- **The five structural tests**: deletion, inversion, stranger, attribution,
  and load bearing. Each terminates in a verifiable artifact.
- **`research/verification-ledger.md`**, recording eight corrections to figures
  that circulate incorrectly in this field.
- 314 tests, and continuous integration that runs all of them plus gates for
  long dashes, local absolute paths, dead wikilinks, manifest validity, and
  skill frontmatter.

### Fixed before release

An adversarial verification pass, instructed to break the project rather than
confirm it, found and this release corrects:

- Five source-ledger entries carried invented descriptive titles that resolved
  to no paper. The identifiers were always correct and nothing was fabricated.
- The project's own limitations note asserted a verification that had not been
  performed. The claim is replaced with a table separating what was checked
  from what was not, and the error is documented rather than removed.
- A p-value was wrong by thirteen orders of magnitude and attached to a
  comparison its source never tested.
- A cited null result was described as published when it is a preprint, and its
  first phase, which found the opposite direction, was omitted.
- The firewall could be bypassed by hand-writing an adapter envelope.
- The audit would have dropped from market-ready to scaffolded on 2026-08-27 on
  the calendar alone. There is now a fourteen day warning band.
- 36 dead wikilinks existed in the shipped vault because the only link check
  ran against the template vault.

### Known limitations

- Most 2026 citations are preprints verified at abstract level, and are tiered
  `CONTESTED` rather than `EVIDENCE-BASED`.
- Marker lists have a shelf life. Vocabulary shifts by model generation and
  human usage is converging on model usage.
- The AI code quality literature is genuinely unsettled and is presented that
  way, including the pre-registered null result that cuts against the thesis.

[Unreleased]: https://github.com/AgriciDaniel/anti-slop/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AgriciDaniel/anti-slop/releases/tag/v0.1.0
