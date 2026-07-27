---
type: "surface"
title: "Knowledge Base Surface"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/surface"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Note Conventions]]"
  - "[[Distributional Convergence]]"
  - "[[Model Collapse]]"
  - "[[Documentation Surface]]"
  - "[[Prose Surface]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Regulation and Governance]]"
  - "[[Corpus Study Method]]"
  - "[[Agent Output Surface]]"
  - "[[Why Structural Not Judgmental]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models/RfC"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2604.23178"
  - "https://doi.org/10.1038/s41586-024-07566-y"
---

# Knowledge Base Surface

Wikis, team handbooks, personal note vaults, and second brains fail in a way
essays do not. An essay can be padded on its own. A knowledge base degrades
**between** its notes: forty pages that each look acceptable in isolation and,
read together, turn out to be one page written forty times. This vault is
graded on that failure, by a script, on every build.

## The between-note defects

| Defect | What it looks like | Why isolated review misses it |
| --- | --- | --- |
| Near-duplicate notes | two pages covering the same ground with different titles | each page is fine; only the pair is the problem |
| Shared heading skeleton | every note running Background, Key points, Considerations, Summary | the outline is defensible once, and empty by the tenth use |
| Anchor reuse | the same opening sentence, lightly varied, across a folder | the sentence reads well; the repetition is invisible per page |
| Pasted citation bundles | six identical sources at the foot of unrelated notes | the sources are real, and none of them was read for this note |
| Topic drift into restatement | a new note that only reorganises an old one | it adds a page and no information |
| Orphan notes | a page nothing links to and that links nowhere | link health is a graph property, not a page property |
| Confidence inflation | a note asserting more than the source it cites | the assertion is well written and unsupported |

The mechanism behind the first four is [[Distributional Convergence]]: when many
notes are generated to the same outline, the outline becomes the content. The
long-run version is [[Model Collapse]]: `shumailov-model-collapse`, published in
Nature, found that recursive training on generated data causes early collapse in
which distribution tails and variance are lost, then late collapse to a
low-variance point estimate. That result assumes data replacement rather than
accumulation, so the analogy is a direction and not a proof. A vault written
mostly by generation, then fed back as context for more generation, is the same
loop at small scale inside one repository.

## The floors, and what each one prevents

`scripts/score_substance.py` measures nine things and fails the build on any of
them. None of the checks asks whether the writing is good and none asks who
wrote it, which is what makes them Layer 0 work under
[[Why Structural Not Judgmental]].

| Floor | Threshold | Defect it prevents | Why the number is where it is |
| --- | --- | --- | --- |
| Near-duplicate similarity | below 0.82 | two notes saying the same thing | 8-token shingle Jaccard; 0.82 clears legitimate topical overlap |
| Heading skeleton reuse | at most 3 notes share one | template convergence | three notes can share an outline honestly; a fourth is a template |
| Anchor line reuse | at most 2 notes share one line | copy-pasted opening sentences | measured on lines of 12 or more words, so short shared lines are ignored |
| Generic citation bundle | a set of 6 or more sources reused by at most 3 notes | pasted reference blocks | a compact 2 to 5 source set can be correct scholarship for a folder |
| Note-specific words | 120 minimum per note | boilerplate shared across many notes | counted only on lines unique to that note |
| Table or procedure coverage | 0.90 of notes | prose that never commits to specifics | a table or a numbered procedure of at least three steps |
| Specific citation coverage | 0.95 of notes | single-source assertions | each note cites at least 2 ledger ids, and not a reused bundle |
| Note length | 80 lines mean | thin stubs padded out with headings | a mean, so short notes are allowed if others carry weight |
| Wikilinks | 8 mean per note | orphan notes that never join the graph | also a mean |

Three of these deserve a second look because they are the ones that catch
machine-assisted vault building specifically.

**Note-specific word count** is computed only on lines that appear in this note
and nowhere else in the vault. Padding a note with material that also appears
elsewhere raises the line count and lowers this number at the same time. It is
the one floor that cannot be gamed by writing more.

**Anchor reuse at 2** is stricter than it sounds. Two notes may share a long
sentence, three may not. In practice this bans the habit of opening every note
in a folder with the same framing clause, which is the single most visible tell
of a vault written in one pass.

**Generic bundle reuse** targets a specific dishonesty. Four notes carrying an
identical set of six or more sources is evidence that the sources were pasted
rather than consulted, because four genuinely different topics rarely rest on
exactly the same six references. A small shared set is fine; the rule only fires
at six or more.

## Reading the current score

The scorer prints a score out of 100 and the metrics behind it. The score is
derived, so read the metrics rather than the number:

