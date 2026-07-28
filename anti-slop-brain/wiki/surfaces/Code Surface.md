---
type: "surface"
title: "Code Surface"
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
  - "[[The Load Bearing Test|The Load-Bearing Test]]"
  - "[[Dependency Surface]]"
  - "[[Commit and Review Surface]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall|Severity and Confidence]]"
  - "[[The Firewall]]"
  - "[[Package Hallucination Evidence|Package Hallucination and Slopsquatting]]"
  - "[[Evidence Quality Ladder|Vendor Evidence Conflicts]]"
  - "[[The Generation Verification Asymmetry|Generation-Verification Asymmetry]]"
  - "[[Prose Surface]]"
source_urls:
  - "https://arxiv.org/abs/2507.09089"
  - "https://arxiv.org/abs/2507.00788"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://gitclear-public.s3.us-west-2.amazonaws.com/GitClear-AI-Copilot-Code-Quality-2025.pdf"
  - "https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/"
  - "https://arxiv.org/abs/2606.28438"
---

# Code Surface

Every packaged anti-slop tool this vault reviewed has near-zero coverage of
code. `blader-humanizer` addresses code artifacts in exactly one of its 33
patterns, and its only protection in file mode is a single sentence telling the
model to leave code blocks untouched, with no mechanism behind it. That gap is
the reason this note exists, and it is also the reason this note has to open
with a disagreement rather than a defect list.

## The evidence does not agree, and this note will not pick a side

The literature on AI-assisted code quality splits cleanly along a line that
should make anyone uncomfortable: the strongest slop figures come from vendors
selling engineering-intelligence products, and the strongest null results come
from academia. Both halves are recorded here at full strength.

**What the vendor telemetry measured.** `gitclear-copilot-quality-2025` analysed
211 million changed lines from 2020 to 2024 and reports moved or refactored code
falling from 24.8 percent in 2021 to 9.5 percent in 2024, copy-pasted code
rising from 8.3 percent to 12.3 percent over the same period, and an eight-fold
increase during 2024 in code blocks containing five or more duplicated lines.
`gitclear-maintainability-gap` extends the series across 623 million changes and
reports block duplication climbing from 40.3 per million changed lines in 2023
to 73.0 in 2026 year to date, a rise of 81 percent. Both are correlational, both
are vendor-produced, and GitClear sells code-quality tooling, so the finding
serves its commercial interest. The often-quoted 7.1 percent churn figure from
this series was a discarded 2024 projection and was never a measurement; the
2024 actual was 5.7 percent. See [[Superseded Figures]].

**What the randomised trial measured.** `metr-developer-slowdown` ran a
randomised controlled trial with 16 experienced developers across 246 real tasks
on mature repositories and found that allowing AI increased task completion time
by 19 percent. The perception gap in the same study is the more interesting
result: developers forecast a 24 percent speedup and still estimated a 20
percent speedup after the fact, while economists forecast 39 percent and machine
learning experts 38 percent. Small n, and METR's own 2026-02-24 follow-up could
not obtain a clean signal because developers increasingly refused to work
without AI.

**What the pre-registered study measured.** `borg-null-result` is the
methodologically strongest single item in this literature and it is a null
result. With 151 participants and pre-registered with In-Principle Acceptance
before data collection, its Phase 2 found no significant differences in
subsequent code evolution, completion time, or quality between AI-assisted and
unassisted development. It is a preprint, arXiv 2507.00788, not a published
paper: the In-Principle Acceptance was granted at ICSME and there is no journal
reference. Phase 1 of the same study was observational and found the opposite
direction, a 30.7 percent median reduction in completion time with an AI
assistant, so quoting the null on its own misreports it. Cite it whenever the
vendor figures are cited. This vault's rule is that the two are quoted together
or not at all; [[Evidence Quality Ladder|Vendor Evidence Conflicts]] holds the
general policy.

Nothing above is resolved. What survives the disagreement is narrow and
sufficient: duplication is measurably rising in at least one large telemetry
corpus, self-assessment of AI-assisted speed is measurably unreliable, and
controlled evidence for a quality difference is absent. That is enough to
justify mechanical review and not enough to justify a moratorium.

## Defect catalogue

Every row is convicted or acquitted by [[The Load Bearing Test|The Load-Bearing Test]]: delete the
construct, then state what broke or became unclear. If nothing did, the construct
was ceremony. The final column is the legitimate case that stops the row from
being a blanket rule.

