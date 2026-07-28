---
type: "concept"
title: "What This Brain Does Not Claim"
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
  - "[[The Firewall]]"
  - "[[Why Detection Fails]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Marker Cohort Rot]]"
  - "[[Note Conventions]]"
  - "[[Superseded Figures]]"
  - "[[Content Provenance]]"
  - "[[Watermarking]]"
  - "[[The Moral Panic Objection]]"
source_urls:
  - "https://arxiv.org/abs/2507.00788"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2512.09292"
  - "https://arxiv.org/abs/2604.24890"
  - "https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/"
  - "https://doi.org/10.1038/s41586-024-07566-y"
---

# What This Brain Does Not Claim

Six limits, stated as refusals rather than as caveats. A caveat sits at the end
of a document and is skipped. A refusal is a property of the product: there is
no code path that produces the claim, no output field that could hold it, and
no prompt that unlocks it. Anything below that reads like modesty is actually a
constraint on what this brain can be made to do.

## The register

| Id | The claim this brain does not make | What it says instead | Where the refusal is enforced |
| --- | --- | --- | --- |
| N1 | This text was written by AI | a named defect, a location, an artifact | output schema has no authorship field |
| N2 | This writing scores 72 out of 100 | per-finding severity and confidence, never summed | no total is computed anywhere |
| N3 | These markers are the complete set | a tiered list with dated cohorts and known gaps | `refresh_due` on every ledger entry |
| N4 | AI-assisted code is measurably worse | a disagreement with the null result named first | [[The Code Slop Disagreement]] |
| N5 | Detectors can be made reliable | a refusal to build or recommend one | no detector is bundled or called |
| N6 | These notes are free of the defects described | a scorer run against this vault | `scripts/score_substance.py` in the build |

## The two architectural limits

**N1, authorship.** This brain cannot tell you who or what wrote a document,
and will not estimate it. `stowe-detector-bias` ran 16 detection models over
student essays labelled for gender, race and ethnicity, English-language-learner
status and socioeconomic status, and found ELL essays disproportionately
flagged, non-White ELL students disproportionately flagged relative to White ELL
peers, and human annotators showing no significant demographic bias on the same
essays. The bias belongs to the instrument. The full argument is in
[[The ESL Objection]] and the rule is rule 1 of [[The Firewall]].

The refusal is stronger than a policy against saying it. A percentage, a
likelihood, a colour-coded confidence bar or a phrase like "reads as generated"
are all the same output with different packaging, and none of them has a field
to occupy.

**N2, holistic quality.** There is no overall writing score here, and the
reason is measured rather than stylistic. `shaib-measuring-slop` compared LLM
judges against human slop annotations and found agreement near zero: kappa 0.01
for GPT-5, minus 0.01 for DeepSeek-V3, 0.03 for o3-mini. Models flagged spans at
0.03 to 0.08 against a human rate of 0.34, under-flagging by roughly five times,
and GPT-5 span extraction ran at precision 0.14 with recall 0.11. Roughly six in
seven model-nominated spans are not what the model says they are.

A holistic rating built on that operation would be a number with no referent,
and the number would be trusted in proportion to how confident it looked. Every
finding here therefore carries an artifact a reader can inspect, and severity
and confidence stay on separate axes so that no downstream reader can multiply
them into a single grade.

## The two evidential limits

**N3, completeness and durability of the markers.** The marker folder is not a
closed set and its contents have shelf lives. Vocabulary markers decay as human
usage absorbs model vocabulary, per-model figures expire with their model
rosters, and fine-tuning can eliminate a marker as easily as amplify it. The
mechanism and the maintenance cadence are in [[The Moving Baseline Objection]]
and [[Marker Cohort Rot]]. Anyone treating the marker list as a checklist for
authorship has misread both this note and [[Signs Are Not The Problem]].

**N4, the code literature.** This brain does not claim the AI code quality
question is settled, and it names the reason first rather than in a footnote.
`borg-null-result` was pre-registered with In-Principle Acceptance before data
collection and ran 151 participants. It is a preprint, arXiv 2507.00788, not a
published paper; the In-Principle Acceptance was granted at ICSME and the study
carries no journal reference. Its pre-registered Phase 2 found no significant
differences in subsequent code evolution, completion time or quality between
AI-assisted and unassisted development. Methodologically it is the strongest
single item in the area and that phase is a null. Phase 1, observational, ran
the opposite direction: a 30.7 percent median reduction in completion time with
an AI assistant, and an estimated 55.9 percent speedup for habitual AI users.
Reporting only the null is an incomplete citation.

The pattern around it is worth stating without softening: the strongest
pro-slop numbers in code come from vendors selling engineering-intelligence
products, and the strongest null results come from academia. This vault's
standing rule is that `borg-null-result` is cited whenever a vendor code-slop
figure is cited. The exception is defects that are decidable rather than
statistical, such as a dependency that does not exist in the registry, and those
are handled in [[Dependency Surface]] rather than by this debate.

## The limit on detection, including the good-faith versions

**N5.** This brain does not claim detectors can be fixed, and it does not
recommend one. OpenAI shipped a classifier that identified 26 percent of
AI-written text as likely AI-written while labelling human-written text as
AI-written 9 percent of the time, and withdrew it on 2023-07-20 citing its low
rate of accuracy (`openai-classifier-withdrawal`). That is a vendor abandoning
its own product on its own numbers.

