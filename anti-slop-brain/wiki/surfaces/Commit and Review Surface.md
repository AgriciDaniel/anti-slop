---
type: "surface"
title: "Commit and Review Surface"
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
  - "[[Signs Are Not The Problem|Signs of AI Writing]]"
  - "[[Code Surface]]"
  - "[[The Attribution Test]]"
  - "[[The Deletion Test]]"
  - "[[The Firewall]]"
  - "[[The Firewall|Severity and Confidence]]"
  - "[[Evidence Tiers]]"
  - "[[Evidence Quality Ladder|Vendor Evidence Conflicts]]"
  - "[[Agent Output Surface]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://arxiv.org/abs/2507.00788"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/"
---

# Commit and Review Surface

Wikipedia has spent four years building a taxonomy of what LLM-assisted edit
summaries look like, and nobody in the engineering tooling space appears to have
noticed that a git commit message is an edit summary. The transfer is the
original contribution of this note. A commit message, a pull request
description, and a code review comment are all short accompanying texts written
about a change by the person who made it, which is the exact genre WP:AISUMMARY
and WP:AICOMMENT describe.

## The transfer, sign by sign

`wikipedia-signs-of-ai-writing` characterises AI edit summaries as formal,
first-person paragraphs without abbreviations that conspicuously echo the exact
text of the project's policies, and that often mention things the editor
"ensured" or "avoided" doing. It names three sub-signs. Each maps onto
engineering without modification.

### Canned assurance of adherence

On Wikipedia the watch list is "ensured that it adheres to", "in compliance
with", "verifiability", "neutrality", "encyclopedic tone". The engineering
equivalents are "follows existing code conventions", "adheres to the project
style guide", "ensures backwards compatibility", "maintains test coverage", and
"follows best practices". The guide's own contrast is the useful part: a human
writes "removed excessive links per MOS:OVERLINK", and the AI equivalent is
"more verbose and yet less specific". The engineering version of that contrast
is "drop retry on 429, upstream now sends Retry-After" against "improved error
handling to ensure robust and reliable behaviour".

### Specific mentions of what was preserved

The guide's watch list is "preserved", "preserving", "retained", "retaining",
with the observation that it is unusual for a human edit summary to mention
material that was not edited. "While preserving existing functionality" is the
phrase this vault sees most often in generated pull request descriptions, and it
is worth naming precisely why it is a defect rather than a harmless flourish.
The sentence asserts an invariant that the author did not verify. It reads as
evidence of a check that never happened, and a reviewer who trusts it reviews
less carefully than one who does not. That makes it a correctness claim wearing
a summary's clothes, and it routes to [[The Attribution Test]]: name the test
run, the manual verification performed, or delete the clause.

### Overemphasis on what was addressed

Wikipedia watches "added sourced information", "added citations", "improved
attribution", and the AfC form "Addressed reviewer feedback by improving
sourcing, formatting, and neutrality". The pull request form is "Addressed all
review comments", "Addressed feedback and improved error handling", "All tests
pass". These are checkable and therefore cheap to convict. Resolve "addressed
all review comments" against the thread: every comment either has a
corresponding change, a reply explaining why not, or the claim is false.

## Restating the diff instead of explaining the why

This is the dominant defect on the surface and it is not on Wikipedia's list,
because Wikipedia edits do not carry a machine-readable diff. Git does. A commit
message that says "updated UserService.java to add null check in getProfile"
tells the reader what `git show` already tells them, and costs the one thing the
diff cannot supply: why the null arrived, why a check is the right response
rather than a fix upstream, and what happens the next time it arrives.

The procedure is [[The Deletion Test]] with a specific loss condition. Delete
the message. Regenerate a mechanical summary from the diff. If the two carry the
same information, the message contributed nothing. A commit message earns its
place by containing at least one fact that is not recoverable from the diff:
the triggering incident, the rejected alternative, the constraint, the ticket,
the measurement.

## Review comment defects

`wikipedia-signs-of-ai-writing` also documents comment-specific indicators in
its WP:AICOMMENT section, and those transfer to code review with equal force.
Editors using LLMs for comments tend to misquote policy and cite made-up
shortcuts, post long comments divided into titled sections, assure others that
their content adheres to policy, ask what exactly should be improved, and accuse
those who question them of acting on speculation about writing style.

