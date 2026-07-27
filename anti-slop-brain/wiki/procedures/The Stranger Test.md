---
type: "procedure"
title: "The Stranger Test"
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
  - "[[The Inversion Test]]"
  - "[[The Attribution Test]]"
  - "[[Why Structural Not Judgmental]]"
  - "[[Distributional Convergence]]"
  - "[[Signs Are Not The Problem]]"
  - "[[Excess Vocabulary]]"
  - "[[Prose Surface]]"
  - "[[Commit and Review Surface]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2509.19163"
---

# The Stranger Test

Swap the author. Leave the sentence exactly where it is, and put behind it a
competent writer who has the topic, the genre and the vocabulary but has never
opened the source material: never ran the migration, never sat in the meeting,
never read the paper being summarised, never saw the incident. If that
substituted author could have produced the sentence anyway, then the sentence
carries the genre and not the work, and the author who did the work has left no
trace in it.

Everything below is that one substitution, done carefully enough to produce
something a second person can check.

## The substitution, stated precisely

The stranger is not a fool and not a layperson. Weakening the stranger is the
usual way this test is broken, because a sufficiently ignorant stranger cannot
write anything and the test acquits everything. Hold the stranger at this exact
level:

- knows the field at a professional level
- knows the document genre and its conventions
- knows every publicly available general fact about the subject
- has read nothing that is specific to this project, this run, this incident,
  this codebase, or this dataset

The question is then decidable in one direction. If the stranger can write the
sentence, you know it. If you believe the stranger cannot, you owe a fact: the
particular thing in the sentence that is unavailable to anyone outside the
work. That fact is the artifact this procedure produces, and without it the
test has not been run.

## Why the substitution finds anything at all

`wikipedia-signs-of-ai-writing` gives the mechanism in its own words. Language
models infer what should come next from a large corpus and therefore regress
toward the most statistically likely result that applies to the widest variety
of cases. Its illustration is the one worth memorising: the highly specific
inventor of the first train-coupling device becomes a revolutionary titan of
industry. The subject becomes simultaneously less specific and more
exaggerated. The same guide lists, on the other side of its ledger, specific,
unusual, hard-to-fabricate detail as a sign of human writing, on the reasoning
that models round specifics off while people hoard them.

Round-off is exactly what the substitution detects. A rounded sentence is one
whose remaining content is available to the widest variety of cases, which is
another way of saying it is available to the stranger.

`kobak-excess-vocabulary` measured the residue of that process across more than
15 million PubMed abstracts from 2010 to 2024, finding that at least 13.5
percent of 2024 abstracts were processed with a model, up to 40 percent in some
subcorpora, and that the excess vocabulary is overwhelmingly stylistic verbs
and adjectives rather than content words. Stylistic words are precisely the
words the stranger already owns. That is why this test targets a class of
defect rather than a word list, and why it does not rot the way word lists do.

## The operation

1. Select one sentence or one clause. Not a paragraph. The unit must be small
   enough that a single fact can be named for it.
2. Name the stranger out loud, in the artifact, at the level described above.
   "A competent SRE who has never seen this incident" is a named stranger.
   "Someone else" is not.
3. Ask the substitution question and answer it yes or no before looking for a
   repair. Deciding the verdict and the fix at the same time biases both.
4. If the answer is no, write the fact. One line, with the thing that makes it
   unavailable to the stranger: a number, a timestamp, an identifier, a name, a
   file path, a measured outcome, a decision and its reason.
5. Locate that fact in a source of record and write the location down beside
   it. A fact you cannot locate is a fact you are about to invent.
6. If the answer is yes and no locatable fact exists, the verdict is generic.
   Cut the sentence or replace it with the located fact. Never decorate it.
7. Record the artifact: span, stranger, verdict, fact or the literal word
   `absent`, and the source of record.

Step 5 is the load-bearing step and the one most often skipped. Steps 1 to 4
can be performed on a document alone. Step 5 cannot, and a stranger test run
without access to the source of record can only ever return a suspicion.

## The substitution ledger

| Sentence contains | Stranger can supply it | Therefore |
| --- | --- | --- |
| A claim about why something matters | Yes, always | Generic by construction |
| A named public entity and a public fact about it | Yes | Generic unless the pairing is the finding |
| A number with a unit and a measurement context | No | Specific, check it under [[The Attribution Test]] |
| A timestamp, commit sha, ticket id, or file path | No | Specific |
| A decision plus the constraint that forced it | No | Specific, and usually the most valuable line in the document |
| A negative result or a thing that did not work | No | Specific, and rarely invented by anyone |
| A named tradeoff with the side that was accepted | No | Specific |
| A list of three qualities of the subject | Yes | Generic, see [[Tricolon and Rule of Three]] |
| An assertion that the subject reflects a broader trend | Yes | Generic, see [[Puffery and Undue Emphasis]] |

The right column never says "delete". It says what the substitution established.
Deletion is a separate decision, taken by the author, after the artifact exists.

## Substitution one: a migration writeup

