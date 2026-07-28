<!--
Adapted from "Wikipedia:Signs of AI writing" and WikiProject AI Cleanup,
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing , retrieved
2026-07-27, by Wikipedia contributors. Licensed CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/ . Changes: reorganised into
evidence tiers, false-positive classes added, routed to structural procedures,
and figures replaced with the sources recorded in this project's ledger.
This file and adaptations of it remain under CC BY-SA 4.0.
-->

# Code markers

Load this before writing any finding whose surface is source code, tests,
configuration, generated documentation, a commit message or a pull request
description.

Two things make code different from prose, and both make it easier.

**The load-bearing test is a real experiment.** In prose, deletion is a thought
experiment about meaning. In code, you can actually delete the thing and run
the tests. Do that. The artifact is what happened, not what you expected to
happen.

**Some code claims are decidable.** A package either exists in its registry or
it does not. A method either exists in the pinned version or it does not. A
test either fails when you break the behavior it names, or it does not. These
are the only HIGH-severity findings in code, and they are HIGH because they are
false statements about the world, not because the code is ugly.

Everything else in this file is MEDIUM or LOW, and everything else in this file
requires the load-bearing artifact before it becomes a finding at all.

---

## The load-bearing test, restated for code

**Procedure.** Delete the thing. Run what you can. Name what broke.

**Artifact.** What broke, named specifically. Or "nothing broke", with the
evidence: which callers you checked, which tests you ran, which behavior you
mutated.

**Not an artifact.** "This looks unnecessary." "I would have written this
differently." "The comment adds no value." Those are preferences with the
grammar of findings.

Where you cannot actually run the deletion (no test suite, no build, read-only
review), say so and downgrade confidence, not severity. A finding you could not
test is confidence: low. It is not a finding you get to assert harder.

---

## M1. Redundant comments

**What it is.** A comment that restates the line beneath it in English.

```python
# Increment the counter
counter += 1
```

**Load-bearing test.** Delete the comment. Ask whether the code still states
its own intent, or whether the comment carried the only record of an invariant,
a gotcha, or a reason.

Contrast, where the answer is different:

```python
# The API returns 200 with an empty body when rate limited, so a status check
# alone is not enough here.
if resp.status_code == 200 and resp.json():
```

Deleting that loses the only statement of why the second condition exists, and
the next reader would reasonably simplify the condition and reintroduce the
bug. No finding.

**Severity.** LOW, and only worth reporting as part of a cluster. A single
redundant comment is not worth a reviewer's attention and reporting it costs
you credibility for the HIGH findings in the same report.

**False-positive class.** Teaching codebases, tutorial repositories and
example code comment obvious lines on purpose. Some house styles require a
comment per public declaration. Accessibility: some maintainers rely on
comments for navigation. Check the surrounding file before deciding the
density is anomalous.

---

## M2. Ceremonial docstrings

**What it is.** A docstring that restates the signature. Parameters listed with
their types and no semantics, a Returns line that repeats the return
annotation, a one-line summary that is the function name with spaces in it.

```python
def get_user_by_id(user_id: int) -> User:
    """Get user by id.

    Args:
        user_id: The user id.

    Returns:
        User: The user.
    """
```

**Load-bearing test.** Delete the docstring. Does a caller lose anything? The
question that separates the two cases is whether the docstring answers
something the signature cannot: what happens when the user does not exist, what
the id refers to, which of three plausible behaviors this one implements.

**Severity.** LOW normally. **HIGH when the docstring describes different
behavior from the code under it**, because that is a false statement a reader
will act on. Check this specifically. Documentation drift is the single most
valuable thing to catch on this marker, and it is decidable.

**False-positive class.** Many projects generate API reference documentation
from docstrings and require the full parameter block whether or not it adds
anything. Public library code has different obligations from internal code.
Check for a docs build before flagging.

---

## M3. Passthrough wrappers

**What it is.** A function that renames a call and forwards its arguments
unchanged.