In review, the same shapes appear as: citing a style rule the project does not
have; a review comment with four bolded headings on a twelve-line diff; asking
the author to clarify rather than reading the surrounding file; and blanket
approval with a summary of what the change does. That last one is the one to
watch, because a review that summarises the diff and approves is
indistinguishable in the record from a review that examined it.

## Signal table

| Signal | Where it appears | Tier | Procedure | False positive specific to this surface |
| --- | --- | --- | --- | --- |
| Canned policy assurance | commit, PR body | 1 | [[The Attribution Test]] | teams with a mandated PR template that asks for exactly this |
| "while preserving existing functionality" | PR body | 1 | [[The Attribution Test]] | a genuine compatibility guarantee backed by a named contract test |
| Overemphasis on what was addressed | PR body, review reply | 1 | resolve against the thread | a real changelog of responses to review |
| Diff restatement | commit subject and body | 1 | [[The Deletion Test]] | conventional-commit subjects, which are supposed to be mechanical |
| Titled sections in a short review comment | review | 2 | [[The Deletion Test]] | design review of a large change, where structure earns its place |
| Emoji section markers | commit, PR body | 3 | none, routes only | project conventions such as gitmoji |
| First-person formal paragraph | commit body | 2 | none, routes only | maintainers who have always written this way |
| Approval with no located concern | review | 1 | none; process signal | a genuinely small and obviously correct change |
| Fabricated ticket or rule reference | any | Layer 0 | scanner | renamed tracker projects and moved anchors |

Note the tier-3 rows. They route attention and may not be reported as findings,
because both have obvious innocent causes and neither carries harm on its own.
This is [[Evidence Tiers]] applied without exception.

## What the merge-rate evidence does and does not show

A peer-reviewed MSR 2026 study by Chowdhury and colleagues reports that pull
requests handled only by code-review agents merge at 45.20 percent against 68.37
percent for human-only review, with 60.2 percent of closed agent-only pull
requests falling in the 0 to 30 percent signal range. **Recorded honestly: this
finding lives in `.research/verification-ledger.md` and does not yet have an
entry in `references/source-ledger.json`, so under this vault's own citation
rules it is not yet citable and the figure must not be repeated in a deliverable
until the ledger entry exists.** It is stated here because leaving it out would
be worse than flagging it.

Even once entered, the figure supports a narrower claim than it appears to. A
lower merge rate is a merge-rate difference. It is consistent with agent review
missing real problems, and equally consistent with agent review surfacing
changes that were never going to merge, and with reviewer behaviour changing
when the reviewer is known to be an agent. It is not a quality measurement.

The counterweights are recorded for the same reason they are recorded in
[[Code Surface]]. `borg-null-result`, a preprint pre-registered with In-Principle
Acceptance across 151 participants, found no significant differences in
subsequent code evolution, completion time, or quality in its pre-registered
Phase 2, while its observational Phase 1 found a 30.7 percent median reduction in
completion time. `gitclear-maintainability-gap` reports
block duplication rising 81 percent from 2023 to 2026 year to date across 623
million changes, and is vendor-produced and correlational.
`stenberg-high-quality-chaos` reports a maintainer concluding in April 2026 that
the situation is no longer a problem, with confirmed-vulnerability rates back to
15 to 16 percent. The honest summary is that the process evidence is mixed and
that none of it licenses a statement about who or what wrote a given commit. See
[[The Firewall]].

## Repair guidance

1. Keep the subject line mechanical. Conventional-commit subjects are supposed
   to restate the change; the why belongs in the body.
2. Delete every clause asserting an unverified invariant, or attach the check
   that supports it.
3. Replace policy echoes with the specific rule and the specific line.
4. In review, state the located concern with a file and line, or approve without
   a summary. A summary is not a review.

## Related

- [[Code Surface]]
- [[Documentation Surface]]
- [[Agent Output Surface]]
- [[Dependency Surface]]
- [[Marker Cohort Rot]]
- [[Workslop|Workslop Downstream Cost]]
- [[Note Conventions]]
- [[index|Index]]
