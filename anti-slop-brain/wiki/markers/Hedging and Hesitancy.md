---
type: "marker"
title: "Hedging and Hesitancy"
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
  - "[[The Attribution Test|Attribution Test]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[Excess Vocabulary]]"
  - "[[Tricolon and Rule of Three]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Humanizers|Repair Degrades Voice]]"
  - "[[Prose Surface]]"
  - "[[Agent Output Surface|Chat Transcripts]]"
  - "[[The Firewall]]"
source_urls:
  - "https://arxiv.org/abs/2604.19768"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://arxiv.org/abs/2604.22142"
---

# Hedging and Hesitancy

Hedging is where this folder's evidence openly disagrees with itself, and the
disagreement is not resolvable by picking a side. One well-observed source
lists hedging qualifiers among the signs of **human** writing. Another
well-packaged tool instructs a model to delete them as a sign of machine
writing. Both are describing something real. A brain that smooths this over
would be hiding its most useful finding, so this note states the conflict
first and reconciles it second.

## Two different things wear the same name

**Epistemic hedging** marks the strength of a claim: may, tends to, suggests,
in most cases, roughly. It is load-bearing. Removing it converts a careful
claim into an overclaim, which is a factual defect introduced by an editing
pass.

**Hesitancy filler** performs uncertainty without carrying any: it could
potentially possibly be argued that, some might say, it is worth noting that,
while specific details are limited. It marks nothing, because it modifies no
specific quantity and commits to no specific doubt.

The marker in this note is the second. The first is a thing to protect. Any
procedure that cannot tell them apart will damage documents, and most of the
prior art cannot tell them apart.

## The measured density

`bakhshi-saying-more` reports that language models produce hesitancy markers at
**roughly twice human density**, measured across 225 texts and approximately
600,000 tokens with an expert comparison group. The same paper produced the
tricolon figure carried in [[Tricolon and Rule of Three]], and the two findings
share a corpus, which is worth knowing when both fire on one document: they are
not independent confirmations.

That measurement is what places hedging density at Tier 1 in
[[Evidence Tiers]]. As with every tier, it licenses routing to a procedure and
nothing beyond that. The paper is a preprint verified at abstract level, which
caps the note's confidence at practitioner.

## The conflict, stated rather than smoothed

`wikipedia-signs-of-ai-writing` maintains a section on signs of **human**
writing whose syntax entry is based on over 25 years of observing Wikipedia
prose. It lists as human-characteristic: hedging qualifiers and intensifiers
such as very, perhaps and tends to; superlative or definitive statements such
as one of the best, is the only, was the first; and isolated wordy
constructions such as as a result of, in order to, all of the, and the fact
that.

`blader-humanizer` instructs a model to delete exactly those items. Its
pattern 23 rewrites "in order to achieve this goal" and "due to the fact that",
and its pattern 24 rewrites stacked modals into a single clean modal.

| Construction | `wikipedia-signs-of-ai-writing` | `blader-humanizer` | This brain |
| --- | --- | --- | --- |
| in order to, as a result of, the fact that | human signal | delete as filler | leave alone |
| very, perhaps, tends to | human signal | reduce as hedging | leave alone |
| one of the best, was the first | human signal | not addressed | leave alone, but route to [[The Attribution Test|Attribution Test]] |
| could potentially possibly be argued | not addressed | delete | flag as hesitancy stacking |
| while specific details are limited, it is believed that | AI signal, speculative gap-filling | delete | flag, and treat the speculation as the finding |

The two sources are not measuring the same thing. Wikipedia is describing what
distinguishes a human editor's prose from smooth model output, where the
smoothness itself is the tell. Prior art is describing what makes prose read as
tight. Optimising for tightness deletes the human signal. That is the trap, and
it is not hypothetical: `vannuenen-voice-under-revision` found across 300
personal narratives and three models that model revision decreases function
words, contractions and first-person pronouns while increasing vocabulary
diversity and word length, and that the shift persists even under explicit
instructions to preserve the author's voice, with rewritten texts converging in
feature space regardless of where they started. Stripping filler is one of the
mechanisms by which that convergence happens. See [[Humanizers|Repair Degrades Voice]].

## How this brain resolves it

1. Never delete a hedge on sight. The presence of a hedge is not a finding.
2. Flag only **stacking**: two or more uncertainty markers modifying the same
   proposition. "It could potentially possibly be argued" stacks three. "The
   policy may affect outcomes" stacks one and stays.
3. Flag **unresolvable hedges**: an uncertainty marker attached to a claim with
   no source, where the hedge is doing the work a citation should do. These go
   to [[The Attribution Test|Attribution Test]], and the finding is the missing source rather than
   the hedge.
4. Flag **speculative gap-filling**, the form where the text writes a paragraph
   about the absence of information and then invents plausible filler to cover
   it: information about her early life is not publicly available, suggesting
   she maintains a low profile, she likely grew up in a middle-class household.
   The source is blunt that this is entirely speculative, including the claim
   that the information is undocumented. The repair is to say what is not
   known, or to cut the sentence, and never to dress the guess as a fact.
5. Leave single hedges, wordy connectives, and intensifiers alone unless the
   document's own house style bans them. House style is a separate axis from
   evidence, exactly as it is for the character discussed in [[The Em Dash]].

## The stacking threshold

| Uncertainty markers on one proposition | Class | Action |
| --- | --- | --- |
| 0 | assertion | check it has a source |
| 1 | ordinary epistemic hedge | leave |
| 2 | stacking | run [[The Deletion Test|Deletion Test]] on the weaker marker, keep one |
| 3 or more | hesitancy filler | rewrite to a single marker, and report the claim as unsourced if no source resolves |

## False positive class: who this marker wrongly flags

1. **Scientists and statisticians.** Careful modality is the discipline's core
   competence. A methods section is dense with hedges because the findings are
   conditional.
2. **Lawyers and compliance writers.** Qualified language is legally necessary
   and stacking is sometimes deliberate.
3. **Clinicians and safety writers.** Hedged phrasing protects readers from
   overconfident advice.
4. **Second-language writers.** Hedging is explicitly taught in academic
   English instruction, and `stowe-detector-bias` establishes that
   English-language-learner writing is already disproportionately flagged by
   automated detection, with human annotators showing no comparable
   demographic bias. See [[Detector Bias Against Language Learners]].
5. **Anyone writing about uncertain things.** Forecasts, risk registers, and
   incident postmortems are supposed to hedge.
6. **Autistic and precise writers** who qualify claims because they mean the
   qualification literally.

## Related

- [[Evidence Tiers]]
- [[Tricolon and Rule of Three]]
- [[Excess Vocabulary]]
- [[The Attribution Test|Attribution Test]]
- [[The Deletion Test|Deletion Test]]
- [[Humanizers|Repair Degrades Voice]]
- [[Detector Bias Against Language Learners]]
- [[The Em Dash]]
- [[The Firewall]]
- [[Prose Surface]]
