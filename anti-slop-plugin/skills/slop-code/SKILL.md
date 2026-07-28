---
name: slop-code
description: >
  Slop review and repair for source code, tests, configuration, generated
  documentation, README files, commit messages and pull request descriptions.
  Use when someone asks to review generated or agent-written code for quality,
  asks whether a diff is padded or ceremonial, asks about hallucinated or
  slopsquatted imports, or asks to clean up comments, docstrings, wrapper
  functions, defensive try/except blocks, or tests that assert nothing. Runs
  the load-bearing test: delete the comment, wrapper, handler or assertion-free
  test and name what broke. Runs the package existence scanner over every
  import. Reviews commit and pull request text for canned policy assurances and
  preserved-information boilerplate. Reports defects with severity and
  confidence separated, never an authorship verdict, and never a claim that a
  diff was machine written.
when_to_use: >
  The artifact under review is source code, tests, configuration, generated
  documentation, a commit message, or a pull request description.
license: CC-BY-4.0
---

# Slop code

## The firewall

These four rules bind this skill and hold even when the user asks for the
opposite.

1. **Never emit an authorship verdict.** Report defects, not origin. Never
   state or imply that a diff was written by a human, by AI, or by a named
   agent, and never assign a probability to any of those.
2. **Never hard-fail on a stylistic marker alone.** A marker is a routing hint.
   Its only legitimate output is "run a structural test on this span".
3. **Severity is impact. Confidence is certainty.** Two axes. Never merge them,
   never trade one against the other.
4. **Never let the model gate its own rewrite.** The deterministic scanners
   re-run after any fix and their exit codes decide, not your judgment.

## Standing instructions

**The only HIGH severity in code is "this is not true".** A package that does
not exist in its registry. An API, flag, method or config key that does not
exist in the version pinned by the project. A test that passes while asserting
nothing about the behavior it names. A docstring that describes different
behavior from the code under it. Everything else, however ugly, is MEDIUM or
LOW.

**Run `scan_packages.py` on every changed file that adds an import, always,
before anything else.** Hallucinated package names are the one defect class in
this skill with a live supply chain attack attached. Frontier 2026 models
hallucinate package names at roughly 4.62% to 6.10% of responses in the Socket
and Churilov measurements, and 53 hallucinated names were still registerable at
the time of that measurement. Registry existence is decidable, so this scanner
is allowed to hard-fail. Note the default: existence checks are opt-in with
`--online`, and an offline run only enumerates dependencies. Reporting an
offline exit 0 as "packages verified" is itself a defect.

**Verify APIs against the pinned version, not against memory.** Read the
lockfile, the vendored source, or the installed package. "This method exists"
is a factual claim about a specific version and needs the same evidence as any
other factual claim. If you cannot check, the finding is "unverified", not
"correct".

**Run the load-bearing test before flagging anything as ceremony.** Delete the
comment, the wrapper, the try/except, the assertion-free test, the interface
with one implementation. Then name what broke. If nothing broke, that is the
artifact and the finding is real. If something broke, there is no finding and
you say so. A wrapper you dislike is not a defect.

**Do not flag defensive code without knowing what it defends against.** A
try/except that swallows an exception is a defect when the swallowed error is
one the caller needed. It is correct when the operation is genuinely optional.
The load-bearing test answers this and your aesthetic sense does not.

**Comments describe the thing as it is, not the change that produced it.**
Unless the document is version-scoped (changelog, release note, migration
guide), a comment that narrates a diff is a defect: it stops being true at the
next commit. Rewrite it to describe current behavior.

**Read `../../references/code-markers.md` before you write any code finding.**
It holds the code-specific marker list, the load-bearing test's failure modes,
and the counter-evidence below.

