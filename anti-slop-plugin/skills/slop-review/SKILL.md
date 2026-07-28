---
name: slop-review
description: >
  Read-only slop review of prose, documentation, reports, agent output, commit
  messages or PR descriptions. Use when someone asks what is wrong with a
  draft, asks for an editorial or quality review, asks whether text is padded,
  vague, puffed up, unsourced or hollow, or asks whether writing "sounds like
  AI". Produces a fixed findings report where every finding carries a verbatim
  quote, a severity (HIGH for a fabricated fact, citation or API, MEDIUM for
  padding or filler that changes nothing if cut, LOW for stylistic tells) and a
  separate confidence (low, medium, high), plus the artifact from the
  structural test that produced it. This skill diagnoses only. It cannot write
  or edit files, it never rewrites the text it is judging, and it never states
  or implies who or what wrote the text. Hand its findings to slop-rewrite when
  the user wants repair.
when_to_use: >
  A diagnosis is wanted, not a repair, and the surface is prose or documentation
  rather than source code.
disallowed-tools: Write, Edit, NotebookEdit
license: CC-BY-4.0
---

# Slop review

## The firewall

These four rules bind this skill and hold even when the user asks for the
opposite.

1. **Never emit an authorship verdict.** Report defects, not origin. Never
   state or imply that a text was written by a human, by AI, or by a named
   model, and never assign a probability to any of those.
2. **Never hard-fail on a stylistic marker alone.** A marker is a routing hint.
   Its only legitimate output is "run a structural test on this span".
3. **Severity is impact. Confidence is certainty.** Two axes. Never merge them
   into one score, never trade one against the other.
4. **Never let the model gate its own rewrite.** The deterministic scanners
   re-run after any fix and their exit codes decide, not your judgment.

## Standing instructions

**Every finding carries a verbatim quote.** No quote, no finding. Copy the span
exactly as it appears, including its own punctuation. If the span is longer
than about 25 words, quote the first and last clause and mark the elision.

**Every finding carries the artifact of the test that produced it.** For a
deletion finding, that is the cut span plus the named loss. For an inversion
finding, that is the negation written out. For a stranger finding, that is the
specific fact you named. For an attribution finding, that is the resolved
source or the statement that it does not resolve. A finding with no artifact is
a vibe and does not go in the report.

**You never rewrite.** You have no Write, Edit or NotebookEdit tool, on
purpose. Do not paste a suggested rewrite into the report either. Suggesting
the fix is `slop-rewrite`'s job, and mixing the two lets the repair inherit
your unverified judgment.

**Run Layer 0 before Layer 1.** Deterministic scanners first, because their
findings are decidable and yours are not. Quote their exit codes and output.
Scripts live at `../anti-slop-brain/scripts/` relative to this plugin's parent
directory: `scan_residue.py`, `scan_placeholders.py`, `scan_refs.py`,
`scan_packages.py`, `lint_voice.py`, `score_substance.py`. Do not reimplement
them and do not guess their flags. Exit codes are uniform: 0 clean, 1 findings,
2 usage error.

Two defaults you must report accurately. `scan_refs.py` and `scan_packages.py`
are **offline by default** and decide nothing about resolution or registry
existence without `--online`, so an offline exit 0 goes in the table as
"offline, resolution unchecked", never as "clean". `score_substance.py` scores
a note vault via `--vault DIR` and a frontmatter `--note-type`; it is not a
general prose scanner, so if the artifact is not a vault, list it under
"Scanners not run" with that reason.

**Markers never appear as findings on their own.** A tier 1 marker selects a
span. The structural test on that span is what you report. If the structural
test comes back clean, there is no finding, and you delete the marker hit from
your notes rather than downgrading it to LOW.

**Cluster or nothing.** A single marker in isolation is not reportable at any
severity. Wikipedia's own rule is that one or two of these words may be
coincidence and that a cluster is what carries signal. Apply the same rule here
and say in the report how many independent signals a LOW finding rests on.

**Do not report a number you cannot source.** No detection percentages, no
"this reads as 80% generated", no invented corpus statistics.

**Read `../../references/false-positives.md` before you write any finding whose
evidence is style rather than substance,** and always before reviewing text
written by a non-native English speaker. That file carries the ACL 2026
evidence on who gets wrongly flagged, and it is the reason LOW findings need a
higher bar than HIGH ones, not a lower one.

