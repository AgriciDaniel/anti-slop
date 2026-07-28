---
type: "surface"
title: "Documentation Surface"
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
  - "[[Prose Surface]]"
  - "[[Code Surface]]"
  - "[[Commit and Review Surface|Diff-Anchored Writing]]"
  - "[[The Deletion Test]]"
  - "[[The Stranger Test]]"
  - "[[Evidence Tiers]]"
  - "[[Workslop|Workslop Downstream Cost]]"
  - "[[The Firewall]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://www.betterup.com/workslop"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
---

# Documentation Surface

Half of what a general-purpose slop checker flags in a README, an API reference,
or a changelog is a correct convention of the genre. Running an untuned prose
checker over technical documentation produces a findings report that is itself a
form of slop: high volume, confident, and mostly wrong. This note exists mainly
to draw the line between the two.

## Three genres in one folder

`docs/` is not one surface. It is at least three, with incompatible correct
answers, and a check that cannot tell them apart will fight the genre.

| Genre | What it is for | Convention that looks like a defect | Marker that misfires |
| --- | --- | --- | --- |
| README and guide prose | persuade and orient a reader who has not decided yet | benefits framing, a quick-start ordering | puffery, generic positive conclusion |
| API reference | let a reader who already decided look up one symbol | rigid per-symbol template, repeated phrasing | template convergence, elegant variation absent |
| Changelog and release notes | say what changed between two versions | narrating the diff, version-scoped framing | [[Commit and Review Surface|Diff-Anchored Writing]] |
| Migration guide | move a reader from version A to version B | before-and-after pairs, imperative steps | uniform sentence length, inline-header lists |
| ADR and design doc | record a decision and the alternatives rejected | passive constructions, hedged tradeoffs | passive voice, hedging density |

The prior-art skill `blader-humanizer` gets exactly one of these right. Its
pattern 30 explicitly carves out changelogs, release notes, and migration guides
from the diff-anchored-writing rule. Its patterns on copula avoidance, passive
voice, inline-header lists, title case, hyphenation, and fragmented headers carve
out nothing, and each of them will fire on correct documentation. That is the
gap this note fills.

## Patterns that are conventions here, not defects

**Changelogs are legitimately diff-anchored.** A changelog entry exists to
describe a change relative to a previous release. "This function was added to
replace the previous approach" is a defect in a reference page and the entire
job of a changelog line. The rule that generalises is the one
`blader-humanizer` states and then under-applies: a document should read
coherently without knowing what changed in the last commit **unless the document
is inherently version-scoped**. Check the genre before applying the pattern.

**API reference is legitimately formulaic.** Every entry having the same
skeleton is the feature. A reader scanning for the raises clause needs it in the
same position on every page. Elegant variation, which is a marker on the
[[Prose Surface]], is an active defect in reference material because two
different words for one concept mean two concepts to a reader using search.
Template convergence is measured and penalised in [[Knowledge Base Surface]];
it is not penalised here.

**Passive voice is correct where the agent is genuinely irrelevant.** "The
connection is closed after the timeout expires" names the thing a reader must
know. Rewriting it to name an actor invents a subject the documentation may not
want to commit to. Wikipedia's own guide, captured as
`wikipedia-signs-of-ai-writing`, lists formal and academic prose in its
ineffective-indicators section for the same reason. Passive voice earns a flag
only when it hides an actor the reader needs, which is a different and much
narrower test.

**Title case in headings is a house choice.** The blanket ban in prior art is a
Wikipedia manual-of-style preference presented as a universal rule. AP style,
Chicago headline style, and most vendor documentation use title case
deliberately. This vault treats heading case as a `lint_voice.py` house-style
check with a configurable setting, never as a slop signal, and says so in the
output so nobody mistakes a style setting for a finding. The distinction is a
direct application of [[The Firewall]] rule that a stylistic marker proves
nothing on its own.

