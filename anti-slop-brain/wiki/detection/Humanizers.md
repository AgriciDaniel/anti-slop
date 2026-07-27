---
type: "concept"
title: "Humanizers"
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
  - "[[Signs Are Not The Problem]]"
  - "[[Why Detection Fails]]"
  - "[[Watermarking]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Constraint Beats Coaxing]]"
  - "[[Prose Surface]]"
  - "[[The Deletion Test]]"
  - "[[Excess Vocabulary]]"
  - "[[The Em Dash]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2605.19516"
  - "https://arxiv.org/abs/2604.22142"
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://arxiv.org/abs/2509.19163"
---

# Humanizers

The tools in this category promise to make generated text read as human. The
best-measured thing they actually do is make it worse. That finding comes from
an awkward place, and this note is organised around reading the awkwardness
correctly rather than around the tools themselves.

## The paper and its conflict

`masrour-damage-humanizers` was published at GenAIDetect, COLING 2025, so it is
peer reviewed. It was also written by employees of Pangram, a company that sells
an AI-text detector. Under the ledger's fifth downgrade rule, a vendor selling a
product that a finding would sell more of has that conflict recorded, and the
entry records it.

A blanket discount would be lazy, because the paper makes two claims that point
in opposite commercial directions. Treating them identically throws away the
information the conflict actually gives you.

| Claim in the paper | Direction of author interest | How this vault treats it |
| --- | --- | --- |
| Humanizer tools successfully evade text detectors | supports the argument that buyers need a better detector | discounted; convenient findings from interested parties are weak |
| SynthID-Text true positive rate falling 87.6 to 5.4 percent after DIPPER paraphrase | same direction, watermarks look inadequate | discounted, and carried in [[Watermarking]] with the conflict attached |
| "All humanizers tend to degrade the quality of the original text" | cuts against interest; it says the customer's problem is smaller than feared | strengthened; a finding published against incentive is worth more |
| Documented failure modes: hallucinated citations, comment leakage, nonsensical strings | against interest, for the same reason | strengthened |

A result that an author had a reason not to publish is stronger than the same
result from a disinterested party, because the incentive to suppress it was
present and it was published anyway. [[Evidence Quality Ladder]] states the
general rule; this is the case that most clearly requires it.

## The degradation numbers

The paper's fluency comparison judged humanized text against the original it was
derived from. The humanized version won:

- **26.0 percent** of the time for the best tier of tools,
- **14.67 percent** for the medium tier,
- **2.67 percent** for the worst tier.

Read the worst-tier figure carefully. A 2.67 percent win rate is not a tool that
sometimes helps and sometimes does not. It is a tool that reliably damages the
text it is pointed at, and it is being sold as an improvement. Even the best
tier loses roughly three comparisons out of four.

The three named failure modes matter more than the rates for anyone deciding
whether to run one of these tools over a real document:

1. **Hallucinated citations.** A rewriting pass that invents a reference has
   introduced a factual defect where none existed. This is strictly worse than
   the stylistic problem it was hired to fix.
2. **Comment leakage.** Instructions, meta-commentary, or the tool's own notes
   surviving into the output. The vendor residue taxonomy in
   `wikipedia-signs-of-ai-writing` catalogues the same class of artifact.
3. **Nonsensical strings.** Output that is not text in any register.

## The paraphrase tradeoff, quantified

`xu-base-models-look-human`, a Carnegie Mellon preprint verified at abstract
level, measured what iterative paraphrasing buys and what it costs. Detector
evasion succeeds completely: text reaches **100 percent human probability by
round 10**. Meaning does not survive the trip. Semantic preservation collapses
from a starting band of **99 to 100** down to a range of **33 to 99**.

The lower bound is the number to hold onto. A document can come out of that
process retaining a third of its meaning while scoring perfectly on the metric
the process was optimising. That is the exact shape of Goodhart's problem, and
it is why [[Signs Are Not The Problem]] is doctrine here rather than advice.

## Voice does not survive revision either

`vannuenen-voice-under-revision` looked at 300 personal narratives across three
models and found that LLM revision decreases function words, contractions, and
first-person pronouns while increasing vocabulary diversity and word length.
Two details make it load-bearing:

- The shift **persists under explicit instructions to preserve the author's
  voice**. Asking nicely does not work, which is the empirical core of
  [[Constraint Beats Coaxing]].
- Rewritten texts **converge in feature space regardless of where they
  started**. Two authors with different styles come out closer together than
  they went in.

So the humanizer proposition inverts. A tool that rewrites text to look less
machine-produced is a tool that moves every text it touches toward a common
point, which is the mechanism described in [[Distributional Convergence]]. It
is manufacturing the defect it claims to remove.

## What the prior art actually does

`blader-humanizer` is the most widely used open implementation, MIT licensed,
at version 2.9.1 as of 2026-07-22, with 33 patterns derived from the Wikipedia
signs guide. It is a fair specimen of the category's design assumptions:

- no severity system, no confidence system, no per-pattern weights;
- a no-fabrication rule that is a prompt instruction with no verification
  mechanism behind it;
- no coverage of fabricated citations, vendor residue markers, or code;
- a section that bans en dashes outright, which breaks legitimate numeric and
  date ranges;
- a runtime prompt that itself contains an em dash, violating its own stated
  hard constraint.

The last two are not cheap shots. They show what happens when a marker list is
promoted to a rule without a procedure behind it: the rule fires on correct
usage and fails to fire on its own author. [[The Em Dash]] and
[[Excess Vocabulary]] are held as routing signals here for exactly this reason.

The source that most of this field derives from says so directly.
`wikipedia-signs-of-ai-writing` warns in bold that the listed patterns are only
potential signs of a problem rather than the problem itself, and that treating
the signs as the things to fix could just make detection harder.

## The gap, stated rather than filled

No peer-reviewed study in this ledger measures commercial humanizer output with
**human raters** or against standard writing rubrics, and none **counts factual
errors introduced** by a humanizing pass. The DAMAGE fluency figures come from
GPT-4o acting as judge, and `shaib-measuring-slop` reports that model judges
agree with human slop labels at close to zero kappa, so a model-judged fluency
comparison is a weaker instrument than it looks.

What that gap means in practice:

1. Treat "humanizers degrade quality" as a **direction**, well supported, and
   not as a calibrated magnitude.
2. Do not quote the 26.0, 14.67, and 2.67 percent figures as human judgements.
   They are model judgements, and the sentence that quotes them should say so.
3. Treat the hallucinated-citation failure mode as the highest-severity finding
   in the note, because it is the one that converts a style problem into a
   correctness problem.
4. If you need a magnitude for a decision, commission the human evaluation
   rather than inferring one. Nothing here supports a number.

## Why this brain is not one

Repair here is limited to spans a structural procedure convicted, and the
artifact of conviction is kept. A padded paragraph that fails
[[The Deletion Test]] gets cut, and the record shows what was lost. Nothing runs
a whole-document rewrite as a first move, which is precisely what a humanizer
is. See [[Prose Surface]] for how this constrains editing, and
[[What This Brain Does Not Claim]] for the limits admitted up front.

## Related

- [[Signs Are Not The Problem]]
- [[Why Detection Fails]]
- [[Watermarking]]
- [[Evidence Quality Ladder]]
- [[Constraint Beats Coaxing]]
- [[Distributional Convergence]]
- [[Prose Surface]]
- [[The Deletion Test]]
- [[The Em Dash]]
- [[Excess Vocabulary]]
- [[Note Conventions]]
