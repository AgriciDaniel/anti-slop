---
type: "concept"
title: "The Moral Panic Objection"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/concept"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[AI Slop]]"
  - "[[Workslop]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Evidence Quality Ladder]]"
  - "[[The Accessibility Objection]]"
  - "[[Why Structural Not Judgmental]]"
  - "[[Superseded Figures]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://simonwillison.net/2024/May/8/slop/"
  - "https://www.merriam-webster.com/wordplay/word-of-the-year"
  - "https://arxiv.org/abs/2605.19936"
  - "https://arxiv.org/abs/2509.19163"
  - "https://www.betterup.com/workslop"
  - "https://arxiv.org/abs/2507.00788"
---

# The Moral Panic Objection

Cheap print, dime novels, radio serials, television, comics, video games and
social feeds each arrived with a literature explaining that culture was about to
drown in mass-produced filler. Some of that writing was perceptive. Most of it
now reads as an aesthetic complaint about unfamiliar form, dressed as a warning
about civilisational decline. The objection in this note says the slop
discourse is the newest entry in that sequence, and that this vault is a
participant rather than an observer.

## The argument, put by someone who means it

It has four parts, and they are stronger separately than the summary suggests.

**One, the pattern.** Every prior mass medium produced a wave of critics who
identified a novel formal quality, treated it as evidence of degradation, and
were later shown to have been describing novelty. The prior is therefore
against the current wave, not neutral toward it.

**Two, the base-rate error.** "AI produces mostly mediocre output" is a claim
with no content until it is set against how much human output is mediocre. If
the vast bulk of writing in any medium is unremarkable, then observing that
machine writing is mostly unremarkable identifies nothing about machines. The
correct comparison is a difference, and the discourse almost never computes one.

**Three, the aesthetic tell.** The markers that get catalogued are disliked
before they are measured. Punctuation habits, triadic rhythm, particular
adjectives. A list assembled by noticing what irritates readers is a taste
document, and giving it a tier does not convert taste into evidence.

**Four, the cost.** Panics are not free. They license bad policy and bad
accusations, and the accusations land unevenly. This part of the objection is
not speculative and is worked through in [[The ESL Objection]].

None of that is a straw position. Parts two and four are, in this brain's
assessment, correct.

## The part of this that is reasoning rather than evidence

No source in this brain's ledger establishes the historical-panic parallel
empirically. There is no entry measuring the accuracy of past media criticism,
no entry comparing the trajectory of the slop discourse to any earlier one, and
no entry testing whether present concern is proportionate by any historical
standard. Part one of the objection above is therefore argument by analogy, and
it is labelled as such here rather than presented as a finding.

That cuts both ways, and this note says so plainly rather than treating the
asymmetry as a win. A brain that dismissed the parallel would also be reasoning
without evidence. What follows is that neither side gets to invoke history as
proof, and the dispute has to be settled on claims that were actually measured.
The rule that produced this paragraph is in [[Evidence Quality Ladder]]:
unsourced reasoning is kept and labelled, never promoted by repetition.

## The base-rate half, taken on its own terms

Part two deserves better than a dismissal, because the ledger partly supports
it.

`miletic-lexical-diversity` found that expert readers rated LLM-modified
academic text as more understandable and more exciting than the unmodified
text, while the same text measured lower on lexical diversity. If machine
involvement reliably produced worse reading, that result should not exist. It
does exist, in a study spanning more than 37,000 ACL Anthology papers, and it
is the single strongest piece of ledger evidence for the objection. The full
treatment is in [[The Accessibility Objection]].

`borg-null-result` is the second. Pre-registered with In-Principle Acceptance
before data collection, 151 participants, and a preprint rather than a published
paper: arXiv 2507.00788, In-Principle Acceptance granted at ICSME, no journal
reference. Its pre-registered Phase 2 found no significant differences in
subsequent code evolution, completion time or quality between AI-assisted and
unassisted development. It is the most carefully designed single item in the AI
code quality literature and that phase is a null result. The objection does not
get the whole study, though: Phase 1 was observational and found a 30.7 percent
median reduction in completion time with an AI assistant. Anyone arguing that
the panic is outrunning the evidence should cite both phases, and this brain
cites the source against itself in [[The Code Slop Disagreement]].

