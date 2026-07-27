---
type: "procedure"
title: "The Inversion Test"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/procedure"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[The Firewall]]"
  - "[[The Deletion Test]]"
  - "[[The Attribution Test]]"
  - "[[Why Structural Not Judgmental]]"
  - "[[Puffery and Undue Emphasis]]"
  - "[[Hedging and Hesitancy|Hedging and Hesitancy Markers]]"
  - "[[Sycophancy]]"
  - "[[Signs Are Not The Problem|Signs of AI Writing]]"
  - "[[Prose Surface]]"
  - "[[Commit and Review Surface|Commit and PR Surface]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2604.19768"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://doi.org/10.1126/science.aec8352"
---

# The Inversion Test

A sentence carries information only if it rules something out. Negate it and
look at what it ruled out. If the negation is a sentence no competent person
would ever assert, then the original excluded nothing, and asserting it was
free. Free assertions are the cheapest thing a language model produces and the
hardest thing for a reader to notice, because they are never wrong.

Unlike [[The Deletion Test]], this one does not touch the document. It is a
logical operation on a single proposition, and its artifact is a sentence you
write down that was never in the text.

## The operation as a rule of inference

Let `C` be the claim as written and `not C` its negation.

- If `not C` is assertable, meaning some informed person could sincerely write
  it in a comparable document, then `C` had content. It ruled `not C` out.
- If `not C` is not assertable by anyone, then `C` ruled nothing out. It is
  vacuous. Its truth was guaranteed before you read it.

The everyday form: **the test of a claim is whether its opposite is a claim.**

Notice what the rule does not do. It never asks whether `C` is true, whether it
is well written, or who wrote it. A vacuous sentence is usually true. That is
exactly why it survives review, and why an accuracy-focused reviewer will pass
it every time. Vacuity is a separate defect from falsity, and this is the only
one of the five procedures that isolates it.

## Building the negation

The result depends entirely on negating the right thing. Four rules, in order
of how often they are broken.

**Negate the predicate, not the subject.** "Observability is crucial for
distributed systems" inverts to "Observability is not crucial for distributed
systems", not to "Observability is crucial for monolithic systems". Swapping
the subject produces a different claim and tells you nothing about the original.

**Preserve the scope and the quantifier.** "In the three services we measured,
tail latency fell" inverts to "In the three services we measured, tail latency
did not fall". Dropping "the three services we measured" turns a bounded report
into a universal, and universals invert into assertable universals, so you get
a false acquittal.

**Do not negate a hedge into a claim.** "This may indicate a regression"
inverts to "This may not indicate a regression", which is also assertable, so
the hedged sentence passes. That is a known weakness and it is handled in the
next section rather than by bending the negation. `bakhshi-saying-more` measured
LLMs producing hesitancy markers at roughly twice human density, so hedges are
exactly the population this test is worst at, and pretending otherwise would be
worse than admitting it. See [[Hedging and Hesitancy|Hedging and Hesitancy Markers]].

**Negate the load-bearing verb in a chain.** "The framework enables teams to
build scalable systems efficiently" has three candidate predicates. Take the
one the sentence is for: `enables`. Inverting to "prevents teams from building
scalable systems" gives you the answer faster than inverting `efficiently`.

## Reading the verdict

| Status of `not C` | Verdict on `C` | Severity | Action |
| --- | --- | --- | --- |
| Nobody would assert it, in any document | Vacuous | medium | Cut, or replace with the specific claim it was standing in for |
| Only a vendor or an adversary would assert it | Weak but real | low | Leave. It is a position, not a truism |
| A competent person could assert it and be wrong | Genuine claim | none | Leave alone. Route to [[The Attribution Test]] instead |
| A competent person could assert it and be right | Genuine and contested | none | Leave alone. This is the good case |
| `not C` is also what `C` says | Both-sided | medium | The sentence affirms both branches and settles nothing |

The last row deserves its own note. `cheng-elephant-sycophancy` measured models
affirming both sides in 48 percent of moral conflicts. A both-sided sentence
inverts into itself: "While speed matters, correctness is also important"
negates to "While correctness matters, speed is also important", and both are
the same non-position. See [[Sycophancy]].

