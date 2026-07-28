---
name: anti-slop
description: >
  Router for the anti-slop toolkit. Use when someone asks to review, clean,
  de-slop, humanize, or quality-check prose, documentation, code, commit
  messages, PR descriptions, or agent output, or asks whether some writing
  "sounds like AI". Also use for verifying citations, DOIs, links and imported
  package names, for stripping vendor residue markers such as oaicite or cite
  spans, and for auditing padding, filler, puffery, vague attribution and
  hollow analysis. Explains the three layers (deterministic scanners,
  structural procedures, evidence-tiered soft signals) and picks the right leaf
  skill: slop-review for read-only findings, slop-rewrite for repair, slop-code
  for code and docs, slop-verify for citations, links and packages. Never
  produces an authorship verdict and never treats a stylistic marker as proof
  of anything. Use this hub only when the surface or the operation is unclear;
  otherwise invoke the leaf skill directly.
when_to_use: >
  The user wants slop detection or repair but has not said which surface (prose,
  code, docs, citations) or which operation (review, rewrite, verify) applies.
license: CC-BY-4.0
---

# Anti-slop

## The firewall

These four rules bind every skill and agent in this plugin. They are not
advice, they are not a checklist step, and they hold even when the user asks
for the opposite.

1. **Never emit an authorship verdict.** Report defects, not origin. Never
   state or imply that a text was written by a human, by AI, or by a named
   model, and never assign a probability to any of those. Say what is wrong
   with the artifact and where.
2. **Never hard-fail on a stylistic marker alone.** A marker is a routing hint.
   Its only legitimate output is "run a structural test on this span".
3. **Severity is impact. Confidence is certainty.** Two axes. Never merge them
   into one score, never trade one against the other.
4. **Never let the model gate its own rewrite.** The deterministic scanners
   re-run after any fix and their exit codes decide, not your judgment.

Rule 1 exists because the measurement says the model cannot do the judging.
LLM-as-judge agreement with human slop labels is near zero (kappa 0.01 for
GPT-5, -0.01 for DeepSeek-V3, 0.03 for o3-mini; Shaib, Chakrabarty,
Garcia-Olano and Wallace, arXiv 2509.19163, rev. 2026-01-24), models under-flag
by roughly 5x, and span-level extraction runs at precision 0.14 and recall
0.11. Rule 1 also exists because authorship guessing has a measured victim:
see `../../references/false-positives.md`.

## The three layers

**Layer 0, deterministic scanners.** Python scripts with exit codes. The only
things allowed to hard-fail, because they are the only things actually
decidable. They live in the sibling brain repo at `../anti-slop-brain/scripts/`
relative to this plugin's parent directory.

| Script | Decides |
|---|---|
| `scan_residue.py` | vendor artifacts: `oaicite`, `[cite: 1]`, lenticular-bracket citations, `(start_span)`, `grok-card`, `:::writing{`, `[attached_file:1]`, `utm_source=chatgpt.com`, `referrer=grok.com` |
| `scan_placeholders.py` | `[Your Name]`, `INSERT_SOURCE_URL`, `access-date=2025-XX-XX`, `YYYY-MM-DD`, `TODO: quote` |
| `scan_refs.py` | DOI, ISBN and arXiv shape and checksums offline; resolution of DOIs, arXiv IDs and URLs with `--online` |
| `scan_packages.py` | dependency inventory offline; registry existence with `--online` |
| `lint_voice.py` | house style: no U+2014, no U+2013, no ` -- `, plus banned tokens from a voice file |
| `score_substance.py` | near-duplicate, skeleton-reuse and specific-word-density floors over a note vault, via `--vault DIR` |

Run them, read their exit codes, quote their output. Exit codes are uniform: 0
clean, 1 findings, 2 usage error. Do not reimplement them and do not guess
their flags; run one with `--help` if you need options.

Two defaults matter and are easy to misreport. `scan_refs.py` and
`scan_packages.py` are **offline by default** and decide nothing about
resolution or registry existence until you pass `--online`. An offline run is
not a clean bill of health. `scan_refs.py` also does not compare a cited title
to the resolved title; that comparison is deliberately a Layer 1 attribution
test with a human-readable artifact, not a scanner output.