```python
def retry_fetch_user(user_id):
    return fetch_user(user_id)
```

**Load-bearing test.** Find every caller. Delete the wrapper and rewire the
call sites. Name what was lost.

Artifact format:

> Deleted `retry_fetch_user`. Its only caller is `handlers.py:88`, which passed
> its arguments through unchanged to `fetch_user`. Rewired that call site
> directly. Nothing broke and no retry behavior was lost, because the wrapper
> contained no retry logic.

Note the second sentence there. The wrapper's *name* claimed a behavior it did
not implement. That is a second, separate, and more serious finding than the
indirection: a name that lies is closer to M10 than to M3.

**Severity.** MEDIUM. Indirection costs every future reader a jump.

**False-positive class.** Wrappers that exist for a reason you cannot see from
the call site: a seam for dependency injection, a stable public name over a
moving internal one, an adapter that will absorb a signature change, a boundary
enforced by a linter or an import rule. Ask before flagging. If the user can
name the reason, there is no finding.

---

## M4. Over-abstraction

**What it is.** An interface with one implementation. A factory that constructs
one type. A configuration layer with one configuration. A strategy pattern with
one strategy. A base class no one else inherits from.

**Load-bearing test.** Delete the abstraction and inline the single
implementation. What broke? Then ask the question the test cannot answer
alone: is there a second implementation planned, and can the user name it?

**Severity.** MEDIUM.

**False-positive class.** The largest in this file after M6. Test doubles count
as second implementations. Planned work counts when the user can name it.
Public API boundaries count. Plugin systems count even when only one plugin
ships. A framework's required shape counts. This marker is the easiest one in
the file to be wrong about with confidence, so ask before flagging.

---

## M5. Defensive handlers that swallow errors

**What it is.** A try/except (or catch, or `if err != nil { return nil }`) that
discards a failure the caller needed to know about. The strongest form is a
bare catch-all around a block that can fail in several distinct ways, with a
log line and a default return.

```python
try:
    config = load_config(path)
except Exception:
    config = {}
```

**Load-bearing test.** Delete the handler. Does a real failure mode now escape
uncaught, or was the handler catching something that cannot happen? Then, the
sharper version: force the exception and see what the caller does with the
default. If the caller cannot distinguish "no config" from "config file is
corrupt", the handler converted a loud failure into a silent wrong answer.

**Severity.** MEDIUM normally. HIGH when the swallowed error is one the caller
demonstrably needed, because the program now produces a wrong result instead of
stopping.

**False-positive class.** The operation may genuinely be optional: telemetry,
cache warming, a best-effort cleanup, an optional plugin load. Broad handlers
are correct at process boundaries, in request handlers, in supervisor loops and
in plugin hosts, where the whole point is that one failure must not take the
system down. **Do not flag defensive code without knowing what it defends
against.** The load-bearing test answers this; an aesthetic reaction does not.

---

## M6. Generic naming

**What it is.** `data`, `result`, `handler`, `manager`, `process`, `utils`,
`helper`, `info`, `item`, `temp`, `obj`, `do_work`. Names that describe the
shape of a thing rather than what it holds or does.

**Load-bearing test.** This one uses a variant. Rather than deleting, rename
the symbol to what it actually holds, based on reading its uses. If you cannot
produce a specific name after reading every use, that is the finding, and the
artifact is the attempt: "read all four uses of `data`; it holds a decoded
webhook payload in two and a database row in the other two". A name is generic
in a reportable way when the thing itself is doing two jobs.

**Severity.** LOW.

**False-positive class.** Genuinely generic code should have generic names.
`result` is the right name in a three-line function. `item` is the right name
in a comprehension. `T` is the right name for a type parameter. Established
project conventions win. And this marker sits close to the register and fluency
signals that `false-positives.md` shows are unsafe: naming style varies with
the author's first language and with the language community's conventions.
Weigh accordingly.

---

## M7. Assertion-free tests