**Repetition across pages of the same boilerplate.** Installation prerequisites
repeated on every guide page reduce reader friction. Deduplicating them into a
single page that every guide links to is a documentation-architecture decision,
not a slop repair.

## Defects that are real here

**Section inflation.** Headings added because a template said so, with one or
two sentences under each that restate the heading. The check is
[[The Deletion Test]] applied to the heading rather than the paragraph: remove
the section and name what a reader can no longer find. If the answer is nothing,
the section was scaffolding. This is the documentation form of the formulaic
"Challenges and Future Prospects" pattern that `wikipedia-signs-of-ai-writing`
documents, and the caveat that guide attaches transfers exactly: the sign is
about the rigid formula, not about mentioning challenges.

**Unsupported superlatives.** "Blazing fast", "production-ready",
"enterprise-grade", "seamless", and "robust" applied to a component with no
benchmark, no SLO, and no test behind them. The repair is not to soften the
adjective. It is to replace it with the number, or to delete it.
`kobak-excess-vocabulary` is the corpus grounding for treating this class as a
real shift rather than a taste preference: the excess vocabulary measured across
over 15 million PubMed abstracts was overwhelmingly stylistic verbs and
adjectives, which is precisely this word class.

**Instructions that were never executed.** A quick-start whose commands nobody
ran, an example whose imports do not resolve, an option that does not exist in
the flag parser. This is the highest-severity defect on this surface because the
cost lands on a reader following the steps in good faith. It routes to the
scanner work described in [[Dependency Surface]] and to a documentation test run
where one exists.

**Fabricated cross-references.** Links to sections, anchors, and pages that do
not exist. Cheap to check, so it is checked mechanically rather than reasoned
about. See [[The Attribution Test|Fabricated Citations]] for the same defect class in prose.

**Documentation that describes the intended system.** A README describing
behaviour the code does not have. [[The Stranger Test]] catches most of it: name
the specific fact that only someone who ran the thing would know, and if the
page contains none, nobody ran the thing.

## Routing table for documentation

| Marker | Tier | Procedure | Acquitting genre |
| --- | --- | --- | --- |
| Section Inflation | 2 | [[The Deletion Test]] on the heading | mandated compliance document structure |
| Unsupported superlative | 1 | [[The Inversion Test]] | marketing landing copy, which is a different artifact |
| [[Commit and Review Surface|Diff-Anchored Writing]] | 1 | genre check first | changelog, release notes, migration guide |
| Passive voice | 3 | none, routes only | reference prose where the actor is irrelevant |
| Title case heading | 3 | house style check only | any project whose style guide chooses it |
| Inline-Header Vertical Lists | 2 | [[The Deletion Test]] | option tables and parameter lists |
| Template convergence across pages | 2 | none on this surface | API reference, where it is required |
| Broken anchor or link | Layer 0 | scanner | none |
| Unrunnable example | Layer 0 | doc test | none |
| [[Vendor Residue Markers|Knowledge-Cutoff Disclaimers]] | 1 | [[The Deletion Test]] | none in documentation |

## The cost that justifies the work

`betterup-workslop` surveyed 1,150 United States desk workers with Stanford
Social Media Lab and reports that 40 percent received workslop in the prior
month, that roughly 15 percent of received content qualified, that each incident
took about two hours to resolve, and that the estimated cost is 186 dollars per
employee per month, or about 9 million dollars a year at 10,000 employees. These
are self-reported survey estimates rather than controlled measurement, and the
figure is quoted here as an order of magnitude for downstream cost, not as a
precise loss. Documentation is where that cost concentrates, because a document
is read many more times than it is written and every reader pays the resolution
time again.

## Related

- [[Prose Surface]]
- [[Code Surface]]
- [[Commit and Review Surface]]
- [[Knowledge Base Surface]]
- [[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]
- [[Marker Cohort Rot]]
- [[Note Conventions]]
- [[overview|Overview]]