`lint_voice.py` enforces a house rule. Its findings are style violations, never
slop verdicts.

**Layer 1, structural procedures.** Five mechanical tests. Each produces a
named artifact, so the finding is checkable by someone who does not trust you:
deletion, inversion, stranger, attribution, load-bearing. Summarised below,
worked in `../../references/structural-tests.md`.

**Layer 2, evidence-tiered soft signals.** Markers, ranked by how well the
corpus evidence supports them. Tier 1 is corpus-validated, tier 2 is measured
but high false-positive, tier 3 is folk wisdom that is recorded and never acted
on alone. A Layer 2 hit does exactly one thing: it selects a span for a Layer 1
test.

## The five structural tests

1. **Deletion.** Cut the span. Name what was lost. If nothing was lost, it was
   padding. Artifact: the cut span plus the named loss.
2. **Inversion.** Negate the claim and write the negation out. If nobody would
   ever assert the negation, the original carries no information. Artifact: the
   negation, in full.
3. **Stranger.** Could someone who never read the source have written this? If
   yes, it is generic. Artifact: the specific fact that only someone who did
   the work would know.
4. **Attribution.** Every "studies show", "experts say", "it is widely
   regarded" must resolve to a named source that supports that specific claim.
   Artifact: the resolved citation, or the finding.
5. **Load-bearing (code).** Delete the comment, the wrapper, the try/except,
   the assertion-free test. What broke? Artifact: what broke, or nothing.

A test you did not actually run produces no artifact and therefore no finding.
Never report a structural finding without its artifact.

## Routing

| Ask | Skill |
|---|---|
| "review this", "is this slop", "what is wrong with this draft" | `slop-review` |
| "fix it", "clean this up", "de-slop this", "rewrite" | `slop-rewrite` |
| code, tests, comments, READMEs, commit messages, PR descriptions | `slop-code` |
| citations, DOIs, dead links, imported packages, vendor residue | `slop-verify` |

Order matters when more than one applies. `slop-verify` first, because
fabricated citations and hallucinated packages are the only HIGH-severity
defect class that a rewrite can silently launder. Then `slop-review`. Then
`slop-rewrite`, which consumes the review's findings and never re-derives them.

For a fresh-context second opinion, dispatch the `slop-grader` agent (read-only
findings) or the `slop-verifier` agent (adversarial check of an existing
review). Never dispatch either to approve your own output as finished; that is
firewall rule 4.

## Standing prohibitions

- Never report a percentage, likelihood or score for "how AI-generated" a text
  is. There is no such number in this plugin.
- Never quote a statistic that is not in
  `../../references/` or in the project's verification ledger. If you want a
  number that is not there, omit the number.
- Never remove a marker without fixing the defect underneath it. Wikipedia's
  own guidance on the sign list is that the patterns are potential signs of a
  problem and not the problem itself, and that treating the signs as the thing
  to be fixed can just make the underlying problem harder to see.
- Never write U+2014 (em dash) or U+2013 (en dash) in any output. Use commas,
  periods, colons or parentheses.
- Never strip hedges, qualifiers or "filler" mechanically. Wikipedia's own
  observed human-writing signals include "in order to", "as a result of", "the
  fact that", "very", "perhaps" and "tends to". Removing them makes text read
  more generated, not less.

## Depth, loaded on demand

- Read `../../references/structural-tests.md` when you are about to run a
  structural test and need the worked artifact format.
- Read `../../references/markers-tier1.md` when you need the corpus-validated
  marker list and its citations.
- Read `../../references/markers-tier2.md` when a finding rests on em-dash
  density, burstiness or sentence-length uniformity.
- Read `../../references/markers-tier3.md` when you are tempted to flag a
  single word or an unsourced heuristic.
- Read `../../references/code-markers.md` when the surface is code, tests,
  config or generated documentation.
- Read `../../references/false-positives.md` before writing any finding whose
  evidence is style rather than substance, and always before reviewing text by
  a non-native English writer.