Source paragraph, from the summary section of an internal writeup:

> The migration was carefully planned and executed with minimal disruption to
> end users. The team worked closely with stakeholders throughout, and the
> results speak for themselves. This effort reflects our ongoing commitment to
> platform reliability.

Artifact:

```text
SPAN:      migration writeup, Summary, sentences 1 to 3
STRANGER:  a competent platform engineer who has never seen this migration
CAN THE STRANGER WRITE IT?  yes, in full, from the genre alone
ONLY-THE-DOER FACT:  absent
SOURCE OF RECORD:  cutover runbook and the dual-write dashboard export
FACT RECOVERED FROM RECORD:  cutover ran 02:40 to 03:21 UTC on 2026-03-11;
           dual writes held for 41 minutes; 3 of 1,904 sessions were dropped
           when the read replica lagged 9 seconds behind the primary
VERDICT:   generic. severity medium, confidence confirmed.
REPAIR:    replace all three sentences with the recovered fact.
```

The repaired paragraph is shorter than the original and says more. Note what
the repair did not do: it did not invent the 41 minutes. The number was read
out of the dashboard export. Had the export not existed, the correct repair
would have been to cut the three sentences and write nothing in their place.

`masrour-damage-humanizers` is the reason that distinction is stated as a rule
rather than a preference. Its documented failure modes for tools that rewrite
text toward a more human register include hallucinated citations, comment
leakage and nonsensical strings, and it found that all such tools tend to
degrade the original, with a fluency win rate against the original of 26.0
percent for the best tier of tool, 14.67 percent for the middle tier and 2.67
percent for the worst. A stranger test that ends in an invented specific has
converted a medium-severity padding defect into a critical-severity false
statement. That is a worse document, arrived at through a correct diagnosis.

## Substitution two: the acquittal

Source sentence, from a library's usage documentation:

> A `Session` object reuses the underlying TCP connection, so issuing repeated
> requests through one session avoids repeating the handshake.

Artifact:

```text
SPAN:      docs/usage.md, "Sessions", sentence 1
STRANGER:  a competent Python developer who has never read this library
CAN THE STRANGER WRITE IT?  yes
ONLY-THE-DOER FACT:  absent
VERDICT:   generic, and correct as written. No finding.
REASON:    the section's purpose is to state a general property of the API to
           a reader who does not have it. Genericity is the deliverable here.
```

This is the acquittal the test exists to protect, and it is the boundary
condition that separates this procedure from a style rule. Genericity is a
defect only where the document's purpose is to transmit what the author
learned: postmortems, research summaries, review notes, design records, commit
messages, evaluations. In reference material, tutorials, definitions and
standards text, the general statement is the product, and a demand for
project-specific detail would make the page worse.

Decide which kind of document you are in before step 1. Running this test on a
glossary produces a page of false findings, and every one of them will look
convincing.

## Substitution three: a review comment

```text
SPAN:      pull request 4417, review comment 2
TEXT:      "Looks good overall. Some minor considerations around error
            handling and maintainability, but nothing blocking."
STRANGER:  any reviewer who has not opened the diff
CAN THE STRANGER WRITE IT?  yes, without opening the diff
ONLY-THE-DOER FACT:  absent
VERDICT:   generic. severity high, confidence confirmed.
NOTE ON SEVERITY: this span is an approval. A generic sentence that carries an
           approval transfers unearned assurance downstream, which is a
           different cost from a padded paragraph in an essay.
```

Severity here comes from the function of the span, not from its length or its
register. See [[Commit and Review Surface]] for the surface treatment and
[[The Firewall]] for why severity and confidence never collapse into one score.

## What the substitution cannot do

- **It cannot check truth.** A specific, unrepeatable, entirely fabricated
  detail passes this test perfectly, which is why step 5 exists and why
  fabricated support is handled by [[The Attribution Test]].
- **It cannot be run by a model on suspicion alone.** `shaib-measuring-slop`
  measured span-level slop extraction by GPT-5 at precision 0.14 and recall
  0.11, with a fine-tuned Qwen-7B reaching 0.32 and 0.30. Roughly six in seven
  model-nominated spans are not what the model claims. The artifact, not the
  nomination, is the finding.
- **It cannot distinguish a generic sentence from a sentence about a genuinely
  general subject.** Only the document's purpose settles that, and purpose is
  an input to this test rather than an output of it.
- **It says nothing whatsoever about who wrote the span.** Human writers
  produce genre-shaped filler constantly, and [[Distributional Convergence]]
  plus the convergence evidence in [[Marker Cohort Rot]] means the surface is
  moving toward the middle from both directions. The finding is that the span
  carries no work, not that no person did any.

## Related

- [[The Firewall]]
- [[The Deletion Test]]
- [[The Inversion Test]]
- [[The Attribution Test]]
- [[The Load Bearing Test]]
- [[Why Structural Not Judgmental]]
- [[Signs Are Not The Problem]]
- [[Puffery and Undue Emphasis]]
- [[Marker Cohort Rot]]
- [[index|Index]]
