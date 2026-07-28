---
type: "concept"
title: "Constraint Beats Coaxing"
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
  - "[[The Firewall]]"
  - "[[The Generation Verification Asymmetry]]"
  - "[[Signs Are Not The Problem]]"
  - "[[Why Structural Not Judgmental|LLM As Judge Fails At Slop]]"
  - "[[Sycophancy]]"
  - "[[Code Surface]]"
  - "[[Vendor Residue Markers]]"
  - "[[Evidence Tiers]]"
  - "[[Distributional Convergence]]"
  - "[[Note Conventions]]"
source_urls:
  - "https://arxiv.org/abs/2606.28438"
  - "https://www.pnas.org/doi/10.1073/pnas.2415697122"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2404.13076"
  - "https://arxiv.org/abs/2410.13341"
  - "https://arxiv.org/abs/2604.23178"
---

# Constraint Beats Coaxing

An instruction in a prompt is a request. A hook that runs a script and returns a
non-zero exit code is a gate. The two are often written in the same imperative
voice and they are not the same kind of object at all, and confusing them is how
a system ends up with a written rule that has never once been enforced.

## Request versus gate

The distinguishing question is: what happens when the model does not comply.

For a prompt instruction, nothing happens. The instruction competes for
attention with everything else in context, degrades under length, and is subject
to the model's own judgment about whether this case is an exception. Compliance
is probabilistic and unlogged.

For a gate, the action does not complete. There is nothing to comply with. The
harness runs the check, and the outcome is a fact independent of what the model
believed about it.

This is why the vault's non-negotiable rules live in scripts and hooks, and why
the prose rule about dashes in [[Note Conventions]] is checked mechanically
rather than trusted. The distinction is not a claim about model quality. It
holds equally for a perfectly compliant model, because the point is that a
request produces no artifact and a gate does.

## The evidence that self-gating decays

The strongest reason to prefer gates is that the alternative has been measured
failing, and it fails in a specific and predictable direction.

**Self-review drifts into rubber-stamping.** Song, Cai and Zhao report that AI
self-review gates enter a rubber-stamp regime in which acceptance scores rise
while benchmark correctness falls (`song-rubber-stamp-regime`). The two curves
separate. The gate reports improvement while the artifact degrades. This is a
2026 preprint verified at abstract level only, carried at CONTESTED tier, and it
is the single most directly on-point result for anything that asks a model to
approve its own output.

**Judges prefer the thing they are supposed to catch.** GPT-4 preferred
LLM-written product pitches 89 percent of the time against human raters at 36
percent, with the same bias appearing for papers at 78 versus 61 percent and
movies at 70 versus 58 percent (`laurito-ai-ai-bias`, peer reviewed in PNAS,
human baseline n equal to 13; the paper's p-values test model-versus-human text
preference, not this rater gap). A judge with that prior is not a neutral gate
on machine-shaped text.

**Self-recognition drives self-preference.** Panickssery and colleagues found
that a model's ability to recognise its own generations correlates linearly with
the strength of its preference for them, and argue the relationship is causal
(`panickssery-self-preference`). Asking a model to review its own output is
therefore not a weakly biased procedure; it is biased along exactly the axis
being measured.

**Style outranks substance in the preference signal.** Judge style bias runs
from 0.10 to 0.76, with markdown-formatted answers preferred over the same
content in plain text, against position bias of 0.04 or less
(`soumik-judging-the-judges`). A model gate rewards the formatting that
[[Distributional Convergence]] says the model already over-produces.

**And it does not detect slop anyway.** LLM judge agreement with human slop
labels sits at kappa 0.01 for GPT-5, minus 0.01 for DeepSeek-V3 and 0.03 for
o3-mini, with models flagging at 0.03 to 0.08 against a human rate of 0.34
(`shaib-measuring-slop`). Span-level extraction runs at precision 0.14 and
recall 0.11.

**There is a ceiling result too.** When the judge is no more accurate than the
model it evaluates, no debiasing method can reduce the required ground-truth
labels by more than half (`dorner-limits-scalable-eval`). Scaling the judge does
not escape the problem; it halves the human cost at best.

