---
type: "marker"
title: "Vendor Residue Markers"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/marker"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
  - "[[The Em Dash]]"
  - "[[Marker Cohort Rot]]"
  - "[[Model Fingerprints]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Why Detection Fails]]"
  - "[[Content Provenance]]"
  - "[[Knowledge Base Surface]]"
  - "[[Agent Output Surface]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2502.12150"
  - "https://arxiv.org/abs/2512.09292"
---

# Vendor Residue Markers

A residue marker is a string that a rendering or citation layer emitted and
that nobody would ever type. `oaicite` is not a word. `(start_span)` is not
punctuation. `【85†L261-269】` is not a citation format any style manual
describes. These strings arrive in a document by one route only: something
pasted the raw output of a product interface without stripping the interface.

Every other entry in this folder is a claim about how text tends to read.
This one is not a claim about writing at all, and that difference in kind is
the entire content of the note. It is the reason these are the only markers
this brain treats as near-conclusive, and the reason they are handled by
`scripts/scan_residue.py` rather than by the tier system in
[[Evidence Tiers]].

## The token table

Sourced from the markup taxonomy in `wikipedia-signs-of-ai-writing`, sections
E3 and F6, as captured in the project snapshot on 2026-07-27. Every token is
shown in code formatting, for reasons that become clear in the false-positive
section.

