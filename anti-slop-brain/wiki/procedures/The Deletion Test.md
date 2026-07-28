---
type: "procedure"
title: "The Deletion Test"
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
  - "[[Why Structural Not Judgmental]]"
  - "[[The Load Bearing Test]]"
  - "[[The Stranger Test]]"
  - "[[Prose Surface]]"
  - "[[Code Surface]]"
  - "[[Documentation Surface]]"
  - "[[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]"
  - "[[Puffery and Undue Emphasis]]"
  - "[[Humanizers|Humanizer Quality Degradation]]"
source_urls:
  - "https://arxiv.org/abs/2509.19163"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
  - "https://arxiv.org/abs/2501.03437"
---

# The Deletion Test

Cut the span out. Then say, in words, what the reader no longer knows. If you
cannot finish that sentence, the span was padding and the cut is the repair.

The test is deliberately subtractive. It never asks for a rewrite, which means
it cannot introduce a new error, and that matters: `masrour-damage-humanizers`
found that all humanizers tend to degrade the original text, with a fluency win
rate against the original of 26.0 percent for the best tier of tool, 14.67
percent for medium and 2.67 percent for the worst. Deletion has no such failure
mode. The worst outcome of a wrong deletion is that you put the span back.

## The operation

1. Choose the smallest coherent unit: a sentence, a paragraph, a comment, a
   heading and its body. Do not delete across a boundary you cannot restore.
2. Remove it from the document. Actually remove it, in the editor. Reading a
   span while imagining it gone does not work, because the imagined version is
   still on the page.
3. Read the two neighbouring units end to end, in order, without the removed
   span between them.
4. Write one sentence beginning "Without this, the reader no longer knows". You
   must complete it with a specific noun: a number, a name, a constraint, a
   causal link, a consequence, a path, an identifier.
5. Check the completion against the loss table below. A completion that names
   nothing from the left column is not a loss.
6. Record the artifact: the cut span, the completed sentence or the explicit
   word `none`, and a verdict. Then restore or keep the cut.

Step 4 is the whole test. The default in step 4 is `none`, and the burden is on
keeping the span, not on cutting it. That inversion is intentional.
`shaib-measuring-slop` measured models flagging slop at 0.03 to 0.08 against a
human rate of 0.34, an under-flagging factor of roughly five. Any procedure
whose default answer is "leave it" will inherit that bias. Making `none` the
default forces the positive claim.

## What counts as a loss

| Candidate answer to step 4 | Counts as a loss | Reason |
| --- | --- | --- |
| A number, date, name, version, file path, or identifier vanishes | Yes | Information the reader cannot reconstruct |
| A causal link vanishes: X happens because Y | Yes | Relations are content |
| A precondition, constraint, or consequence vanishes | Yes | Changes what the reader will do |
| A concession or scope limit vanishes, so a claim now reads stronger than it is | Yes | Deleting a hedge can be a defect |
| A definition of a term used later vanishes | Yes | Forward dependency |
| "It transitions between the two sections" | No, downgrade to `probable` | Rhythm, not information |
| "It sets context" | No, unless you can name the context in the same sentence | Unnameable context is not context |
| "It helps a beginner" | Only if you name the specific thing the beginner would not otherwise know | Otherwise it is a guess about an absent reader |
| "It restates the point for emphasis" | No | Restatement is the defect being tested for |
| "The section would be short" | Never | Length is not a reader outcome |

The rows that count share one property: a second person can verify the loss by
searching the rest of the document for the same fact. The rows that do not
count cannot be checked by anyone.

## Cut one, prose: an incident postmortem

Source span, section 2 of a postmortem, 43 words:

> It is important to note that observability plays a crucial role in modern
> distributed systems. As organisations increasingly adopt microservice
> architectures, the ability to understand system behaviour becomes ever more
> essential. Without adequate visibility, teams can find themselves navigating
> complex failure modes.

The paragraph that follows it reads: "The 04:12 alert fired on p99 latency, but
the trace sampler was set to 0.001, so 4 of the 3,900 affected requests carried
spans. We reconstructed the rest from the load balancer access log."

Artifact:

```text
CUT: postmortem, section 2, paragraph 1 (43 words)
STEP 4: "Without this, the reader no longer knows ..." -> none.
        Every noun in the span (observability, microservices, visibility,
        failure modes) recurs, with numbers attached, in the next paragraph.
        No fact in the cut span is absent from the rest of the document.
VERDICT: padding. severity medium, confidence confirmed.
ACTION: keep cut. Section 2 now opens on the 04:12 alert.
```

