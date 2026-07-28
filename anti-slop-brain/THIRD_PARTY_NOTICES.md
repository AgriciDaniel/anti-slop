# Third-Party Notices

This brain adapts and depends on third-party material. Each item below records
what was taken, from where, and under which licence.

## Adapted material

### Wikipedia: Signs of AI writing, and WikiProject AI Cleanup

Source: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
Licence: Creative Commons Attribution-ShareAlike 4.0 International.
Used for: the marker taxonomy, the ineffective-indicators list, the citations
and markup defect categories, and the doctrine that the signs are not the
problem itself. A wikitext snapshot was captured during the build and is
retained locally under the repository-root `.research/` directory, which is
gitignored and therefore not published; readers get the live guide at the URL
above instead of a mirrored copy. Attribution is required by the licence and is
given in every note that draws on the guide.

### blader/humanizer

Source: https://github.com/blader/humanizer
Licence: MIT.
Used for: comparative analysis of prior art only. No text was copied into this
brain. The repository is documented in the source ledger as
`blader-humanizer`, including its gaps, so that this brain's scope is defined
against it rather than duplicating it.

### Claude Blog Brain wiki substance scorer

Source: local sibling project, `scripts/audit_brain.py`.
Used for: `scripts/score_substance.py` is a port and generalisation of the
`check_wiki_substance` and `score_wiki_substance` functions and their helpers.
Thresholds were retained unchanged. The origin is credited in the module
docstring.

### claude-blog prose linter

Source: local sibling project, `scripts/lint_prose.py`.
Used for: `scripts/lint_voice.py` is a clean reimplementation of its rule set
and of its fence-aware and backtick-aware dash detection, built against this
repository's own `scripts/scan_common.py` helpers. The origin is credited in
the module docstring. It is a design credit, not a dependency: `lint_voice.py`
imports nothing from that project and runs on the standard library alone.

### impeccable plugin

The two-tier detection methodology that reached this brain by way of
claude-blog originates in the impeccable plugin by Paul Bakaus, Apache
Licence 2.0. Credit is recorded here because the lineage is real even though
no code was copied directly.

## Dependencies

This brain uses the Python standard library only. It declares no third-party
runtime dependencies, so no further licence notices are required.
