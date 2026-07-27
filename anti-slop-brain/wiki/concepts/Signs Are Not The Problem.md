---
type: "concept"
title: "Signs Are Not The Problem"
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
  - "[[AI Slop]]"
  - "[[Distributional Convergence]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[The Inversion Test|Inversion Test]]"
  - "[[The Stranger Test|Stranger Test]]"
  - "[[The Attribution Test|Attribution Test]]"
  - "[[The Attribution Test|Fabricated Citations]]"
  - "[[Vendor Residue Markers]]"
  - "[[Humanizers|Humanizers Degrade Quality]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2604.22142"
  - "https://arxiv.org/abs/2605.19516"
  - "https://github.com/blader/humanizer"
---

# Signs Are Not The Problem

This is the doctrine note. Everything else in the vault is downstream of it,
and a single sentence from the community guide that most marker lists are
copied from states it better than any restatement:

> The patterns listed here are also only potential **signs** of a problem, not
> **the problem itself**. Please do not merely treat these signs as the problems
> to be fixed; that could just make detection harder.

That is the boldfaced warning in Wikipedia:Signs of AI writing
(`wikipedia-signs-of-ai-writing`, retrieved 2026-07-27, a living community
guide that changes continuously). It is quoted here in full because the tools
built from that guide almost universally ignore it, and because it names the
failure mode with precision: not merely useless, actively counterproductive.

## The trap, stated mechanically

A sign S co-occurs with a defect D. A tool removes S. Two cases follow.

**Case one: D was never present.** The text was fine, S was a stylistic
coincidence, and the edit is a net loss of the author's voice for no benefit.
The cost is small per instance and compounding across a document.

**Case two: D was present.** D is still present. What has changed is that the
cheapest available cue for finding D has been destroyed. The document is now
defective and harder to triage. Every subsequent reader spends more to reach the
same finding.

There is no case in which removing S repairs D, because S was never D. The
guide's phrase "could just make detection harder" is describing case two, and
case two is where the harm concentrates: fabricated citations, unsupported
synthesis and hollow analysis all survive a surface edit intact.

## The separation this vault enforces

| Surface sign | Defect it may co-occur with | What removing the sign accomplishes | What actually repairs the defect |
| --- | --- | --- | --- |
| Excess stylistic vocabulary | none by itself; the excess is verbs and adjectives, not content | flattens the prose, changes no claim | nothing to repair unless a claim fails a test |
| Tricolons and negative parallelism | rhetorical shape standing in for an argument | the shape goes, the empty argument stays | [[The Inversion Test|Inversion Test]] on the claim inside the shape |
| Hedging and over-attribution | a claim with no resolvable source | reads more confident, is now confidently unsourced | [[The Attribution Test|Attribution Test]], resolve to a named source or cut |
| Generic authority phrasing | analysis anyone could have written without the source | text sounds specific, is not | [[The Stranger Test|Stranger Test]], name the fact only the worker would know |
| Em dash density | nothing decidable at document level | breaks legitimate punctuation | not a defect; see [[The Em Dash|Em Dash Density]] |
| Vendor residue tokens | a real, literal artifact of a paste | this one genuinely is the defect | delete it, and this is a hard gate |
| A citation with a DOI | the DOI may resolve to nothing or to an unrelated paper | hiding it makes it unfindable | resolve it, match the title, see [[The Attribution Test|Fabricated Citations]] |

Read the right-hand column downward. Only two rows are ones where the visible
thing is the actual thing: vendor residue and, partially, citations. Those two
are exactly the classes the guide documents in its own taxonomies, covering
markup residue such as `oaicite`, bracketed cite tokens, `grok-card` and
`utm_source` tracking parameters, and citation defects including fabricated
references, invalid DOIs and ISBNs, and DOIs that point at unrelated papers
(`wikipedia-signs-of-ai-writing`). They are also, not coincidentally, exactly
the classes that surface-editing tools tend to omit entirely.

## Two measured failure modes

The doctrine would be an assertion if it were not for two results that measure
the damage.

**Humanizers degrade the text.** The DAMAGE study states plainly that all
humanizers tend to degrade the quality of the original text, and quantifies it:
in fluency comparisons against the original, best-tier tools won 26.0 percent of
the time, medium tier 14.67 percent, worst tier 2.67 percent
(`masrour-damage-humanizers`). Documented failure modes include hallucinated
citations, comment leakage and nonsensical strings. So the tool that removes the
signs is capable of adding a fabricated citation, which is one of the defects
the signs were pointing at.

That source has a conflict of interest worth stating rather than hiding: it was
authored by employees of a company selling a detector, and the finding that
humanizers evade detection serves that interest. The finding that humanizers
degrade quality does not, which is why the ledger raises confidence in the
degradation result specifically and why this note leans on that half.

**Revision flattens voice even when told not to.** Van Nuenen measured LLM
revision across 300 personal narratives and three models
(`vannuenen-voice-under-revision`). Function words, contractions and
first-person pronouns fall. Vocabulary diversity and word length rise. Rewritten
texts converge in feature space regardless of their starting point. Critically,
the shift persists under explicit instructions to preserve the author's voice.

Put those together and the picture is not neutral. Passing text through a model
to remove signs costs voice reliably, may introduce new defects, and by
construction cannot fix the defects the signs indicated. See
[[Distributional Convergence]] for why the flattening direction is a property of
the process rather than a fixable prompt failure.

There is a third result worth carrying as an outer bound. Xu and colleagues
found that iterative paraphrasing reaches 100 percent human probability under a
detector by round ten, while semantic preservation collapses from a 99 to 100
range down to a 33 to 99 range (`xu-base-models-look-human`, preprint verified
at abstract level). Perfect evasion is achievable. It costs the meaning.

## What this rules out, by name

The best-packaged prior art in this space, `blader/humanizer` v2.9.1, enumerates
33 patterns derived directly from the Wikipedia guide and has no coverage of
fabricated citations, vendor residue markers, or code
(`blader-humanizer`, snapshot 2026-07-27; the repository changes continuously).
Its no-fabrication rule is a prompt instruction with no verification mechanism,
it has no severity or confidence system, and its own runtime prompt contains an
em dash in violation of its stated hard constraint.

The distribution discipline of that project is worth copying. Its substance is
what this note exists to reject. A tool that removes the 33 signs and leaves the
citations unchecked has implemented case two of the trap above, at scale, with a
persuasive interface.

The doctrine therefore produces four standing rules, enforced elsewhere:

1. A marker never fails a build alone. It routes to a procedure.
   ([[Evidence Tiers]])
2. A repair is only a repair if it changed a claim, a citation, a structure or a
   fact. Style-only edits are recorded as style edits.
3. Anything decidable is decided by a script, not by a rewrite.
   ([[Vendor Residue Markers]], [[The Attribution Test|Fabricated Citations]])
4. No output ever states or implies who wrote the text. ([[The Firewall]])

## Related

- [[AI Slop]]
- [[Evidence Tiers]]
- [[The Firewall]]
- [[Distributional Convergence]]
- [[Humanizers|Humanizers Degrade Quality]]
- [[The Attribution Test|Fabricated Citations]]
- [[Vendor Residue Markers]]
- [[The Deletion Test|Deletion Test]]
- [[The Inversion Test|Inversion Test]]
- [[The Stranger Test|Stranger Test]]
- [[The Attribution Test|Attribution Test]]
- [[The Em Dash|Em Dash Density]]
