---
type: "procedure"
title: "Why Structural Not Judgmental"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/procedure"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[The Firewall]]"
  - "Measuring AI Slop in Text"
  - "AI-AI Evaluator Bias"
  - "[[Why Detection Fails]]"
  - "[[The Deletion Test]]"
  - "[[The Inversion Test]]"
  - "[[The Stranger Test]]"
  - "[[Distributional Convergence]]"
  - "[[Evidence Tiers]]"
  - "[[Note Conventions]]"
source_urls:
  - "https://arxiv.org/abs/2509.19163"
  - "https://www.pnas.org/doi/10.1073/pnas.2415697122"
  - "https://arxiv.org/abs/2409.15268"
  - "https://arxiv.org/abs/2604.23178"
  - "https://arxiv.org/abs/2410.13341"
  - "https://arxiv.org/abs/2404.13076"
  - "https://arxiv.org/abs/2501.15654"
  - "https://arxiv.org/abs/2605.19936"
---

# Why Structural Not Judgmental

Everything in this brain is downstream of one number. If a model could look at
a paragraph and say reliably whether it was slop, the correct design would be a
prompt: show the model the text, ask the question, act on the answer. That
design is what almost every tool in this space ships. It does not work, and the
failure has been measured rather than argued.

## The measurement

`shaib-measuring-slop` put LLM judges against human slop annotations on a
labelled corpus and reported Cohen's kappa, the agreement statistic that
corrects for chance. Kappa of 0 means the judge and the human agree exactly as
often as two people flipping coins would.

| Judge | Kappa against human slop labels |
| --- | --- |
| GPT-5 | 0.01 |
| o3-mini | 0.03 |
| DeepSeek-V3 | minus 0.01 |

Three frontier models, three results indistinguishable from chance, one of them
on the wrong side of zero. This is not a calibration problem that a better
rubric fixes. There is no signal to calibrate.

Two further figures from the same source describe the shape of the failure.
Models flag slop at a rate of 0.03 to 0.08 where humans flag at 0.34, so they
under-flag by roughly five times: the judge's instinct is to approve. And at
span level, where the judge must point at the offending text rather than rate
the whole passage, GPT-5 runs at precision 0.14 and recall 0.11. A fine-tuned
Qwen-7B reaches 0.32 and 0.30, better by a factor of two and still wrong most
of the time.

That last pair is the one that kills the obvious workaround. "Ask the model to
show its work by quoting the bad span" does not rescue the method, because the
quoted span is wrong roughly six times out of seven.

## The judge is biased toward the thing it is judging

A near-zero kappa would already be enough. The bias evidence makes the design
question worse, because the errors are not random. They lean toward slop.

`laurito-ai-ai-bias`, peer reviewed in PNAS 122(31), ran the same items past
model judges and human raters. GPT-4 preferred LLM-written product pitches 89
percent of the time where human raters preferred them 36 percent of the time.
The gap replicates across domains: papers at 78 percent versus 61 percent, and
movies at 70 percent versus 58 percent.

Two caveats that an earlier version of this note dropped, and that matter more
than the headline. First, the human baseline is **n equal to 13 in total, six
per dataset**, and the authors write that the findings are not definitive. This
brain imposes a standing rule that Liang's n equals 91 must travel with its 61.3
percent figure; the same rule applies here, and applies harder. Second, the
paper's p-values, including the p below 10 to the minus 16 figures for the
product and movie experiments and P equal to 0.001 for papers, test whether
**model selectors prefer model-written text over human-written text**. They do
not test the human-rater-versus-model-rater gap that the percentages above
describe. That comparison carries no significance test in the paper, so none is
quoted here. See AI-AI Evaluator Bias.

`feuer-style-over-substance`, published at ICLR 2025, isolates what the
preference tracks. Judge preferences do not correlate with factuality or with
safety measures. The judge is responding to something, and that something is
not whether the text is true.

`soumik-judging-the-judges` puts a number on the something. Style bias ranges
from 0.10 to 0.76, with markdown-formatted answers preferred over the same
content in plain text, against a position bias of 0.04 or less. Verbosity bias
turns out to be model-family specific rather than universal: Gemini and Llama
run plus 0.24 to plus 0.44, Claude runs minus 0.12, GPT-4o minus 0.04. This
source is tiered medium confidence and is corroborating rather than
load-bearing here, but the direction is consistent with the peer-reviewed work.