**What it is.** A test that names a behavior and does not test it.

```python
def test_user_creation():
    user = create_user("alice")
    assert user is not None
```

**Load-bearing test.** Mutate the code under test, then run the test. This is
the highest-value artifact in the file because it is a real experiment with a
binary outcome.

> Replaced the body of `create_user` with `return object()`. The test still
> passes. It asserts that the function returns something, not that a user was
> created, that the name was stored, or that the row reached the database.
> Deleting the test loses no coverage.

**Severity.** HIGH, confidence high. A test that names a behavior and does not
exercise it is a false statement about the state of the codebase, and it is
false in the direction that costs the most: it tells a future maintainer the
behavior is protected when it is not.

**False-positive class.** Smoke tests and import tests are legitimate and are
usually named honestly (`test_imports`, `test_smoke`). A test whose assertion
is weak but whose *name* is modest is not making a false claim. Also check for
assertions hiding in fixtures, in `setUp`, in context managers such as
`pytest.raises`, or in snapshot comparisons: absence of the literal word
`assert` is not absence of an assertion.

---

## M8. Coverage padding

**What it is.** Tests that execute lines without checking outcomes: a
parametrized test over twenty inputs asserting only that no exception was
raised, tests of generated getters and setters, tests that assert a mock was
called with the arguments the test itself just passed in.

**Load-bearing test.** Same mutation procedure as M7, applied to the module
rather than one function. Break a real behavior. Count which tests fail. The
artifact is the count.

> Changed the tax rate constant from 0.2 to 0.3. Of the 34 tests in
> `test_billing.py`, 2 failed. The other 32 assert only that the call returned
> without raising.

**Severity.** MEDIUM. It is a defect in the suite's honesty, not in the
program's behavior, unless someone is relying on the coverage number as a
release gate, in which case say so.

**False-positive class.** Property tests and fuzz tests legitimately assert
"does not crash" and that is their whole point. Contract tests against external
services are often thin on purpose. Regression tests pinned to a specific past
bug can look trivial and be exactly right.

---

## M9. Step-narration comments

**What it is.** `# Step 1:`, `# Step 2:`, or a comment before every block that
narrates the control flow. Also the diff-anchored variant: a comment that
describes the change that produced the code rather than the code.

```python
# This function was added to replace the previous approach of iterating
# through all items, which caused O(n^2) performance.
```

**Load-bearing test.** Delete the comment. For step narration, ask whether the
steps are recoverable from the code, which they usually are because they *are*
the code. For the diff-anchored form there is a second, decisive question: will
this comment still be true after the next commit? A comment anchored to a diff
has an expiry date built into it.

**Severity.** LOW for step narration. MEDIUM for diff-anchored comments,
because they become false rather than merely useless. The repair is to rewrite
the comment to describe current behavior: "This function uses a hash map for
constant-time lookups."

**False-positive class.** Version-scoped documents are exempt entirely:
changelogs, release notes, migration guides, upgrade instructions and ADRs are
*supposed* to narrate change. Numbered steps are correct in a procedure that is
genuinely a procedure, such as a setup script or a runbook. Long algorithms
with a published name benefit from step markers that map to the published
description.

---

## M10. Hallucinated APIs

**What it is.** A method, flag, config key, environment variable, exception
type or signature that does not exist in the version the project pins.

**Load-bearing test.** None. This is not a load-bearing question, it is a
factual one, and it is decidable. Read the lockfile, then read the vendored or
installed source, then check. **Verify against the pinned version, not against
memory.** "This method exists" is a claim about a specific version and needs
the same evidence as any other factual claim.

If you cannot check, the finding is "unverified", not "correct" and not
"fabricated". Say which you could not check and why.

**Severity.** HIGH, confidence follows the method: high when you read the
installed source, medium when you read published documentation for the pinned
version, low when you could only check the current release.

