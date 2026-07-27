---
type: "concept"
title: "The Accessibility Objection"
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
  - "[[The ESL Objection]]"
  - "[[Signs Are Not The Problem]]"
  - "[[Distributional Convergence]]"
  - "[[Humanizers]]"
  - "[[Prose Surface]]"
  - "[[The Firewall]]"
  - "[[AI Slop]]"
  - "[[Regulation and Governance]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://arxiv.org/abs/2605.19936"
  - "https://arxiv.org/abs/2604.22142"
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2512.09292"
  - "https://simonwillison.net/2024/May/8/slop/"
---

# The Accessibility Objection

Restricting AI writing assistance is not a neutral act with a neutral cost. The
cost has a distribution, and it falls first on people for whom drafting prose
was already the expensive part: writers working in a second language, writers
with dyslexia or dysgraphia, writers managing fatigue, pain, tremor or
cognitive load, writers whose ideas have always outrun their capacity to render
them in publishable English. For those writers, a drafting assistant is not a
shortcut past the work. It is the ramp that gets them to the work.

This is not a rebuttal note. It is a tradeoff note, and the tradeoff is real in
both directions.

## The finding that damages the easy premise

Most anti-slop writing rests on an unstated premise: that machine-shaped prose
is worse prose, and that a reader with taste can tell. `miletic-lexical-diversity`
measured across more than 37,000 ACL Anthology papers and found the two halves
of that premise pointing opposite ways. LLM-modified text showed lower lexical
diversity than unmodified text, which is the flattening this vault documents
elsewhere. Expert readers nonetheless rated the modified text as more
understandable and more exciting.

Both results come from the same study, so they cannot be split apart and only
the convenient one kept. Lower diversity is the measurement that supports the
convergence argument in [[Distributional Convergence]]. Higher reader ratings
are the measurement that undercuts the aesthetic argument built on top of it.
The source is a preprint verified at abstract level and tiered accordingly; the
reader panel's size is not recorded in this brain's ledger and is therefore not
quoted here.

What survives is narrow and important. "Fewer distinct words" is not a synonym
for "worse". A writer who reaches an expert audience more clearly after a
revision pass has gained something, and a framework that cannot name that gain
is not describing the world.

## What is genuinely lost, and how it was measured

The loss is equally measured, and it is not about vocabulary size.
`vannuenen-voice-under-revision` ran 300 personal narratives through three
models and tracked what moved. Function words, contractions and first-person
pronouns fall. Vocabulary diversity and word length rise. Rewritten texts
converge in feature space regardless of where they started. The finding that
makes this more than a prompting problem is that the shift persists under
explicit instructions to preserve the author's voice.

Read the direction of those features. Contractions, function words and
first-person pronouns are the carriers of a person being present in a sentence.
What rises in their place is formality. So the assistance that makes a text
more legible to an expert reader is, in the same pass, moving it away from
sounding like anyone in particular. The gain and the loss are the same
operation viewed from two sides.

## The tradeoff ledger

| What changes | Direction | Measured by | Who gains or bears it |
| --- | --- | --- | --- |
| Lexical diversity | falls | `miletic-lexical-diversity` | reader, ambiguously |
| Rated understandability | rises | `miletic-lexical-diversity` | reader, clearly |
| Rated excitement | rises | `miletic-lexical-diversity` | reader, clearly |
| Function words, contractions, first-person pronouns | fall | `vannuenen-voice-under-revision` | author, as a loss |
| Word length and formality | rise | `vannuenen-voice-under-revision` | author, as a loss |
| Distance between two authors in feature space | falls | `vannuenen-voice-under-revision` | the corpus, as a loss |
| Cost of producing a publishable draft | falls | no ledger source found | disabled and second-language writers, as the gain |
| Risk of a false authorship accusation | rises | `stowe-detector-bias` | the same writers, as a second cost |
| Fluency against the original, under commercial humanizers | falls | `masrour-damage-humanizers` | author and reader both |