## Four inversions, worked

**Inversion 1.** The canonical case.

```text
C:     "Data quality plays a crucial role in model performance."
not C: "Data quality plays no role in model performance."
ASSERTABLE BY ANYONE? No. Nobody has ever written that sentence sincerely.
VERDICT: vacuous. severity medium, confidence confirmed.
REPAIR:  the specific claim it was standing in for was available two
         paragraphs later: "Deduplicating the training set cut eval loss
         by 0.04." That inverts to "Deduplicating raised eval loss by 0.04",
         which is assertable and in fact happens. Use that sentence instead.
```

**Inversion 2.** The importance-of construction.

```text
C:     "These results highlight the importance of careful evaluation design."
not C: "These results highlight the unimportance of careful evaluation design."
ASSERTABLE BY ANYONE? No.
VERDICT: vacuous. severity medium, confidence confirmed.
NOTE:    the sentence also claims that "these results" support something. They
         cannot support a tautology, so the citation is decorative. This one
         fails two tests at once.
```

**Inversion 3.** The acquittal. This is the outcome the test exists to protect.

```text
C:     "The rewrite cut p99 latency by 31 percent and raised resident memory
        by 12 percent on the same hardware."
not C: "The rewrite raised p99 latency by 31 percent and cut resident memory
        by 12 percent on the same hardware."
ASSERTABLE BY ANYONE? Yes. That is an ordinary and common outcome, and a
        reviewer would want to know which one happened.
VERDICT: genuine claim. Leave the sentence exactly as written.
```

**Inversion 4.** The trap that looks vacuous and is not.

```text
C:     "Detector accuracy is not uniform across writing populations."
not C: "Detector accuracy is uniform across writing populations."
ASSERTABLE BY ANYONE? Yes. Detector vendors assert it routinely, in marketing
        and in support documentation.
VERDICT: genuine and contested. Leave alone.
ROUTE:   this claim is load bearing and needs a source, so it goes to
         [[The Attribution Test]], not to a cut.
```

Inversions 1 and 2 are the same grammatical shape as 4. Register, sentence
length, and vocabulary do not separate them. Only the negation does.

## The failure mode: acquitting is the point

The most common way to misuse this test is to treat every acquittal as a near
miss and rewrite the sentence anyway, usually by adding emphasis to make it
sound more substantial. That is how a plain true sentence becomes puffery.

`wikipedia-signs-of-ai-writing` warns specifically against treating the surface
signs as the problem to be fixed, on the grounds that removing the sign can
simply make the underlying defect harder to detect. Applied here: a genuine
claim that reads flatly is not a defect. A flat true sentence is the target
state, not a waypoint on the way to a better one. If inversion 3 or 4 fires,
the correct edit count is zero.

The second failure mode is running this on non-claims. Instructions, questions,
definitions, and section headings are not propositions and do not invert.
"Assume the role has already propagated" has no negation in the required sense.
Skip them rather than forcing an answer.

## Where inversion cannot reach

- **Hedged assertions**, as noted above, pass in both directions. Pair this
  test with the deletion test: "this may indicate a regression" often deletes
  with no loss even though it inverts cleanly.
- **True and specific but unsupported claims** invert perfectly and are still
  defects. They belong to [[The Attribution Test]].
- **True, specific, supported, and generic** claims also invert perfectly. If
  the sentence could have been written by someone who never opened the source
  material, that is [[The Stranger Test]].
- **Individual words.** Inversion operates on propositions. `kobak-excess-vocabulary`
  found that the excess vocabulary in the 2024 corpus is dominated by stylistic
  verbs and adjectives rather than content words, which is why a word-level
  version of this test would just be a banned-word list, and why
  [[The Firewall]] forbids acting on one.

## Related

- [[The Firewall]]
- [[The Deletion Test]]
- [[The Stranger Test]]
- [[The Attribution Test]]
- [[Why Structural Not Judgmental]]
- [[Puffery and Undue Emphasis]]
- [[Hedging and Hesitancy|Hedging and Hesitancy Markers]]
- [[Sycophancy]]
- [[Signs Are Not The Problem|Signs of AI Writing]]
- [[Evidence Tiers]]