| Vendor | Token | What emitted it | Scanner rule id |
| --- | --- | --- | --- |
| ChatGPT | `oaicite`, typically inside `:contentReference[oaicite:0]{index=0}` | reference markup layer | `residue.oaicite` |
| ChatGPT | `contentReference` | reference markup layer | `residue.content_reference` |
| ChatGPT | `oai_citation` | older reference markup layer | `residue.oai_citation` |
| ChatGPT | `turn0search0` and the general `turnNsearchN` form | search tool result handle | `residue.turn_search` |
| ChatGPT | `attributableIndex` | attribution metadata | `residue.attributable_index` |
| Gemini | `[cite: 1]`, `[cite: 3, 12, 13]` | citation annotation layer | `residue.gemini_cite` |
| Gemini | `[cite_start]` | citation span opener | `residue.gemini_cite_start` |
| Gemini | `(start_span)` and `(end_span)`, usually as `[span_1](start_span)` | span annotation layer | `residue.gemini_span` |
| DeepSeek | lenticular brackets around a dagger, `【85†L261-269】` | citation renderer | `residue.lenticular_citation` |
| Grok | `grok-card`, in `<grok-card data-id="..." data-type="citation_card">` | citation card component | `residue.grok_card` |
| Grok | `grok_render_citation_card_json` | citation card payload | `residue.grok_card` |
| Unclassified | the writing fence, `:::writing{variant="document" id="12345"}`, and its localised form `:::écriture{` | document container directive | `residue.writing_block` |
| Perplexity | `[attached_file:1]` | attachment reference | `residue.attached_file` |
| Perplexity | `[web:1]` | web result reference | `residue.web_ref` |
| Perplexity | `ppl-ai-file-upload` inside a storage URL | upload host | `residue.ppl_upload` |
| Several | `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `utm_source=perplexity.ai`, `utm_source=grok.com`, `utm_source=claude.ai` | link tracking parameter appended by the product | `residue.utm_source` |
| Several | `referrer=grok.com`, `referrer=chatgpt.com`, `referrer=openai.com`, `referrer=perplexity.ai` | referrer parameter in a copied link | `residue.referrer` |

One documented token is deliberately not scanned. The guide records `Example+1`
as ChatGPT residue, and it is too close to ordinary text to grep for without
generating noise. Leaving it out of the scanner and naming it here is the
honest handling: the inventory is the union of what is documented, and the
scanner is the subset that is safely decidable.

## Why these differ in kind from every other marker

An em dash is a feature of how someone writes. A tricolon is a feature of how
someone writes. Excess vocabulary is a distribution over how a population
writes. All three therefore have a false-positive class made of people:
typographers, essayists, speakers trained in rhetoric, writers who learned
English formally, anyone whose word processor substitutes characters on save.
`stowe-detector-bias` is the sharpest measurement of what that costs. Sixteen
detection models over student essays found English-language-learner essays
disproportionately flagged and non-White ELL students disproportionately
flagged relative to their White ELL peers, while human annotators looking at
the same essays showed no significant demographic bias. The bias is a property
of style-based automated judgment, and it lands on the same people every time.

A residue token has no such class, because no writing habit produces it. The
distinction is not that residue is stronger evidence of the same thing. It is
evidence of a different thing:

| | Style marker | Residue marker |
| --- | --- | --- |
| What it is | a property of prose | a property of a paste |
| Produced by | how a person writes | a rendering layer |
| Error class | writers with particular habits or training | documents that mention the token |
| Distribution | continuous, needs a threshold | binary, present or absent |
| Decays with model generation | yes, see [[Marker Cohort Rot]] | only when a vendor changes its renderer |
| May hard-fail a document | never | yes, by scanner exit code |
| Handled by | [[Evidence Tiers]] | `scripts/scan_residue.py` |

`sun-idiosyncrasies` marks the far edge of what style can do. Five-way model
attribution reached 97.1 percent accuracy across ChatGPT, Claude, Grok, Gemini
and DeepSeek, and the signal survived rewriting, translation and
summarization, published at ICML 2025. That is an extremely strong stylistic
result and it is still a probability over a distribution, with 2.9 percent
landing somewhere. A residue token is not a probability. Either the string is
in the file or it is not, and `grep` settles it.

## The one real false positive

There is exactly one, and this note is an instance of it: text that discusses
the markers rather than carrying them. It has three sub-forms.

1. **Documentation of the markers**, like this page, the scanner's own module
   docstring, and its unit tests.
2. **Quoted output**, where someone pastes a transcript into a bug report,
   support ticket, or research note precisely so the residue can be examined.
3. **Analytics and log material**, where `utm_source` values appear as data in
   a traffic report or a referrer breakdown.

All three are the mention-versus-use distinction, and the mitigation is
structural rather than probabilistic: `scripts/scan_residue.py` is markdown
fence aware and inline-code aware, so matches inside fenced code blocks and
inline code spans are skipped unless `--include-code` is passed. Every token in
the table above sits inside backticks for that reason, and the vault scans
clean against its own scanner.

The exception to the exception: a match that lands inside a URL is always
reported, fenced or not. A fenced block is not a licence to ship a tracking
parameter, because the URL will still be clicked.

## What the token licenses, and what it does not

`wikipedia-signs-of-ai-writing` describes the E3 family as an unambiguous
indicator that the text originated with AI. This brain does not repeat that
inference, and the difference is worth being precise about rather than
hand-waving past.

What the token establishes: the string was emitted by a product's rendering
layer and pasted into this document without cleaning. That is a fact about a
string, and it is as close to certain as anything in this field gets.

What the token does not establish: who wrote the sentences around it. A
researcher quoting a model's answer, an author pasting a retrieved citation
into their own paragraph, and a document generated end to end all leave the
same token. The guide itself concedes the narrower version of this for the
tracking parameters, noting that while `utm_source` near-definitively proves a
particular product's involvement, it does not prove on its own that the same
product generated the writing.

So the finding is a mechanical defect with a location, never a verdict.
Removing `[cite: 1]` from a sentence is correct regardless of who wrote the
sentence, and rule 1 of [[The Firewall]] is not suspended just because the
evidence happens to be strong. Strong evidence for the wrong proposition is
still the wrong proposition.

## Handling

1. Run `python3 scripts/scan_residue.py` over the document. Record the rule
   ids, line numbers, and exit code.
2. Delete the token. Do not paraphrase it, escape it, or wrap it in
   punctuation, all of which leave the string in the file.
3. Check what the token was standing in for. A `[cite: 4]` marker was pointing
   at a source, so removing it silently drops the attribution. Route the
   sentence to [[The Attribution Test]] before the paragraph is considered
   repaired.
4. For `utm_source` and `referrer` hits, strip the query parameter and confirm
   the bare URL still resolves. Some products only serve the tracked form, in
   which case the link needs replacing rather than trimming.
5. Re-run the scanner and record the new exit code. The exit code is the gate,
   not anybody's opinion that the fix worked.
6. If the token appeared in material intended as a quotation, move it inside a
   fenced block rather than deleting it, and note why in the surrounding text.

## Related

- [[Evidence Tiers]]
- [[The Firewall]]
- [[The Attribution Test]]
- [[Marker Cohort Rot]]
- [[Model Fingerprints]]
- [[Why Detection Fails]]
- [[Detector Bias Against Language Learners]]
- [[Content Provenance]]
- [[Agent Output Surface]]
- [[index|Index]]