The technically serious alternatives are also not claimed to work yet.
`c2pa-security-analysis` concludes that the C2PA specifications fail to achieve
their claimed security goals, states they should not yet be relied upon for
high-stakes uses such as financial disclosures, journalism or legal evidence,
and finds that specification version 2.4 does not address the identified
problems. It is a preprint verified at abstract level. Provenance and
watermarking are covered on their own terms in [[Content Provenance]] and
[[Watermarking]], and the reasons the whole category fails are in
[[Why Detection Fails]].

## The limit that applies to this vault

**N6.** Nothing here claims these notes are free of the defects they describe. A
knowledge base about padded, generic, uncited writing is the single most likely
document in any repository to be padded, generic and uncited, because its author
knows the vocabulary of quality and can produce the appearance of it.

The response is mechanical rather than aspirational.
`scripts/score_substance.py` runs against this vault in the build and counts
near-duplicate note pairs at an 8-token shingle similarity of 0.82, how many
notes share an identical H2 and H3 skeleton, how many repeat the same long line
verbatim, whether each note carries a real table or a numbered procedure,
whether each cites at least two distinct ledger sources without pasting an
oversized shared bundle, and how many words in each note appear on lines unique
to that note. None of those counts asks whether the writing is good and none
asks who wrote it. A vault that padded its notes to clear a line floor would
fail the density and duplication counts, which is the point. The full contract
is in [[Note Conventions]].

That check has a known blind spot, stated here rather than left to be
discovered: it cannot detect a claim that is well-cited, well-structured and
wrong. Only the source ledger and review catch that class, and
[[Superseded Figures]] exists because they have not always caught it.

## Sources that could not be read

Research is reported with its failures attached. The following could not be
retrieved directly, and every claim depending on them is either sourced
elsewhere or demoted.

| Source | Barrier | Consequence for this vault |
| --- | --- | --- |
| merriam-webster.com Word of the Year page | Cloudflare block on automated fetch | `merriam-webster-woty-2025` verified through wire copy dated 2025-12-15 |
| openai.com classifier post | HTTP 403 | `openai-classifier-withdrawal` figures confirmed through trade coverage of the withdrawal note |
| Nature Author Correction s41586-025-08905-3 | publisher authentication wall | the scope of the correction to `shumailov-model-collapse` is unknown to this brain |
| Harvard Business Review workslop article body | paywall | `betterup-workslop` figures taken from the vendor's own page |
| sciencedirect.com | HTTP 403 | `liang-gpt-detectors-biased` verified through its DOI record |
| IJEI 22:16 (2026), DOI 10.1007/s40979-026-00226-w | Springer paywall | the only third-party peer-reviewed detector evaluation found is unread |
| iso.org | HTTP 403 | the claim that C2PA is now an ISO standard could not be verified and is not repeated |
| Claude Opus 5 System Card | PDF exceeded the fetch limit | not relied on anywhere in this vault |

Three further limits on the research itself. Most 2026 entries in the ledger are
arXiv preprints verified at abstract level only, and are tiered `CONTESTED`
accordingly. The search budget was exhausted before three loose ends could be
closed, including the Nature correction above.

### A false claim that used to sit here

An earlier version of this note asserted that "every arXiv identifier in the
ledger was confirmed to resolve to a document with a matching title." That was
untrue when it was written. An adversarial pass on 2026-07-28 resolved all 23
identifiers and found **five whose ledger title matched no paper**: the entries
now corrected as `song-rubber-stamp-regime`,
`churilov-package-hallucination-2026`, `c2pa-security-analysis`,
`miletic-lexical-diversity`, and `borg-null-result` all carried invented
descriptive titles rather than real ones.

The identifiers themselves were all correct, and no citation was fabricated.
But a brain built to catch unverified assertions had published an unverified
assertion about its own verification, which is the exact failure its
[[The Attribution Test]] describes at rung two: a real, correctly named source
stapled to a claim it does not support.

What is true now, stated precisely:

| Claim | Status |
| --- | --- |
| All 23 arXiv identifiers resolve | Verified 2026-07-28 |
| Each resolves to a paper on the claimed topic | Verified 2026-07-28 |
| Ledger titles match the real titles | Verified after five corrections |
| Papers were read in full | **No.** Most are abstract level only |
| Every quoted figure appears in the source | **Not established.** Spot-checked, not exhaustive |

The corrected entries carry a `title_correction_note` recording what they used
to say. The record of the error is kept rather than quietly overwritten, on the
same reasoning as [[Superseded Figures]].

## Adding a limit

1. Write the claim in the form this brain would have to make it, in one
   sentence, as a positive assertion.
2. Identify what evidence would be required to support it, and check whether
   the ledger contains that evidence.
3. If it does not, add a row to the register above with the refusal and the
   substitute output.
4. Name the enforcement point: a missing schema field, an absent code path, a
   scanner, or a ledger cadence. A refusal enforced only by prose is a
   preference, and it will not survive the first person who wants the feature.
5. Link the limit from the note that would otherwise be read as making the
   claim, so the qualification travels with the assertion.

## Related

- [[The Firewall]]
- [[Why Detection Fails]]
- [[The Code Slop Disagreement]]
- [[Marker Cohort Rot]]
- [[The Moving Baseline Objection]]
- [[The ESL Objection]]
- [[The Moral Panic Objection]]
- [[Note Conventions]]
- [[Superseded Figures]]
- [[Content Provenance]]
- [[Watermarking]]
- [[Dependency Surface]]
