---
type: "procedure"
title: "The Load Bearing Test"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/procedure"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[The Firewall]]"
  - "[[The Deletion Test]]"
  - "[[Code Surface]]"
  - "[[Dependency Surface]]"
  - "[[Commit and Review Surface]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Package Hallucination Evidence]]"
  - "[[Why Structural Not Judgmental]]"
  - "[[Evidence Quality Ladder]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://arxiv.org/abs/2507.00788"
  - "https://arxiv.org/abs/2507.09089"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf"
---

# The Load Bearing Test

In prose, the oracle is a reader who says what they no longer know. In code
there is a better one available, and it does not have opinions: the toolchain.
Delete the construct, run the repository's own gates, and read the exit codes.
A construct that is genuinely holding weight breaks something when it is
removed. A construct that breaks nothing was decoration, whatever it looked
like.

This is the only procedure in this brain whose artifact is produced by a
machine rather than written by a person, which makes it the cheapest to run and
the easiest to fake. The faking is covered at the end.

## The construct table

Each row names a construct, the deletion, and the specific thing that must
break if the construct is load bearing. The right-hand column is the finding
when nothing breaks. Every break condition is a command with an exit code or a
grep with a hit count, so no row terminates in a judgment.

| Construct | Delete | Must break if load bearing | If nothing breaks |
| --- | --- | --- | --- |
| Comment restating the line below it | the comment | a `grep` for the comment's key noun returns no other hit in the repository | no fact was lost; medium severity padding |
| Comment recording a reason, ticket, or vendor quirk | the comment | the same `grep` returns nothing: the reason exists nowhere else | it duplicated a docstring or an ADR; keep the better located copy |
| Passthrough wrapper that only forwards arguments | the wrapper, then redirect callers | type check or import resolution fails, or a test asserting the wrapper's own behaviour fails | an indirection layer with no behaviour; medium severity |
| Defensive `try`/`except` that logs and continues | the handler, keeping the body | a test exercising the failure path fails, or the process now exits non-zero on an input the suite covers | it was suppressing an error nobody has ever seen; high severity, because it converts failures into silence |
| Test with no assertion | the whole test | coverage gate falls below its configured floor | the test proves only that the code does not raise; high severity if it gates a release |
| Ceremonial docstring restating the signature | the docstring | the docs build fails, or a doctest fails, or a public API linter fires | it restates what the signature already says; medium severity |
| Redundant guard clause re-checking a caller invariant | the guard | a test passing the invalid input fails | the invariant is enforced upstream; low severity |
| Re-export module with no additions | the module, then redirect imports | an import fails, or a documented public path breaks | an alias; low severity unless it is a published interface |

The first two rows are the interesting ones, because a comment cannot break a
build by construction. The oracle for comments is therefore not the compiler
but `grep`: a comment is load bearing when the fact it carries exists nowhere
else in the repository. That is still a mechanical check with a countable
result, which is what keeps comments inside this procedure instead of handing
them back to [[The Deletion Test]] on every occasion.

## Running it

1. Confirm a clean working tree and record the commit sha. Every deletion is
   reverted, so the sha is what makes the run reproducible.
2. Delete exactly one construct. Never two. A batch deletion produces one
   ambiguous failure instead of two attributable ones.
3. Run the repository's gates in a fixed order and record each command with its
   exit code verbatim: build, type check, unit tests, integration tests where
   they are cheap, linter, then the targeted `grep` for comment rows.
4. For an assertion-free test, add a step: inject a deliberate fault into the
   code the test claims to cover and confirm the test still passes. A test that
   passes against a broken implementation has been proven to assert nothing,
   and that is a stronger artifact than a coverage percentage.
5. Restore with `git checkout -- <path>` and confirm the tree is clean again
   before the next construct.
6. Classify against the construct table. Record severity and confidence
   separately, per [[The Firewall]].
7. Emit the artifact. The artifact is the command log, not a summary of it.

## Worked: four deletions in one module

```text
BASE: 9f2c41a, working tree clean

DELETE 1  src/loader.py:12  "# increment the retry counter"
  grep -rn "retry_counter" .        -> 3 hits, all code, no other prose
  BROKE: nothing
  VERDICT: padding. severity medium, confidence confirmed. keep deleted.

DELETE 2  src/loader.py:44-46  "# vendor paginates from 1 but reports
          total_pages from 0. ticket 88214, 2026-03-04."
  grep -rn "88214" .               -> 0 hits after deletion
  grep -rn "total_pages" docs/     -> 0 hits
  BROKE: the only record of why the + 1 exists
  VERDICT: load bearing. severity none. restored.

DELETE 3  src/loader.py:70-77  try/except around json.loads, logs and
          returns {}
  pytest tests/test_loader.py      -> 14 passed, exit 0
  mypy src/loader.py               -> exit 0
  BROKE: nothing
  FOLLOW-UP: fed a truncated payload by hand -> process now raises
          JSONDecodeError instead of silently returning {} and writing an
          empty config. No test covered that path in either direction.
  VERDICT: the handler was load bearing for behaviour and invisible to the
          suite. severity high, confidence confirmed. The finding is the
          missing test, not the handler.

DELETE 4  tests/test_config.py::test_defaults  (no assert statement)
  pytest tests/                    -> 41 passed, exit 0
  coverage report                  -> 82.1 percent, floor is 80, exit 0
  MUTATION: set DEFAULT_TIMEOUT = -1 in src/config.py, restored test
  pytest tests/test_config.py      -> 1 passed, exit 0
  BROKE: nothing, in either direction
  VERDICT: assertion-free test. severity high, confidence confirmed. It
          gates the release pipeline and cannot fail. Replace with an
          assertion or remove it from the gate.
```

