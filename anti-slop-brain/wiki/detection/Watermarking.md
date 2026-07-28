---
type: "concept"
title: "Watermarking"
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
  - "[[Content Provenance]]"
  - "[[Why Detection Fails]]"
  - "[[Humanizers]]"
  - "[[Regulation and Governance]]"
  - "[[Superseded Figures]]"
  - "[[Why Pangram Is Not Cited]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[Agent Output Surface|Agent Transcripts]]"
  - "[[Humanizers|Humanizer Quality Degradation]]"
source_urls:
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2605.19516"
  - "https://artificialintelligenceact.eu/article/50/"
  - "https://arxiv.org/abs/2604.24890"
---

# Watermarking

A watermark is a claim made at generation time. It travels with the text only
for as long as the text is left alone, and it says nothing whatsoever about
material the watermarking model never produced. Both of those properties are
usually skipped when watermarking is proposed as the answer to origin
questions, and both are decisive.

Background on mechanism: a text watermark biases token sampling so that a
detector holding the key can recover a statistical signal from the output. This
vault holds no primary specification source for SynthID-Text in its ledger, so
the mechanism sentence above is background rather than a cited claim. Every
number below is ledger-backed and attributed.

## The paraphrase result

The one measured figure this vault will quote comes from Masrour, Emi and Spero,
*DAMAGE*, published at GenAIDetect, COLING 2025 (`masrour-damage-humanizers`).
Measuring SynthID-Text at a fixed 5 percent false positive rate, the true
positive rate fell from **87.6 percent to 5.4 percent** after DIPPER paraphrase.

| Condition | True positive rate at 5 percent FPR | What it means operationally |
| --- | --- | --- |
| Unmodified generated text | 87.6 percent | most watermarked text is recovered |
| After DIPPER paraphrase | 5.4 percent | recovery is close to the floor |
| Delta | minus 82.2 points | one automated rewriting pass removes the signal |

Note the conflict of interest, because the ledger records it: DAMAGE was
authored by employees of a company that sells a detector. A finding that
watermarks are fragile is not obviously against their commercial interest, so
this figure carries less independent weight than the same paper's finding that
humanizers degrade text quality, which cuts against their interest and is
treated as stronger in [[Humanizers]]. The figure is recorded as `medium`
confidence for that reason.

The corroborating direction comes from `xu-base-models-look-human`, which
reports that iterative paraphrasing drives text to 100 percent human
probability by round 10. Watermark removal and detector evasion are the same
operation performed by the same tools, so a defence that fails against one
fails against both.

## The figure this note refuses to quote

There is a widely repeated claim that SynthID's detection rate falls from 100
percent to 21 percent under some evasion condition. It circulates in press
coverage and gets copied into slide decks, briefings and vendor comparisons.

**It could not be verified against any primary source and is not cited here.**
It is recorded in this vault only as an example of the failure mode, in the same
way that [[Why Pangram Is Not Cited]] records an undated vendor page and
[[Superseded Figures]] records numbers that were quietly corrected upstream.

The pattern is worth naming because it recurs:

1. A specific, memorable pair of numbers appears in secondary coverage.
2. The coverage does not link a paper, a table, or a methodology.
3. Downstream writers cite the coverage, and the number acquires the appearance
   of a measurement through repetition alone.
4. Nobody can say what corpus, attack, or false-positive threshold produced it,
   which means nobody can say what it would take to falsify it.

A number with no attached false-positive rate and no named attack is not a
measurement of anything. The 87.6 to 5.4 figure above is quotable precisely
because it names both: 5 percent FPR, DIPPER paraphrase, one paper, one table.
That is the standard [[Evidence Tiers]] applies, and it is why the more dramatic
number is the one that gets dropped.

## Coverage is the harder limit

Robustness is the limit people discuss. Coverage is the limit that actually
kills the idea for this brain's purposes.

- A watermark covers **only what the watermarking model generated**. Text
  written by a human, by an unwatermarked open-weights model, or by any model
  from a provider that has not deployed watermarking, carries no signal, and
  its absence is not evidence of anything.
- Absence of a watermark is therefore **uninformative in both directions**. It
  cannot clear a document and it cannot implicate one.
- Mixed documents, which is nearly all real work, contain generated spans,
  edited spans, and original spans. A document-level watermark verdict on a
  mixed document is a category error.
- The signal degrades under ordinary editing, not just adversarial attack. The
  DIPPER result is an upper bound on how careful an attacker has to be, and the
  answer is: not very.

This is where watermarking and provenance separate. Watermarking tries to make
generated content self-identifying. C2PA-style provenance tries to make the
production history assertable by the producer. The latter has different failure
modes, analysed in [[Content Provenance]] and in `c2pa-security-analysis`, which
concludes those specifications do not currently achieve their claimed security
goals.

## Reading a watermark result

1. Ask what false-positive threshold the reported rate was measured at. A true
   positive rate without its FPR is not interpretable.
2. Ask whether the text has been through any rewriting, translation,
   summarization, or editing pass since generation. If yes, treat a negative
   result as carrying no information.
3. Treat a negative result as uninformative regardless, because coverage gaps
   already make absence meaningless.
4. Treat a positive result as evidence that a specific watermarking model
   contributed some tokens, and nothing more. It is not a statement about a
   person, and under [[The Firewall]] this vault does not convert it into one.
5. Record which vendor's detector produced the result and on what date. Keys,
   thresholds and deployments change, and a stored verdict rots.

## Why regulation makes this matter anyway

Article 50 of the EU AI Act requires machine-readable marking of synthetic
content, applying from 2026-08-02, with generative systems already on the market
given until 2026-12-02 to meet the Article 50(2) marking requirement
(`eu-ai-act-article-50`, a consolidated third-party rendering rather than the
Official Journal text). So watermarking is becoming a **compliance obligation on
producers** at the same time as the evidence says it is a weak **forensic
instrument for consumers**. Those two facts are not in tension: marking your own
output is a duty you can discharge, while inferring origin from a missing mark
is an inference you cannot support. The obligations are set out in
[[Regulation and Governance]].

## Related

- [[Content Provenance]]
- [[Why Detection Fails]]
- [[Humanizers]]
- [[Regulation and Governance]]
- [[Superseded Figures]]
- [[Why Pangram Is Not Cited]]
- [[The Firewall]]
- [[Evidence Tiers]]
- [[Humanizers|Humanizer Quality Degradation]]
- [[Agent Output Surface|Agent Transcripts]]