One figure is regularly misused in the other direction and should not be. In
`shaib-measuring-slop`, human annotators flagged spans at a rate of 0.34 while
LLM judges flagged at 0.03 to 0.08, with agreement near zero at kappa 0.01 for
GPT-5, minus 0.01 for DeepSeek-V3 and 0.03 for o3-mini. The 0.34 is a rate over
that labelled corpus. It is not a measurement of how much human writing is
mediocre, and quoting it as a human base rate would be exactly the error part
two of the objection is complaining about.

## Where the objection stops reaching

The objection is aimed at an aesthetic claim. This brain does not make one. The
definition it operates on, from `willison-slop`, locates the defect in content
that is mindlessly generated and imposed on someone who did not ask for it. That
is a claim about effort on one side and consent on the other. Both are facts
about a transaction, not judgements about a text.

| What the objection attacks | Does the behavioural definition depend on it |
| --- | --- |
| "This writing is ugly" | no, the definition never grades prose |
| "Machine writing is worse than human writing" | no, and `miletic-lexical-diversity` argues against it |
| "Most machine output is mediocre" | no, base rates are irrelevant to an imposition claim |
| "You can tell by reading" | no, and this brain forbids the verdict entirely |
| "The markers are taste, not evidence" | partly, which is why markers may route but never decide |
| "There is a measurable downstream cost" | yes, and this is the only leg that must hold |

Read the last row against the rest. Four of the six attacks land on positions
this vault does not hold. The fifth is conceded and absorbed by tiering, per
[[Evidence Tiers]]. Only the sixth is load-bearing, and only the sixth needs
defending with numbers.

Note also what the lexicographic definition costs the objection. `merriam-webster-woty-2025`
defines slop as digital content of low quality produced usually in quantity by
means of artificial intelligence, and the American Dialect Society independently
selected the same word. That definition does bundle a quality judgement, and it
is the definition most of the discourse uses. The objection is a fair hit on
that reading. It is not a hit on the behavioural one, which is why this brain
uses the behavioural one.

## The empirical leg, with its weakness stated

`betterup-workslop` is the only ledger source that measures receiver-side cost
directly: 40 percent of United States desk workers reported receiving workslop
in the prior month, roughly 15 percent of received content qualified, each
incident took about two hours to resolve, and the estimated cost is 186 dollars
per employee per month, around 9 million dollars a year at 10,000 employees.
The study is n equal to 1,150 desk workers, fielded September 2025 with the
Stanford Social Media Lab.

Its weakness is real. Self-reported survey estimates are not controlled
measurement, respondents classify the content themselves, the vendor publishing
it sells services in the adjacent space, and the Harvard Business Review article
body is paywalled so the figures were confirmed on BetterUp's own page. This
brain treats it as practitioner evidence, not as a measured cost, and
[[Workslop]] carries the caveats in full. If the objection wants to attack the
one leg that matters, this is where to aim.

## What would show this brain is on the wrong side

1. A controlled study finding that readers are not measurably worse off after
   receiving unreviewed generated content, replacing `betterup-workslop` with a
   better-designed null.
2. A demonstration that citation defects, fabricated references and
   non-existent dependencies occur at similar rates in unassisted work, which
   would move those from AI-specific defects to ordinary ones.
3. Evidence that the structural procedures in this vault flag human-authored
   careful writing at a rate close to their flag rate on generated writing,
   which would show they measure style after all.
4. Replication of `borg-null-result` at larger scale across prose as well as
   code, which would make the null the default rather than the counterweight.
5. Any measurement showing that the specific defects catalogued here are
   declining without intervention, which would make the tooling redundant.

Items 1 through 5 are stated so that a reader can hold this vault to them. None
of them is currently satisfied, and item 4 is partly satisfied for code, which
is why the code claims here are hedged and the prose claims are not.

## Related

- [[AI Slop]]
- [[Workslop]]
- [[The Code Slop Disagreement]]
- [[Evidence Quality Ladder]]
- [[The Accessibility Objection]]
- [[The ESL Objection]]
- [[Why Structural Not Judgmental]]
- [[Evidence Tiers]]
- [[Superseded Figures]]
- [[What This Brain Does Not Claim]]