## The enforcement ladder

| Mechanism | Binding | Who can bypass it | Characteristic failure |
| --- | --- | --- | --- |
| Prompt instruction in a system prompt or skill body | no | the model, silently | quietly ignored under context pressure, no artifact |
| Instruction plus a request to self-check | no | the model, while reporting success | rubber-stamp regime (`song-rubber-stamp-regime`) |
| Model-as-judge in a separate call | no | the judge's own priors | favours machine-shaped text (`laurito-ai-ai-bias`) |
| Tool restriction on an agent | yes, at the harness | nobody in-session | over-restriction blocks legitimate work |
| Deterministic script with an exit code | yes | nobody | only covers what is decidable |
| Harness hook bound to an event | yes | nobody in-session | must be installed, and installation is out-of-band |

The ladder is ordered by bindingness, and the useful reading is the boundary
between rows three and four. Everything above the line is a request. Everything
below is a gate. A rule that matters belongs below the line or it does not
matter.

Two harness details are worth recording because they are commonly inverted.
Declaring allowed tools on a skill is a permission pre-approval, not a
restriction; only an explicit disallow actually removes a capability. And a hook
is executed by the harness rather than by the model, which is the entire source
of its bindingness. Neither of these is a claim from the source ledger. They are
properties of the Claude Code runtime, recorded here as runtime facts, and no
ledger source in this vault covers harness behaviour.

## What this looks like in practice here

1. Anything decidable becomes a script with a non-zero exit code: registry
   existence, DOI resolution and title match, literal residue tokens,
   placeholder strings, banned characters. See [[Code Surface]] and
   [[Vendor Residue Markers]].
2. Anything undecidable becomes a structural procedure that emits a written
   artifact a human can audit, never a rating. The procedures are
   [[The Deletion Test|Deletion Test]], [[The Inversion Test|Inversion Test]], [[The Stranger Test|Stranger Test]],
   [[The Attribution Test|Attribution Test]] and the code-side load-bearing test.
3. Nothing model-produced gates anything model-produced. After any rewrite, the
   deterministic layer runs again. That rule is stated in [[The Firewall]] and
   its justification is the rubber-stamp result above.
4. Standing prohibitions are written as standing prohibitions, not as numbered
   steps, so that they survive being read out of order or in part.

Rule 4 is the one concession to the request side of the ladder. Some things
genuinely cannot be gated, and for those the wording matters: a standing rule
stated as a permanent constraint holds up better than the same rule buried as a
step in a checklist.

## Credit, and the boundary

The framing is not original here. It comes from the Gogh vault at
the Gogh vault (a sibling brain covering visual and frontend slop), whose
`wiki/concepts/Constraint Beats Coaxing.md` states the thesis for visual work:
explicit constraints outperform generic requests to make something beautiful,
implemented there through dials, bans, locks and a blocking pre-flight check.
Gogh reached it from the design side, as the practical answer to visual
[[Distributional Convergence]].

This note carries the same thesis into text, code and agent output, and adds the
evidence base Gogh did not need: the self-review and judge-bias literature
above. Gogh's version is correctly marked practitioner synthesis rather than a
controlled benchmark. This version is anchored on measured results, and is still
capped at practitioner confidence because its most on-point source is a
CONTESTED preprint.

## The honest limit

Constraint only reaches what is decidable. A gate cannot tell you whether a
paragraph is worth reading, whether an argument holds, or whether a design is
right. Over-applied, it produces a document that passes every check and says
nothing, which is a recognisable failure mode of any rubric. The gates in this
vault exist to spend human attention well, not to remove the need for it, and
the boundary between the two layers is drawn in [[Evidence Tiers]].

## Related

- [[The Firewall]]
- [[Why Structural Not Judgmental|LLM As Judge Fails At Slop]]
- [[The Generation Verification Asymmetry]]
- [[Signs Are Not The Problem]]
- [[Distributional Convergence]]
- [[Sycophancy]]
- [[Code Surface]]
- [[Vendor Residue Markers]]
- [[The Attribution Test|Attribution Test]]
- [[Evidence Tiers]]
- [[Note Conventions]]