This is the shape `kobak-excess-vocabulary` predicts. Its finding across more
than 15 million PubMed abstracts is that excess words are overwhelmingly
stylistic verbs and adjectives rather than content words: `crucial`, `essential`,
`increasingly`. The deletion test is aimed directly at that class, without
having to name any individual word, which is why it does not rot the way word
lists do. See [[Marker Cohort Rot]] and [[Puffery and Undue Emphasis]].

## Cut two, code: a comment

Two comments from the same file. The test runs identically on both and returns
different verdicts.

```python
# Increment the retry counter by one
retry_counter += 1

# The vendor paginates from 1 but reports total_pages from 0.
# Support ticket 88214, 2026-03-04, confirmed by their engineer.
page = raw_page + 1
```

Artifact:

```text
CUT A: "# Increment the retry counter by one"
STEP 4: -> none. The statement below it says retry_counter += 1.
VERDICT: padding. severity medium, confidence confirmed. Keep cut.

CUT B: the two-line vendor comment
STEP 4: "Without this, the reader no longer knows that the + 1 is a
        deliberate correction for a vendor off-by-one, nor where the
        evidence for it is." Names a causal link and an identifier.
VERDICT: load bearing. severity none. Restore.
```

Cut A restates the code. Cut B carries the one thing the code cannot: why. That
is the durable line for comments, and it holds regardless of who or what wrote
them.

When the answer to step 4 is not about a reader at all but about the program
(the build fails, a type check fails, a test stops passing), you have left this
test and entered [[The Load Bearing Test]], which uses the toolchain rather than
a sentence as its oracle.

## Cut three, documentation: a section

Source section:

```markdown
## Overview

This document provides an overview of the deployment process. It covers the
key steps involved and outlines the main considerations to keep in mind.
Readers should familiarise themselves with this material before proceeding.
```

Artifact:

```text
CUT: "## Overview" heading and its three-sentence body
STEP 4: -> none. "The key steps" are the four H2 headings that follow it and
        are already listed in the generated table of contents. No
        consideration is named. No precondition is stated.
VERDICT: padding. severity medium, confidence confirmed. Keep cut.
```

Contrast the section immediately after it, which looks similar and behaves
differently:

```text
CUT: "## Before you start"
STEP 4: "Without this, the reader no longer knows that the deploy role takes
        about 15 minutes to propagate after assumption, so a deploy attempted
        immediately will fail with an opaque 403."
VERDICT: load bearing. Restore. This section is the reason the page exists.
```

The `wikipedia-signs-of-ai-writing` guide makes the general point that these
patterns are only potential signs of a problem, not the problem itself, and
warns against treating the signs as the thing to fix, because removing a sign
can simply make the underlying defect harder to see. The deletion test is one
answer to that warning: it does not look at signs at all. Both sections above
share the same register, the same sentence length, the same heading depth. Only
one of them survives step 4.

## Three ways this test goes wrong

- **Deleting hedges that were doing work.** "In the three repositories we
  measured" is not padding around "latency fell". Removing a scope limit
  strengthens a claim you cannot support. Row 4 of the loss table exists for
  this.
- **Cutting a span whose loss is real but lives elsewhere.** If a fact appears
  in exactly two places and you cut one, step 4 correctly returns `none`. The
  verdict is still right: the duplicate was padding. Check that the surviving
  copy is the one in the better location before you keep the cut.
- **Batch deletion.** Cutting six spans and then reading once produces one
  vague impression instead of six artifacts. Run it once per span. The output
  of this test is a list of artifacts, and a list of one is not a list.

## What deletion cannot convict

Deletion finds spans that carry no information. It is silent on spans that
carry information which is wrong, unsupported, or attributed to nobody. A
fabricated statistic passes the deletion test cleanly, because removing it
genuinely does remove something the reader knew. That is [[The Attribution Test]].
A sentence that is true, specific, and could have been written by someone who
never read the source is likewise invisible here, and belongs to
[[The Stranger Test]]. Deletion is the cheapest of the five procedures and the
narrowest.

## Related

- [[The Firewall]]
- [[Why Structural Not Judgmental]]
- [[The Inversion Test]]
- [[The Attribution Test]]
- [[The Load Bearing Test]]
- [[Prose Surface]]
- [[Code Surface]]
- [[Documentation Surface]]
- [[Excess Vocabulary|Excess Vocabulary in Biomedical Abstracts]]
- [[Marker Cohort Rot]]