Delete 3 is the row that justifies the whole procedure. The naive reading of a
green suite after removing a `try`/`except` is that the handler was defensive
padding. The follow-up shows the opposite, and it also shows the real defect,
which was never the handler at all. A procedure that stopped at the exit code
would have produced a confident wrong answer, which is why step 4 exists and
why the artifact records the follow-up rather than the verdict alone.

## The evidence picture, unresolved

This procedure is deliberately local. It decides one construct in one
repository against that repository's own gates. It does not depend on the
population-level question of whether assisted development produces worse code,
and that is fortunate, because the population-level question is not settled and
this note is not going to pretend otherwise.

| Source | Type | Finding | Direction |
| --- | --- | --- | --- |
| `gitclear-copilot-quality-2025` | vendor, 211 million changed lines, 2020 to 2024 | moved or refactored code fell from 24.8 percent in 2021 to 9.5 percent in 2024; copy-pasted code rose from 8.3 to 12.3 percent; an eight-fold increase in blocks of five or more duplicated lines during 2024 | duplication rising |
| `gitclear-maintainability-gap` | vendor, 623 million changes | block duplication rose from 40.3 per million changed lines in 2023 to 73.0 in 2026 year to date, a rise of 81 percent | duplication rising |
| `metr-developer-slowdown` | randomized controlled trial, 16 developers, 246 real tasks | allowing AI increased completion time by 19 percent for experienced developers on mature repositories, while the same developers forecast a 24 percent speedup and still estimated a 20 percent speedup afterwards | slower, and unnoticed |
| `borg-null-result` | preprint (arXiv 2507.00788, not published; In-Principle Acceptance granted at ICSME), 151 participants | Phase 2, pre-registered: no significant differences in subsequent code evolution, completion time, or quality. Phase 1, observational: a 30.7 percent median reduction in completion time | no effect in the pre-registered phase, faster in the observational one |

`borg-null-result` is methodologically the strongest single item in this
literature. It was pre-registered with In-Principle Acceptance before data
collection, which means the analysis was fixed before the numbers existed, and
it has the largest participant count of the four. Its pre-registered phase found
nothing. That result is not a footnote to be walked past on the way to the
alarming figures, and neither is the observational phase that preceded it and
pointed the other way.

The pattern across the table is worth stating explicitly and leaving
unresolved: the strongest slop figures come from vendors selling
engineering-intelligence products, whose commercial interest the findings
serve, and both GitClear entries are correlational by their own account. The
strongest null result comes from academia and is pre-registered.
`metr-developer-slowdown` sits between the two, with a genuine randomised
design and a sample of 16, and its own follow-up in February 2026 could not
obtain a clean signal because developers increasingly refused to work without
assistance. Anyone quoting the 19 percent should quote the 151 alongside it.

The honest position is that the population question is open. That is exactly
why this brain runs a per-construct test against a per-repository toolchain
instead of applying a population claim to a diff. See
[[The Code Slop Disagreement]] for the fuller treatment and
[[What This Brain Does Not Claim]] for the boundary.

## What this test must not become

- **A deletion spree.** The output is a set of artifacts, one per construct.
  Deleting eight things and running the suite once produces one exit code and
  no attribution.
- **A defence of an untested repository.** In a repository with no tests,
  nothing breaks and everything looks like decoration. Where the gates are
  absent the correct finding is that the gates are absent, not that the code is
  padded. Record the gate inventory before the first deletion.
- **An authorship claim.** A passthrough wrapper is a passthrough wrapper
  regardless of who typed it, and human codebases have been accumulating them
  since long before 2022. Rule 1 of [[The Firewall]] applies here identically
  to prose.
- **A licence to delete.** The artifact establishes that nothing broke. Whether
  to keep the deletion is the maintainer's call, and reviewers occasionally
  keep constructs whose value is not visible to any gate. Record it as a
  finding with the artifact attached and let the owner decide.

## Related

- [[The Firewall]]
- [[The Deletion Test]]
- [[The Stranger Test]]
- [[The Attribution Test]]
- [[Code Surface]]
- [[Dependency Surface]]
- [[The Code Slop Disagreement]]
- [[Package Hallucination Evidence]]
- [[Why Structural Not Judgmental]]
- [[index|Index]]