| Defect | How it presents | Load-bearing check | Legitimate case that acquits |
| --- | --- | --- | --- |
| Redundant comment | `# increment i` above `i += 1` | delete it; does meaning change | comment records a non-obvious reason or a bug reference |
| Ceremonial docstring | full parameter table on a two-line private helper | delete it; can a caller still use the function | published API where the docstring is the contract |
| Step-narration comments | `# Step 1:`, `# Step 2:` down a function body | delete them; is control flow still readable | teaching material and worked examples |
| Passthrough wrapper | function whose body is one call with identical arguments | inline it; does any caller break | seam held deliberately for a planned substitution or test double |
| Over-abstraction | interface with exactly one implementation and no second planned | collapse it; does anything fail to compile | plugin boundary with an external implementer |
| Error-swallowing try/except | broad catch that logs and continues | remove the handler; what actually propagates | a documented boundary that must not crash, with the swallow logged and justified |
| Generic naming | `data`, `result`, `handler`, `process` in domain code | rename to the domain term; does the name now say more | genuinely generic infrastructure, where `handler` is the domain term |
| Assertion-free test | test that calls the code and asserts nothing | invert the implementation; does the test still pass | smoke test explicitly documented as crash-only |
| Coverage padding | tests that exercise getters and constructors only | delete the file; does the coverage-weighted risk change | none that this vault has found; treat as a real defect |
| Hallucinated API | call to a method that does not exist on that type | run it, or resolve the symbol | none; this is a hard failure, not a marker |
| Hallucinated import | import of a package that is not in any registry | run `scan_packages.py` | none; see [[Dependency Surface]] |

The last two rows behave differently from everything above them. They are
decidable, so they are Layer 0 scanner work and are allowed to hard-fail. The
rest are Layer 1 and require an artifact before an edit, exactly as
[[Evidence Tiers]] specifies for every other surface.

## Why the load-bearing test is the right instrument here

Code has a property prose does not: the compiler, the type checker, and the test
suite are ground truth that costs seconds to consult. That collapses the
[[The Generation Verification Asymmetry|Generation-Verification Asymmetry]] on this surface more than on any other.
A comment that claims the function is thread-safe is checkable. A docstring that
lists a parameter the signature does not have is checkable. Wherever a check is
mechanical, this vault runs it rather than reasoning about it.

That is also why model self-review is barred from gating.
`song-rubber-stamp-regime` reports that AI self-review gates enter a
rubber-stamp regime in which acceptance scores rise while benchmark correctness
falls. It is a preprint verified at abstract level only, so it is tier
CONTESTED, but it points the same direction as the firewall rule that already
existed: deterministic scanners re-run after every repair, and the model never
signs off on its own diff. See [[The Firewall]].

## What is not a code defect

- **Verbosity that the language requires.** Go error handling and Java
  boilerplate are not padding.
- **Comments explaining why.** The defect is restating what the line does. A
  comment naming the constraint, the ticket, or the vendor bug is the most
  valuable line in the file.
- **Defensive programming at a real boundary.** Input validation on a public
  endpoint is not ceremony. The defect is a broad catch in the middle of a call
  stack that turns a failure into a wrong answer.
- **Duplication under three occurrences.** The rule of three predates language
  models by decades and a second copy is often correct.
- **Generated code.** Protobuf stubs, ORM models, and migration scaffolds are
  supposed to look like each other.
- **Code that merely looks machine-written.** No row in this note supports an
  authorship claim, and none may be reported as one.

## The maintainer view, updated

The narrative that AI-assisted contributions broke open-source security triage
is out of date and this vault records the correction. `stenberg-high-quality-chaos`,
a first-hand account from the curl maintainer dated 2026-04-22, states that the
slop situation is not a problem anymore: report frequency runs at about double
the rate seen through 2025, the confirmed-vulnerability rate returned to 15 to
16 percent, and curl returned to HackerOne on 2026-03-01 without a bounty. It is
a maintainer account rather than a controlled study, but it directly contradicts
the common claim that curl abandoned bug bounties permanently. The lesson it
supports is Triage Over Bans: raise the cost of submitting an unverified
artifact, do not ban a tool.

## Related

- [[Dependency Surface]]
- [[Commit and Review Surface]]
- [[Agent Output Surface]]
- [[The Load Bearing Test|The Load-Bearing Test]]
- [[Workslop|Workslop Downstream Cost]]
- [[Marker Cohort Rot]]
- [[Note Conventions]]
- [[overview|Overview]]