- `near_duplicate_pairs` above zero caps the score at 40 regardless of anything
  else, because a duplicate pair is a structural failure rather than a
  deduction.
- `max_skeleton_reuse`, `max_anchor_reuse`, and `generic_bundle_reuse` each cost
  up to 10 points when exceeded.
- `table_or_procedure_coverage` costs up to 15, `specific_citation_coverage` up
  to 20, and notes under the density floor up to 15.
- `spoke_count` is the scored population. If the `--note-type` argument does not
  name every type in the vault, the population is empty and the score reads
  zero, which looks like catastrophic failure and is a usage error.

That last point is worth stating because it is a real trap. This vault splits
content across `concept`, `marker`, `procedure`, and `surface`, so all four must
be passed or the run is meaningless.

## The implementation, and where it came from

The scorer is a **port of the wiki substance checks from Claude Blog Brain**,
specifically the `check_wiki_substance` and `score_wiki_substance` functions of
that project's `scripts/audit_brain.py`, together with their helpers. The
thresholds, the shingle size, the scoring weights, and the citation-bundle
reasoning were carried over unchanged. What is new here is that it stands alone:
it takes a vault path and a ledger path rather than assuming one repository
layout.

Recording the provenance is not modesty, it is the same rule this vault applies
to every other borrowed figure. An unattributed port is a reuse defect of
exactly the kind the script exists to detect, and [[Note Conventions]] would
require the attribution even if courtesy did not.

## What the floors do not catch

A vault can pass every check above and still be bad. Naming the gap keeps the
score from being mistaken for a quality verdict.

- **Wrong facts.** Nothing here checks whether a cited number matches its
  source. That is human work, and the register in this vault's evidence folder
  exists because it is human work that gets skipped.
- **Wrong sources.** A note citing two real ledger ids that do not support its
  claim passes citation coverage. [[Evidence Quality Ladder]] is the control.
- **Stale notes.** Freshness is a frontmatter and refresh-date question, not a
  substance one.
- **Useful things absent.** No count detects a missing note.
- **Holistic quality.** Asking a model to rate the vault is not a substitute:
  `shaib-measuring-slop` reports LLM-as-judge agreement with human slop labels
  at kappa 0.01 for GPT-5, minus 0.01 for DeepSeek-V3, and 0.03 for o3-mini,
  with models flagging at 0.03 to 0.08 against a human rate of 0.34. And
  `soumik-judging-the-judges` finds judge style bias from 0.10 to 0.76 with
  markdown preferred over plain text, so a model asked to grade a vault would
  reward exactly the over-formatting this surface is trying to catch.

## The governance precedent

The largest knowledge base in the world reached a compatible answer through
community process rather than through a script. `wikipedia-llm-guideline`
records an RfC closing 2026-03-20 by 44 to 2 under SNOW, prohibiting the use of
LLMs to generate or rewrite article content, with two exceptions, copyediting
your own writing and LLM-assisted translation, both under mandatory human
review. It is a content guideline rather than a policy, a distinction developed
in [[Regulation and Governance]].

The companion page, `wikipedia-signs-of-ai-writing`, is the descriptive
counterpart and the source most of this field derives from. Its own warning is
the one this surface has to internalise: the listed patterns are potential signs
of a problem rather than the problem itself, and treating the signs as the
things to fix could just make detection harder. A vault that renamed its
headings to dodge the skeleton check while leaving forty interchangeable notes
in place would have done precisely that.

## Adding a note without lowering the score

1. **Write the organising principle first**, in one sentence, before any
   headings exist. If it matches an existing note's principle, extend that note
   instead of adding one.
2. **Derive the headings from the principle.** A note about a disagreement
   should not have the headings of a note about a procedure.
3. **Vary the opening sentence deliberately.** Check the first line against the
   folder's other first lines before writing the second paragraph.
4. **Cite from what the note actually needs**, at least two ledger ids, and
   never by copying another note's source block.
5. **Include one real table or one numbered procedure of at least three steps.**
   Not both by reflex; whichever the content earns.
6. **Run the scorer with every note type named**, then the long-dash grep, then
   the vault linter.
7. **Read the metrics rather than the score**, and treat any near-duplicate pair
   as a merge decision rather than a rewrite task.

## Related

- [[Note Conventions]]
- [[Distributional Convergence]]
- [[Model Collapse]]
- [[Documentation Surface]]
- [[Prose Surface]]
- [[Agent Output Surface]]
- [[Evidence Quality Ladder]]
- [[Corpus Study Method]]
- [[Regulation and Governance]]
- [[Why Structural Not Judgmental]]
- [[index|Index]]