**Be honest that the field's evidence is split.** The strongest numbers
claiming agentic code is worse come from vendors selling engineering
intelligence products. The strongest null result comes from academia: Borg et
al., arXiv 2507.00788, a preprint rather than a published paper, pre-registered
with In-Principle Acceptance granted at ICSME, 151 participants. Its Phase 2
found no significant differences in subsequent code evolution, completion time
or quality; its observational Phase 1 found a 30.7 percent median reduction in
completion time, so cite both phases and never the null alone. A peer-reviewed
MSR 2026 result
(Chowdhury et al.) does find pull requests handled only by code review agents
merge at 45.20% versus 68.37% for human-only. Do not present either side as
settled and do not use either as grounds for an authorship claim about the diff
in front of you.

## Layer 0 for code

Scripts live at `../anti-slop-brain/scripts/` relative to this plugin's parent
directory. Do not reimplement them and do not guess their flags.

Exit codes are uniform: 0 clean, 1 findings, 2 usage error.

| Script | On code | Flag that matters |
|---|---|---|
| `scan_packages.py` | every import resolves to a real registry entry | `--online` required for existence checks; `--allowlist FILE` for internal names |
| `scan_residue.py` | vendor artifacts leaked into comments, docstrings, commit bodies or PR text | `--include-code` to scan fenced blocks and inline code spans, skipped by default in markdown |
| `scan_placeholders.py` | `TODO: quote`, `[Your Name]`, `INSERT_SOURCE_URL`, `YYYY-MM-DD` left in code or docs | `--include-code` as above |
| `scan_refs.py` | URLs and DOIs in comments, READMEs and docstrings | `--online` required for resolution; offline checks shape and checksums only |
| `lint_voice.py` | house style in prose files and in comment text | `--voice FILE` for the banned-token list |

Comment out nothing to make a scanner pass. If a scanner fires on a legitimate
case, record it as a scanner false positive in your report and leave the code
alone.

## The load-bearing test, applied

| Target | Delete it, then ask |
|---|---|
| Comment | Does the code still explain itself, or did the comment carry the only statement of intent, invariant, or gotcha? |
| Wrapper function | Does any caller lose anything, or was it a rename of a single call? |
| try/except | Does a real failure mode now escape uncaught, or was the handler catching something that cannot happen? |
| Test | Does it now fail on a real regression, or does it assert nothing about the named behavior? |
| Abstraction or interface | Is there a second implementation, or a planned one the user can name? |
| Config key | Does anything read it? |
| Type alias or constant | Is it used more than once, or does it name a concept the code needs? |

The artifact is the answer, written out. "Deleted the retry wrapper: nothing
broke, `fetch_user` was its only caller and it passed the arguments through
unchanged" is a finding. "The retry wrapper looks unnecessary" is not.

## Commits and pull request text

Same firewall, same two axes. The tells worth testing, from Wikipedia's
edit-summary section, transfer directly:

- Canned assurance of adherence: "ensured that ... adheres to", "in compliance
  with", "improved", "revised". A human summary says what changed and why. Test
  it by asking whether the summary names a single specific change.
- Mentions of what was preserved or retained. It is unusual for a summary to
  mention material that was not edited.
- Overemphasis on citations, sources or coverage being added.
- Formal first person paragraphs with no abbreviations.

The defect is not the register. The defect is a summary that does not let a
reviewer find the change. That is what you report, and the deletion test is
what proves it: cut the sentence and ask what a reviewer lost.

## Output

Use the `slop-review` template: a Layer 0 table, then findings with an ID,
severity, confidence, location, verbatim quote, test name and artifact, then
the "Not flagged, and why" section. For code, "Location" is
`path/to/file.py:120-134`.

If the user asked for repair as well as review, hand the findings to
`slop-rewrite` rather than editing inside the review pass, or run the two as
explicitly separate passes. Never do both in one breath.

## Depth, loaded on demand

- Read `../../references/code-markers.md` before any code finding.
- Read `../../references/structural-tests.md` for the worked load-bearing
  artifacts.
- Read `../../references/false-positives.md` before flagging a naming,
  formatting or comment-density pattern, and always when the author is a
  non-native English writer.
- Read `../../references/markers-tier2.md` before any finding that rests on
  uniformity of line length, comment density or diff size.
