---
type: "marker"
title: "Puffery and Undue Emphasis"
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
  - "[[Excess Vocabulary]]"
  - "[[Distributional Convergence]]"
  - "[[The Inversion Test|Inversion Test]]"
  - "[[The Stranger Test|Stranger Test]]"
  - "[[The Attribution Test|Attribution Test]]"
  - "[[Marker Cohort Rot]]"
  - "[[Prose Surface]]"
  - "[[Documentation Surface]]"
  - "[[The Firewall]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://www.science.org/doi/10.1126/sciadv.adt3813"
---

# Puffery and Undue Emphasis

Wikipedia's editors have been removing this pattern from articles for longer
than anyone has been studying it, and in `wikipedia-signs-of-ai-writing` it is
the largest and most developed category in the entire taxonomy. That is the
argument for Tier 1 status under [[Evidence Tiers]]: not a controlled
experiment, but sustained adversarial observation by thousands of people who
were correcting real damage, cross-checked against the vocabulary evidence in
`kobak-excess-vocabulary`, where the excess words turned out to be
overwhelmingly stylistic verbs and adjectives of exactly this kind.

## The mechanism, stated by the source

The guide's own explanation is the clearest statement of the mechanism this
whole brain is organised around. Statistical next-token prediction regresses to
the mean, so output tends toward the most likely result covering the widest
range of cases. The guide's image: a highly specific description such as the
inventor of the first train-coupling device becomes a revolutionary titan of
industry. The subject becomes simultaneously less specific and more
exaggerated. Volume rises as information falls.

That trade is the diagnostic. Puffery is not "positive writing". It is
positivity substituted for detail, and the substitution is what the repair
targets. See [[Distributional Convergence]] for the general form.

## The four subtypes the source separates

**Significance, legacy, and broader trends.** Arbitrary facts are attached to a
wider movement. Watch for: stands as, serves as, is a testament to, plays a
vital role, marks a pivotal moment, reflects broader, evolving landscape,
setting the stage for, indelible mark, deeply rooted. A frequent sub-form is
the hedging preamble that concedes low importance and then asserts it anyway:
though it saw only limited application, it contributes to the broader history
of early aviation engineering. Another is situating a subject amid debates that
are never named: generated debate, shaped emerging policy discussions, prompted
broader reflection, raising philosophical questions.

**Notability and media coverage.** The text argues that the subject deserves
coverage instead of describing it. Watch for: independent coverage, national
media outlets, trade publications, profiled in, written by a leading expert,
active social media presence, maintains a strong digital presence. Two details
worth carrying: this subtype is more common in output from tools released in
2025 or later, and models often echo the exact wording of Wikipedia's own
notability guidelines back into article prose.

**Promotional and advertisement-like language.** Watch for: boasts a, vibrant,
rich, profound, enhancing its, showcasing, exemplifies, commitment to, natural
beauty, nestled, in the heart of, groundbreaking, renowned, breathtaking,
must-visit, diverse array. The guide records an edit-summary paradox worth
knowing about: edits whose summary claims to have removed promotional tone
while introducing it.

**Vague attribution and overgeneralization of opinion.** Watch for: industry
reports, observers have cited, experts argue, some critics argue, several
publications, described in scholarship, modern researchers treat. The half that
prior art usually drops is overgeneralization: presenting one or two sources as
a widely held view, referring to reviewers or scholars in the plural while
citing one person, or implying a list is non-exhaustive when the sources give
no indication that other examples exist. Retrieval-augmented systems produce a
sharper version, stapling a hollow evaluative claim to a named real source that
says nothing close to it. That form routes to [[The Attribution Test|Attribution Test]], not to a
style fix.

## Topic-specific variants

| Topic area | Characteristic form | Example shape from the source |
| --- | --- | --- |
| Cultural heritage and place | rich cultural heritage, stunning natural beauty, nestled in the heart of | a town described as vibrant with rich heritage before any fact about it appears |
| Biology and species articles | over-emphasis on ecosystem connection, belaboured conservation status | no specific assessment exists for this species, however the general health of the lake ecosystem is crucial for its survival |
| People and companies | press-release register, notability argued rather than shown | views cited in four outlets, followed by a follower count |
| Institutions and infrastructure | founding dates recast as turning points | established in 1989, marking a pivotal moment in the evolution of regional statistics |

## Model generation changes the surface

The guide notes that older models produced more blatantly positive text, while
newer ones are more subtly positive and avoid obvious superlatives such as
"the best". A 2026 marker list tuned to 2023 output will miss the current form
and over-flag the old one. This is the specific case of the general problem in
[[Marker Cohort Rot]].

## False positive class: who gets wrongly flagged here

1. **Marketing and fundraising writers doing their job.** A grant application,
   a tourism page, and a product landing page are supposed to be promotional.
   The register is correct for the genre; only the missing specifics are a
   defect.
2. **Obituary, tribute, and award citation writers.** "Stands as a testament"
   is a genre convention with a century of human use behind it.
3. **Second-language writers trained on formal templates.** Elevated register
   and significance framing are taught as good academic style in many
   education systems.
4. **Domain conventions in conservation biology and heritage studies.**
   Ecosystem-connection framing is a real disciplinary norm, not an artifact.
5. **Anyone summarising a source that was itself promotional.** The puffery may
   be faithfully reported rather than invented, which the prior art in
   `blader-humanizer` correctly flags as secondhand text that should not be
   rewritten.

## Repair, and what repair is not

`blader-humanizer` treats this category as a rewrite target and stops there.
Its own upstream source warns against exactly that: the patterns are potential
signs of a problem rather than the problem itself, and treating the signs as
the thing to fix can simply make detection harder. Deleting "stands as a
testament to" from an unsourced claim leaves an unsourced claim.

The procedure, in order:

1. Run [[The Inversion Test|Inversion Test]] on the evaluative clause. Negate it. If nobody would
   ever write the negation, the clause carried no information and comes out.
2. Run [[The Stranger Test|Stranger Test]] on what remains. Name the fact in the sentence that
   only someone who read the source could know. If there is none, the sentence
   is generic regardless of its adjectives.
3. Run [[The Attribution Test|Attribution Test]] on every vague authority. Resolve it to a named
   source that supports the specific claim, or report it as unresolved.
4. Only then edit the wording. The wording was never the finding.
5. Never state or imply who or what wrote the passage. That rule is
   [[The Firewall]] and it does not bend for this marker.

## Related

- [[Evidence Tiers]]
- [[Excess Vocabulary]]
- [[Negative Parallelism]]
- [[Hedging and Hesitancy]]
- [[The Inversion Test|Inversion Test]]
- [[The Attribution Test|Attribution Test]]
- [[Marker Cohort Rot]]
- [[Distributional Convergence]]
- [[Prose Surface]]
- [[The Firewall]]
