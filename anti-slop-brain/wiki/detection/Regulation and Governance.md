---
type: "concept"
title: "Regulation and Governance"
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
  - "[[Watermarking]]"
  - "[[Content Provenance]]"
  - "[[Why Detection Fails]]"
  - "[[Human Expert Review]]"
  - "[[The Firewall]]"
  - "[[Knowledge Base Surface]]"
  - "[[Superseded Figures]]"
  - "[[Evidence Quality Ladder]]"
  - "[[The Moral Panic Objection]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://artificialintelligenceact.eu/article/50/"
  - "https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models/RfC"
  - "https://arxiv.org/abs/2604.24890"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
---

# Regulation and Governance

Dates do the work in this note. Two governance regimes now bear on generated
text, one statutory and one community-made, and both are frequently described
with the wrong status or the wrong deadline attached. Laid out chronologically,
the errors become visible.

## Timeline

| Date | Event | Status | Ledger id |
| --- | --- | --- | --- |
| 2026-03-20 | Wikipedia RfC closes 44 to 2 under SNOW | in force, content guideline | `wikipedia-llm-guideline` |
| 2026-04-27 | First independent C2PA security analysis published | preprint, abstract-level verification | `c2pa-security-analysis` |
| 2026-06-16 | Digital Omnibus adopted by the European Parliament | adopted | `eu-ai-act-article-50` |
| 2026-06-29 | Digital Omnibus adopted by the Council | adopted | `eu-ai-act-article-50` |
| 2026-08-02 | EU AI Act Article 50 transparency duties apply | applies, not amended by the Omnibus | `eu-ai-act-article-50` |
| 2026-12-02 | Article 50(2) machine-readable marking deadline for systems already on the market | forthcoming | `eu-ai-act-article-50` |

## 2026-03-20: a knowledge base writes its own rule

The English Wikipedia closed a request for comment on 2026-03-20 by a margin of
**44 to 2**, under SNOW, meaning the outcome was so lopsided that continuing the
discussion served no purpose. The outcome prohibits using large language models
to generate or rewrite article content, with two surviving exceptions:

1. **Copyediting your own writing**, under mandatory human review.
2. **LLM-assisted translation**, also under mandatory human review.

Both exceptions carry the same condition, and it is the condition rather than
the permission that is doing the work. The community did not draw a line around
which tools may be used. It drew a line around who is answerable for the text,
which is the same move [[The Firewall]] makes when it insists on an artifact
rather than a verdict.

**It is a content guideline, not a policy.** On Wikipedia that distinction is
substantive: guidelines describe best practice and admit exceptions, policies
are standards that editors should normally follow without them. Calling it a
policy overstates the authority of the document you are leaning on, which is
recorded as a defect in [[Superseded Figures]]. The related descriptive guide,
`wikipedia-signs-of-ai-writing`, is a living community page rather than any kind
of rule, and it says of itself that its listed patterns are potential signs of a
problem rather than the problem.

## 2026-08-02: Article 50 starts to apply

Article 50 of the EU AI Act sets transparency duties on providers and deployers
of systems that generate synthetic content, and it applies from **2026-08-02**
(`eu-ai-act-article-50`).

The confusion worth clearing up concerns the Digital Omnibus, adopted by the
Parliament on 2026-06-16 and by the Council on 2026-06-29. It **deferred
high-risk deadlines only**. Article 50 was **not amended by it**. A briefing
that says "the Omnibus pushed everything back" is wrong about the one article
that governs marking of generated content.

Penalties under this regime reach **15 million euro or 3 percent of turnover**.

## 2026-12-02: the transitional deadline

Generative systems already on the market before 2026-08-02 have until
**2026-12-02** to satisfy the Article 50(2) machine-readable marking
requirement. This is the row most often dropped from summaries, and it is the
one an operator with a deployed system actually needs.

The technical difficulty is documented elsewhere in this folder and is not
resolved by the deadline existing. Marking is a duty a producer can discharge.
Inferring origin from the absence of a mark is an inference nobody can support,
because coverage gaps make absence uninformative in both directions. That
argument is in [[Watermarking]], and the evidence that the marks themselves
survive editing poorly is there too.

Provenance sits in the same position. `c2pa-security-analysis`, the first
independent security review of the specifications, concludes that they fail to
achieve their claimed security goals and should not yet be relied upon for
high-stakes uses such as financial disclosures, journalism, or legal evidence,
and that version 2.4 does not address the identified problems. It is a preprint
verified at abstract level, so it is tier CONTESTED, and it still points the
same way as every other robustness result in [[Content Provenance]].

## What the timeline does not contain

Naming the absences matters as much as the entries, because a governance note
that reads as comprehensive invites people to act as though it is.

- **No obligation on readers to detect anything.** Article 50 places duties on
  producers and deployers. Nothing in it authorises accusing an author, and
  nothing in it makes a detector's output admissible for anything.
- **No verified ISO status for C2PA.** The claim that the specifications are now
  published as an ISO standard could not be verified against any primary source
  and appears only in marketing material. It is not asserted here.
- **No United States federal equivalent** is recorded in this ledger. Its
  absence from this note means it was not verified, not that it does not exist.
- **No academic-integrity rule.** Institutional detection policy is out of scope,
  and the evidence in [[Why Detection Fails]] argues against building one on a
  classifier. [[Human Expert Review]] is the only adjudication path this vault
  supports.

## Confidence, stated plainly

The EU source is a **consolidated third-party rendering of the regulation rather
than the Official Journal text**, so its ledger confidence is `medium` and this
note inherits `practitioner`. It carries a living-document flag and a refresh
date of 2026-08-26, because a rendering of a regulation can change without the
regulation changing.

The Wikipedia RfC entry is `high` confidence but tier PRACTITIONER, because a
community consensus is authoritative for that community and for nothing else.
The rung ordering behind both judgements is in [[Evidence Quality Ladder]].

## Compliance reading procedure

1. **Identify your role.** Provider, deployer, or neither. Article 50 duties
   differ by role, and most people asking this question are neither.
2. **Verify the article text against EUR-Lex**, not against the rendering cited
   here, before acting on it. The ledger entry says so in its limitations.
3. **Check which deadline applies to your system.** Placed on the market before
   2026-08-02 means 2026-12-02 for machine-readable marking; after that date
   means 2026-08-02.
4. **Separate the marking duty from any detection ambition.** Discharging the
   first is achievable. The second is not supported by evidence in this vault.
5. **Record the date you checked**, since this note is a snapshot of a living
   rendering and both regimes are under active revision.
6. **Do not treat this note as legal advice.** It records what two sources say
   and when they were verified. That is its whole claim, consistent with
   [[What This Brain Does Not Claim]].

## Why governance is not the answer to slop

Both regimes above regulate **disclosure of origin**. Neither regulates
**quality**, and the gap between those two is the entire subject of this vault.
A perfectly marked, fully disclosed, guideline-compliant document can still be
padded, uncited, and useless to its reader. Marking tells you where a text came
from. It tells you nothing about whether the text holds up, which is the only
question a structural procedure can answer and the only one worth asking. The
temptation to treat a compliance checkbox as a quality signal is a variant of
the confusion examined in [[The Moral Panic Objection]].

## Related

- [[Watermarking]]
- [[Content Provenance]]
- [[Why Detection Fails]]
- [[Human Expert Review]]
- [[The Firewall]]
- [[Superseded Figures]]
- [[Evidence Quality Ladder]]
- [[Knowledge Base Surface]]
- [[The Moral Panic Objection]]
- [[Note Conventions]]
- [[index|Index]]