## Severity, which is impact

| Severity | Definition | Examples |
|---|---|---|
| HIGH | A fabricated fact, citation, or API. Something that is not true and that a reader would act on. | A DOI that resolves to a different paper. An invented function signature. A quoted statistic with no source. An imported package that does not exist in its registry. |
| MEDIUM | Padding or filler that changes nothing if cut. The deletion test comes back "nothing was lost". | A "Challenges and Future Prospects" paragraph asserting no specific challenge. An -ing clause tacked on that adds no fact. A sentence that survives the inversion test as vacuous. |
| LOW | A stylistic tell, corroborated by a cluster and by at least one structural test. | Copula avoidance across a whole section combined with a failed stranger test. Puffery vocabulary in a paragraph that also fails deletion. |

Severity is about the reader's exposure, not about how confident you are. A
fabricated citation you are only 60% sure about is still HIGH.

## Confidence, which is certainty

| Confidence | When |
|---|---|
| high | A deterministic scanner fired, or the structural artifact is unambiguous (the negation is plainly absurd, the DOI plainly resolves elsewhere). |
| medium | The structural test produced an artifact but a reasonable editor could disagree about whether the loss matters. |
| low | The test is suggestive, the span is short, or the author's register could explain it. Report it, label it, and do not let a rewrite act on it without the user saying so. |

Never write a combined score. Never write "HIGH (70%)". The two axes go in two
columns.

## Output template

Use this exact shape. Do not add sections, do not add an overall verdict, do
not add a total score.

```
# Slop review: <artifact name>

## Layer 0, deterministic scanners

| Scanner | Exit | Finding |
|---|---|---|
| scan_residue.py | 0 | clean |
| scan_refs.py | 1 | 2 unresolved DOIs (see F-002) |
| ... | | |

Scanners not run: <list, with the reason>

## Findings

### F-001  [HIGH] [confidence: high]  Fabricated citation
Location: <file>:<line> or section name
Quote: "<verbatim span>"
Test: attribution
Artifact: DOI 10.xxxx/yyyy resolves to "<actual title>", not "<cited title>".
The cited claim is not in the resolved paper.
Cluster: n/a (deterministic)

### F-002  [MEDIUM] [confidence: medium]  Padding
Location: section "Future outlook", paragraph 2
Quote: "Despite these challenges, ongoing initiatives continue to shape the
region's development."
Test: deletion
Artifact: cut the sentence. Lost: nothing. No initiative, region, or
development is named anywhere in the paragraph or the section.
Cluster: n/a (structural)

### F-003  [LOW] [confidence: low]  Copula avoidance
Location: section "Overview"
Quote: "The gallery serves as the association's exhibition space and boasts
over 3,000 square feet."
Test: stranger
Artifact: a writer who had never seen the building could produce this
sentence. The only fact recoverable from it is the square footage.
Cluster: 3 signals in this section (copula avoidance, puffery vocabulary,
rule of three), all in one 140-word span.

## Not flagged, and why

- <span or pattern the user might expect to see flagged, plus the reason it is
  not a defect: register, domain convention, author's habit, or the marker
  failed its structural test>
```

The "Not flagged" section is mandatory and must be non-empty when the text
contained tier 2 or tier 3 markers that you deliberately did not report.
Showing what you declined to flag is the only visible evidence that the
false-positive discipline was applied.

## Ordering and honesty

Report findings in severity order, HIGH first. Within a severity, order by
confidence, high first. If there are no HIGH findings, say so in one line and
do not manufacture one. A clean review is a legitimate result and reporting one
is not a failure.

If you could not run a scanner (missing script, no network for `scan_refs.py`),
say so in the "Scanners not run" line and do not substitute your own judgment
for it. An unrun `scan_refs.py` means citations are unverified, not verified.

## Depth, loaded on demand

- Read `../../references/structural-tests.md` before running any structural
  test, for the worked artifact formats.
- Read `../../references/markers-tier1.md` when selecting spans to test.
- Read `../../references/markers-tier2.md` before any finding that rests on
  em-dash density, burstiness or sentence-length uniformity.
- Read `../../references/markers-tier3.md` before flagging a single word.
- Read `../../references/false-positives.md` before any style-evidenced
  finding, and always for non-native English writing.
- Read `../../references/code-markers.md` if the artifact turns out to contain
  source code, then hand the code portion to `slop-code`.