**False-positive class.** Version skew in both directions: the method may exist
in a newer version than your reference, or may have been removed after the one
the project pins. Monkeypatching, plugins, and dynamic attribute definition
mean a method can be real and absent from the source you grepped. Language
servers and type stubs can disagree with runtime.

---

## M11. Hallucinated packages

**What it is.** An import of a package that does not exist in its registry.

**Test.** `scan_packages.py`, always, on every changed file that adds an
import, before anything else in a code review. Note the flag: registry
existence checks are **opt-in** with `--online`, and offline is the default, so
an offline run enumerates dependencies without deciding existence. An offline
run is not a clean bill of health, and reporting it as one is itself a defect.

**Severity.** HIGH, confidence high, always. This is the one defect class in
this file with a live supply chain attack attached: a nonexistent import name
is an open registration slot, and registering it is the attack.

**Evidence.**

- Spracklen et al., USENIX Security 2025: **19.7 percent** of packages
  recommended by code-generating models did not exist, across 16 models and
  576,000 samples. **205,474 unique** hallucinated names. Commercial models
  **5.2 percent** against open-source models **21.7 percent**. **43 percent**
  of hallucinations recurred in all ten reruns of the same prompt, and 58
  percent recurred more than once, which is what makes the names predictable
  enough to squat.
- Churilov, arXiv 2605.17062, 2026-05-16, corroborated by Socket, 2026-07-22,
  across 199,845 responses: 2026 frontier models hallucinate at **4.62 percent
  to 6.10 percent** (Claude Haiku 4.5 at 4.62 percent, GPT-5.4-mini at 6.10
  percent), and **53 hallucinated names remained registerable** at time of
  measurement. Tier: CONTESTED, preprint verified at abstract level.

Read those two together. The rate improved by roughly an order of magnitude,
and the attack still works. The 19.7 percent figure is now a 2024-cohort
number and quoting it as current is an attribution defect.

**False-positive class.** Private and internal registries. Monorepo-local
packages. Namespaced and scoped packages the scanner's registry lookup does not
resolve. Packages installed from a git URL or a local path. Optional
dependencies guarded by a try/except import. Check the project's registry
configuration before reporting, and use `--allowlist` for known-good internal
names rather than silencing the scanner.

---

## Commit messages and pull request descriptions

Same firewall, same two axes. The transferable tells come from the Wikipedia
guide's edit-summary section (WP:AISUMMARY), adapted here under CC BY-SA 4.0:

- **Canned assurance of adherence.** "ensured that ... adheres to", "in
  compliance with", "improved", "revised". The guide's contrast is exact: a
  human writes "removed excessive links per MOS:OVERLINK", while the canned
  equivalent is more verbose and yet less specific.
- **Mentions of what was preserved or retained.** It is unusual for a summary
  to mention material that was not edited.
- **Overemphasis on citations, sources or coverage being added.**
- **Formal first-person paragraphs with no abbreviations.**

**The defect is never the register.** It is a summary that does not let a
reviewer find the change. Prove it with deletion: cut the sentence and name
what a reviewer lost. If the answer is "nothing, because the summary names no
file, no behavior and no reason", that is the finding.

**False-positive class.** Templated PR bodies required by a repository.
Compliance-driven projects that genuinely require an attestation line.
Non-native English writers, who often write more formally. Squash-merge
summaries generated by the forge itself.

---

## The evidence on agentic code, stated unresolved

This section exists so that no finding in this file can be inflated by a claim
about how bad machine-written code is in general. The literature does not
support such a claim, and it does not support the opposite one either. Present
both sides or neither.

**Evidence that code quality is degrading.**

- GitClear, "AI Copilot Code Quality 2025", 211 million changed lines, 2020 to
  2024: moved or refactored code fell from **24.8 percent in 2021 to 9.5
  percent in 2024**; copy-pasted code rose from **8.3 percent to 12.3
  percent**; an **eight-fold increase** in code blocks containing five or more
  duplicated lines during 2024.