`panickssery-self-preference` supplies the mechanism. A model's ability to
recognise its own generations correlates linearly with the strength of its
preference for them, and the authors argue the relationship is causal. The
judge is not neutral about the defendant.

Put the four together and the position is not "the judge is noisy". It is: the
judge is at chance on the target, and its systematic error favours heavy
formatting, confident register, and text that a model produced. Those are the
defining surface features of slop. Asking that judge to find slop is asking a
thing to convict its own aesthetic.

## Adding judges does not fix it

The natural engineering response is an ensemble: several judges, a majority
vote, maybe a stronger judge auditing a weaker one. `dorner-limits-scalable-eval`,
also ICLR 2025, closes that route with a theoretical result. When the judge is
no more accurate than the model being evaluated, no debiasing method can reduce
the number of required ground-truth labels by more than half. You cannot
bootstrap reliable evaluation out of judges that are not better than the thing
they judge. The ground truth has to come from somewhere else.

Somewhere else, in this brain, is a mechanical operation whose result a person
can check without trusting anybody's judgment.

## What survives the argument

Two things survive, and they bound the design.

First, humans with the relevant experience are genuinely good at this.
`russell-expert-detectors`, ACL 2025, found that a majority vote of five expert
annotators misclassified 1 of 300 articles, outperforming commercial and
open-source detectors even under paraphrase evasion. Human review is not the
weak link. It is the strongest instrument available, and it is expensive, which
is the actual problem this brain is trying to solve.

Second, mechanical operations survive because they do not require a judgment at
all. "Delete this span and state what was lost" produces a deleted span and a
written loss. Another person can read both and disagree with the conclusion
while agreeing on the artifact. That is the property judgment lacks.

| Approach | What it outputs | Can a second person check it | Status here |
| --- | --- | --- | --- |
| Holistic rating | A number or a label | No, only agree or disagree | Forbidden by [[The Firewall]] |
| Model-nominated spans | A quoted span | Partly, but precision is 0.14 | Capped at `possible` confidence |
| Deterministic scanner | An exit code and a match location | Yes, deterministically | Allowed to hard-fail |
| Structural procedure | A named artifact | Yes, by re-running the operation | The core of this brain |

## The design rule that follows

Every procedure in `procedures/` obeys the same closing condition, and it is
the single sentence this brain would keep if it could keep only one:

> A procedure terminates in a verifiable artifact, never in a rating.

The artifacts, one per procedure: a deleted span plus the named loss
([[The Deletion Test]]), a written-out negation ([[The Inversion Test]]), a
named specific fact ([[The Stranger Test]]), a resolved or unresolvable
citation ([[The Attribution Test]]), and a broken or unbroken build
([[The Load Bearing Test]]).

Each artifact has the same useful property: it is wrong in a way you can see.
A rating is never wrong in a way you can see, which is why ratings are
comfortable and useless.

## Objections worth taking seriously

The premise that slop is self-evidently worse writing is not safe.
`miletic-lexical-diversity` looked at over 37,000 ACL Anthology papers and
found that LLM-modified text shows lower lexical diversity, which is the
expected slop signature, and that expert readers nonetheless rated the same
modified text as more understandable and more exciting. Lower diversity did not
mean worse reading. This is a preprint verified at abstract level, tiered
contested, and it complicates rather than refutes the case here. It is one
reason the procedures target information content and verifiability rather than
style, and it is why nothing in this brain treats [[Distributional Convergence]]
as automatically equivalent to harm.

The second honest limitation: the structural procedures have not themselves
been validated against a labelled corpus. They are principled, they produce
checkable artifacts, and no one has measured their inter-rater agreement. That
gap is recorded rather than papered over.

## Related

- [[The Firewall]]
- Measuring AI Slop in Text
- AI-AI Evaluator Bias
- [[The Deletion Test]]
- [[The Attribution Test]]
- [[The Load Bearing Test]]
- [[Why Detection Fails]]
- [[Evidence Tiers]]
- [[Distributional Convergence]]
- [[Humanizers|Humanizer Quality Degradation]]
