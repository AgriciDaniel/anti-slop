---
type: "concept"
title: "Content Provenance"
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
  - "[[Why Detection Fails]]"
  - "[[Regulation and Governance]]"
  - "[[Provenance Trace Policy]]"
  - "[[The Firewall]]"
  - "[[Documentation Surface]]"
  - "[[Vendor Residue Markers]]"
  - "[[The Attribution Test]]"
  - "[[Evidence Tiers]]"
  - "[[Human Expert Review]]"
source_urls:
  - "https://arxiv.org/abs/2604.24890"
  - "https://artificialintelligenceact.eu/article/50/"
  - "https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models/RfC"
---

# Content Provenance

Provenance and detection are routinely discussed as if they were the same
project. They answer opposite questions, and conflating them produces the single
most common bad inference in this area: treating an asset with no provenance
manifest as suspicious.

Background on mechanism, not a ledger claim: the Coalition for Content
Provenance and Authenticity (C2PA) defines a manifest attached to an asset,
carrying assertions about how it was produced and a cryptographic signature
over those assertions. The vault's ledger holds one C2PA source, an independent
security analysis, so everything asserted below about security properties comes
from that paper and nothing is claimed about the specification text itself.

## Opposite questions

| | Provenance | Detection |
| --- | --- | --- |
| Question asked | what does the producer assert about this asset | what does a classifier infer about this text |
| Who supplies the evidence | the producer, voluntarily, at creation | a third party, after the fact |
| Failure when absent | no information | often misread as a positive signal |
| Failure when present | assertion may be false, stripped, or re-signed | score cannot be explained |
| Adversary model | someone who wants to forge or remove a claim | someone who wants to defeat a classifier |

The row that matters is the third. Provenance asserts positive origin. It does
not detect fakes. An unsigned file is the normal case for the overwhelming
majority of content ever produced, and treating unsigned as suspect converts a
voluntary disclosure scheme into an accusation engine. Under [[The Firewall]]
this vault does not make that move, for the same reason it does not act on
detector scores in [[Why Detection Fails]].

## The first independent security analysis

The load-bearing source is `c2pa-security-analysis`, an independent security
analysis of the C2PA specifications. Its conclusions, as stated by its authors:

- The specifications **fail to achieve their claimed security goals**.
- They **should not yet be relied upon for high-stakes uses** such as financial
  disclosures, journalism, or legal evidence.
- Specification **version 2.4 does not address** the identified problems.

Confidence handling: this is a preprint verified at abstract level, recorded at
`medium` confidence and `CONTESTED` tier in the ledger. It is single-source for
the security conclusion, and this vault has found no independent replication or
rebuttal to pair with it. That combination, an adversarial finding with no
counter-source, is exactly the shape that [[Evidence Tiers]] says must be stated
rather than smoothed over. The correct reading is not "C2PA is broken forever".
It is "the only independent security review on record is negative, the specific
high-stakes uses it names are the ones people most want to put it to, and no
published work yet contradicts it."

## The ISO claim that could not be verified

A claim circulates that C2PA has been adopted as ISO/IEC 22144. This vault
could not verify that claim against any primary source, and the claim appears
in marketing material rather than in a standards record accessible to this
research pass.

It is therefore recorded here as unverified and is not asserted anywhere in the
brain. The reason to write this down rather than to stay silent is that
standards adoption is a **status claim that changes how much weight a reader
gives a specification**. "An industry consortium published a spec" and "an
international standards body ratified it" license very different levels of
institutional trust, and the second one is currently unsupported here. This is
the same discipline applied to the unverifiable watermarking figure in
[[Watermarking]] and to vendor prevalence numbers in [[Why Pangram Is Not Cited]].

## What a manifest can and cannot support

| Statement | Supported by a valid manifest | Notes |
| --- | --- | --- |
| "The signer asserted this production history." | yes | this is the whole of what is signed |
| "The bytes have not changed since signing." | yes, within the binding's scope | scope is a specification detail, not verified here |
| "The assertion is true." | no | signing binds a claim, it does not audit it |
| "No generative model touched this." | no | only what was asserted, by whoever asserted it |
| "This unsigned asset is suspect." | no | absence is the default state of the world |
| "This is admissible in a high-stakes process." | no | explicitly warned against in `c2pa-security-analysis` |

## Handling a signed asset in review

1. Read the manifest as a **statement by a named party**, and record who that
   party is. An unattributed assertion is worth less than an attributed one.
2. Check whether the signer had any way to know what they asserted. A tool that
   signs "no AI used" because a checkbox was unticked is signing a checkbox.
3. Do not upgrade confidence in the content because the container is signed.
   Signature validity and content quality are unrelated axes, per
   [[The Firewall]].
4. Do not downgrade confidence in unsigned content. That is the inference this
   note exists to block.
5. Run the artifact checks that would have run anyway: do the references
   resolve, does [[The Attribution Test]] pass, is there vendor residue of the
   kind catalogued in [[Vendor Residue Markers]]. Residue is decidable evidence
   about tooling; a manifest is a claim about intent.
6. If the decision is high-stakes, record explicitly that the provenance layer
   was not treated as evidence, and cite `c2pa-security-analysis` for why.

## Where disclosure duties actually come from

Provenance metadata is not currently a reliable forensic instrument, but
disclosure obligations exist independently of it. Article 50 of the EU AI Act
carries transparency duties applying from 2026-08-02, with penalties reaching 15
million euro or 3 percent of turnover (`eu-ai-act-article-50`, a consolidated
third-party rendering rather than the Official Journal text). Wikipedia's
community route is different in kind: a content guideline adopted by RfC, not a
statute (`wikipedia-llm-guideline`). Both are covered in
[[Regulation and Governance]].

The practical consequence for this brain: disclosure is a duty owed by
producers, and this vault's internal chain of custody is handled by
[[Provenance Trace Policy]], which tracks source to claim to note to decision.
That chain is auditable because it is ours. A third party's manifest is not.

## Related

- [[Watermarking]]
- [[Why Detection Fails]]
- [[Regulation and Governance]]
- [[Provenance Trace Policy]]
- [[The Firewall]]
- [[Evidence Tiers]]
- [[The Attribution Test]]
- [[Vendor Residue Markers]]
- [[Why Pangram Is Not Cited]]
- [[Human Expert Review]]