- GitClear, "The AI Code Quality Maintainability Gap", January 2026, 623
  million changes: block duplication climbed from **40.3 per million changed
  lines in 2023 to 73.0 in 2026 year to date**, a rise of **81 percent**.
- METR, arXiv 2507.09089, 2025-07-12, a randomized controlled trial with 16
  experienced developers on 246 real tasks in mature repositories: allowing AI
  **increased** task completion time by **19 percent**. The perception gap is
  the striking part. Developers forecast a 24 percent speedup and still
  estimated a 20 percent speedup **after** the trial. Economists forecast 39
  percent and machine learning experts 38 percent.
- Chowdhury et al., MSR 2026, peer reviewed: pull requests handled only by code
  review agents merge at **45.20 percent** against **68.37 percent** for
  human-only.

**Evidence that it is not.**

- Borg et al., arXiv 2507.00788, a **preprint** rather than a published paper,
  **pre-registered with In-Principle Acceptance before data collection** (granted
  at ICSME), 151 participants. Phase 2, the pre-registered comparison, found **no
  significant differences** in subsequent code evolution, completion time, or
  quality. Phase 1, observational, found the opposite direction: a **30.7 percent
  median reduction in completion time**, and an estimated 55.9 percent speedup
  for habitual AI users. Methodologically this is the strongest single item in
  the area, and reporting only its null is an incomplete citation.
- Greptile, across several million pull requests: reverts per 1,000 pull
  requests measured at 1.19 for one agent and 1.80 for another, against a
  **human baseline of 2.72**. Agent pull requests reverted *less* than human
  ones. Vendor data.
- Mao et al., arXiv 2603.27130: real-world differences between AI and human
  contributions are "rather small", with security alerts per KLOC at **12.81**
  for AI against **11.58** for human.
- Stenberg, "High-Quality Chaos", 2026-04-22, on curl's security reports:
  **"the slop situation is not a problem anymore."** curl returned to HackerOne
  on 2026-03-01. Any narrative that stops at the February 2026 shutdown is out
  of date.

**How to read this honestly.** The strongest figures on the degradation side
come from vendors selling engineering-intelligence products, whose commercial
interest the findings serve. The strongest null result comes from a
pre-registered academic study. Neither observation settles the question, and
neither licenses a claim about the diff in front of you. Note also that METR
and GitClear measure different things: METR measures how long a task took,
GitClear measures the shape of the resulting commits. They are not two
measurements of one phenomenon.

Report defects you tested. Do not report a literature.

**One finding here does bind your own process.** Song, Cai and Zhao, arXiv
2606.28438, 2026-06-26, measured AI self-review gates entering a
**"rubber-stamp regime where acceptance scores rise while benchmark
correctness falls."** That is firewall rule 4, and it is why the scanners
re-run after a fix rather than the model declaring itself done.

---

## Layer 0 for code, with real flags

Scripts live at `../anti-slop-brain/scripts/` relative to this plugin's parent
directory. Exit codes are uniform: **0 clean, 1 findings, 2 usage error**.

| Script | Use | Flag that matters |
|---|---|---|
| `scan_packages.py` | dependency existence | `--online` is required for registry existence checks; offline only enumerates. `--allowlist FILE` for internal names. |
| `scan_residue.py` | vendor markers in comments, docstrings, commit bodies, PR text | `--include-code` to scan fenced code blocks and inline code spans, which are skipped by default in markdown |
| `scan_placeholders.py` | placeholder text left in code or docs | `--include-code` as above |
| `scan_refs.py` | URLs and DOIs in comments, READMEs, docstrings | `--online` is required for resolution; offline checks shape and checksums only. Title matching is deliberately out of scope and belongs in the attribution test. |
| `lint_voice.py` | house style in prose files and comment text | `--voice FILE` for the banned-token list |

Do not reimplement them, do not guess flags, and run one with `--help` if you
need options. Do not comment anything out to make a scanner pass. If a scanner
fires on a legitimate case, record it as a scanner false positive in the report
and leave the code alone.