Two rows deserve to be read together, because they name the trap this note
exists to expose. The writers who gain most from assistance are the writers
already flagged most by detection, per `stowe-detector-bias` and the treatment
in [[The ESL Objection]]. Assistance raises their exposure to an accusation
they were already disproportionately likely to receive. Telling them to stop
using the tool is telling them to pay twice.

The last row is a separate warning. `masrour-damage-humanizers` states plainly
that all humanizers tend to degrade the quality of the original text, with
fluency win rates against the original of 26.0 percent for the best tier, 14.67
percent for medium and 2.67 percent for the worst, and documented failure modes
including hallucinated citations. The tool marketed as fixing the accusation
problem is a quality regression with a fabrication risk attached. See
[[Humanizers]].

## Where this brain draws its line

The line is not drawn at assistance. It is drawn at the defect, and the two are
separable in a way the aesthetic framing hides.

`willison-slop` is useful here precisely because it says nothing about how a
text was drafted. Its formulation locates the defect in mindless generation
imposed on a reader who did not ask for it. A disabled writer using a model to
render an argument they hold, checking the result, and standing behind it, is
not doing that. Someone generating volume and shipping it unread is doing that,
with or without a disability, with or without a second language. The definition
is discussed in full in [[AI Slop]].

| Practice | Is it targeted by this brain | Why |
| --- | --- | --- |
| Drafting with a model, then verifying every claim | no | no unverified claim reaches a reader |
| Rendering an author's own outline into prose | no | the argument is the author's |
| Model-assisted translation under human review | no | the reviewer owns the output |
| Publishing generated text without reading it | yes | imposition, per `willison-slop` |
| Citations produced by the model and never resolved | yes | a checkable defect regardless of who typed it |
| Style-only cleanup that leaves claims unchecked | yes | the failure mode in [[Signs Are Not The Problem]] |

The last two rows carry the point. Every item this brain flags is a property of
the artifact that a third party can verify. None of them requires knowing
whether a model was involved, and none of them becomes more or less true if the
author is disabled, a second-language writer, or neither.

## Accommodation without a style rule

1. Never state or infer a diagnosis, a first language, or a use of assistive
   tooling. It is not the brain's business and it is forbidden output under
   rule 1 of [[The Firewall]].
2. Never treat formal register, low contraction rate or long words as a defect.
   They are the features `vannuenen-voice-under-revision` shows revision
   produces, and they are also what a taught register produces natively.
3. Report only findings with an artifact: a claim with no resolvable source, a
   citation whose identifier resolves elsewhere, a span that deletes with no
   named loss.
4. Rank findings by reader harm, so a fabricated citation always outranks a
   flat sentence. A tool that surfaces style before substance trains its users
   to sand off voice, which is the harm this note is about.
5. Offer voice-preserving repairs as optional and claim-preserving repairs as
   mandatory. Only the second class is a defect fix.
6. When a repair would change how a sentence sounds without changing what it
   asserts, mark it as a style edit and let the author decline it.
7. Record declined style edits without escalation. A declined suggestion is
   not a finding and must not accumulate into one.

## What no source in this ledger establishes

No entry in this brain's ledger measures the productivity or participation gain
that AI writing assistance delivers to disabled writers or to second-language
writers. The gain row in the tradeoff ledger above is marked as unsourced for
that reason. It is asserted here as a widely reported practitioner experience
and as the premise of the objection being taken seriously, not as a measured
effect, and it should not be quoted from this note as though it were one.

Nor does any ledger source measure whether restrictions on AI assistance
actually reduce slop, as opposed to relocating it. That is a policy question
this brain has no evidence to answer, and it is left open in
[[What This Brain Does Not Claim]].

## Related

- [[The ESL Objection]]
- [[Signs Are Not The Problem]]
- [[Distributional Convergence]]
- [[Humanizers]]
- [[AI Slop]]
- [[The Firewall]]
- [[Prose Surface]]
- [[Regulation and Governance]]
- [[What This Brain Does Not Claim]]
- [[The Moral Panic Objection]]
