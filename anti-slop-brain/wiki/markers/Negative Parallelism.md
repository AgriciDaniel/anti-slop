---
type: "marker"
title: "Negative Parallelism"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/marker"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Evidence Tiers]]"
  - "[[The Inversion Test|Inversion Test]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[Model Fingerprints|Model Specific Fingerprints]]"
  - "[[Puffery and Undue Emphasis]]"
  - "[[Tricolon and Rule of Three]]"
  - "[[Marker Cohort Rot]]"
  - "[[Prose Surface]]"
  - "[[Agent Output Surface|Chat Transcripts]]"
  - "[[Distributional Convergence]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://arxiv.org/abs/2502.12150"
---

# Negative Parallelism

Two sentences arrive in the shape of a correction. "It is not just a song, it
is a statement." "This is not a tool, it is a mirror." The construction sets up
a contrast, and the reader's attention obediently follows it, until the reader
notices that the thing being corrected was never asserted by anyone. Nobody
claimed it was just a song. The correction is theatre, and the sentence
delivers a mood where it appeared to deliver a distinction.

`wikipedia-signs-of-ai-writing` catalogues this under the shortcut AIPARALLEL
and it earns Tier 1 in [[Evidence Tiers]] on the same basis as
[[Puffery and Undue Emphasis]]: long, adversarial, high-volume observation by
editors removing it from live articles, with an independently documented
per-model variant described below.

## Three forms, and the one that gets missed

| Form | Shape | Example |
| --- | --- | --- |
| Additive | not only X, but also Y | Not only did the album chart, but it also reshaped the genre. |
| Corrective | not X, it is Y | It is not a career, not a body of work, not sustained relevance, just an algorithmic moment. |
| Reversed | X rather than Y | prioritising empirical consolidation of power amid fragmented loyalties rather than ideological purity |

The corrective example above appears in the source with the U+2014 character
before the final clause; this vault renders it with a comma under the house
style described in [[The Em Dash]]. The substitution changes nothing about the
construction.

Prior art collapses the first two forms into one item and omits the third
entirely. The third matters most, because it is the one currently in growth.

## The reversed form, and why it is called Grok-characteristic

`wikipedia-signs-of-ai-writing` records "X rather than Y" as a construction
particularly common in Grok output, alongside that model's overuse of
superficially scientific vocabulary such as causal, empirical and correlate,
and its continued overuse of underscore as of 2026. The reversed form is harder
to see because it looks like ordinary comparative reasoning. It fails the same
way: Y is a position nobody held, so the sentence has ranked a real thing above
an imaginary rival and called that an analysis.

Per-model attribution of this kind is measurable. `sun-idiosyncrasies` reached
97.1 percent accuracy on five-way model attribution across ChatGPT, Claude,
Grok, Gemini and DeepSeek, with the signal surviving rewriting, translation and
summarization. That result supports the existence of stable per-model
idiolects, which is what makes a claim like "this form is characteristic of one
vendor's model" a coherent claim at all. It does not license reading a vendor
name off a paragraph, and this note does not do that. See
[[Model Fingerprints|Model Specific Fingerprints]] and [[The Firewall]].

## The distributed form

The construction also spreads across sentence boundaries, which defeats any
regex written for a single line:

> The report is thorough. Thoroughness alone was never the point. What the
> committee needed was a decision.

Same move, three sentences, no "not only" anywhere. Detection here is a reading
task rather than a scanning task, which is one reason this marker routes to a
procedure instead of a linter.

## Tailing negations

A clipped fragment tacked onto a finished sentence: "The options come from the
selected item, no guessing." "One command, no configuration." Prior art in
`blader-humanizer` groups this with negative parallelism, and the grouping is
sound: the fragment names an absent problem in order to imply a benefit. The
repair is to write the benefit as a clause, or to cut it if the benefit cannot
be stated positively without sounding empty. If it does sound empty when stated
positively, it was empty.

## False positive class: who this marker wrongly flags

1. **Anyone correcting an actual misconception.** If the audience genuinely
   believes X, "not X, but Y" is the correct rhetorical move and has been for
   two thousand years. The test is whether the misconception is real and
   present, not whether the construction appears.
2. **Contrastive academic prose.** "The effect is driven by selection rather
   than by treatment" is a precise, load-bearing sentence in exactly the
   reversed form.
3. **Legal and specification writing.** "The licence grants use rather than
   ownership" carries the entire meaning of the clause.
4. **Advertising, speeches, and manifestos.** The construction is a staple of
   persuasive human writing and predates the technology by centuries.
5. **Translated prose.** Several languages prefer contrastive framing where
   English would use a plain assertion.
6. **Anyone quoting the construction.** Secondhand text, titles, and examples
   under discussion are not instances.

## Repair procedure

1. Locate the negated term Y. Write it down as a standalone assertion.
2. Ask whether any identified person or source actually holds Y. Not "could
   someone", but "does the document, its audience, or a cited source assert
   it". This is a light form of [[The Inversion Test|Inversion Test]].
3. If Y is held by someone real, keep the construction and, where the surface
   allows it, name who holds it. The sentence becomes stronger, not weaker.
4. If Y is held by nobody, delete the negated half and keep the assertion.
   "It is not just a song, it is a statement" becomes whatever the statement
   actually is, stated once.
5. If deleting the negated half leaves a sentence that says nothing, the
   sentence was carrying the contrast rather than a claim. Run
   [[The Deletion Test|Deletion Test]] on the whole sentence and record what was lost.
6. Count instances per 1,000 words and record the count. Do not convert it into
   a score, and do not fail a document on it. Under [[Evidence Tiers]] no tier
   licenses a hard failure on its own.

## Interaction with other markers

This construction co-occurs with [[Tricolon and Rule of Three]] often enough
that the corrective form frequently arrives as a triple: not A, not B, not C,
just D. When both fire on the same sentence, treat it as one finding with two
names rather than two findings, or the density counts double-charge the same
span.

## Related

- [[Evidence Tiers]]
- [[Tricolon and Rule of Three]]
- [[Puffery and Undue Emphasis]]
- [[The Inversion Test|Inversion Test]]
- [[The Deletion Test|Deletion Test]]
- [[Model Fingerprints|Model Specific Fingerprints]]
- [[The Em Dash]]
- [[The Firewall]]
- [[Marker Cohort Rot]]
- [[Prose Surface]]
