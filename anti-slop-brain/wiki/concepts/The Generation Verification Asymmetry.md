---
type: "concept"
title: "The Generation Verification Asymmetry"
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
  - "[[Workslop]]"
  - "[[Constraint Beats Coaxing]]"
  - "[[Package Hallucination Evidence|Slopsquatting]]"
  - "[[The Attribution Test|Fabricated Citations]]"
  - "[[The Attribution Test|Attribution Test]]"
  - "[[Code Surface]]"
  - "[[Package Hallucination Evidence|Package Hallucination Rates]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
source_urls:
  - "https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf"
  - "https://arxiv.org/abs/2605.17062"
  - "https://www.betterup.com/workslop"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2507.09089"
---

# The Generation Verification Asymmetry

Every other note in this folder is a symptom. This one is the engine. Producing
a plausible sentence, citation, function, package import or status update now
costs close to nothing. Establishing that any one of them is true still costs
what it always cost: a human, or a network call, or a build. The gap between
those two costs is not a nuisance. It is the thing that decides what tooling is
worth building.

## Statement

For a given artifact, let G be the marginal cost of producing something that
passes casual inspection and V be the marginal cost of establishing whether it
is correct. Generative systems have driven G toward zero across every surface
this vault covers. They have not moved V at all, because V is bounded by the
external world: the registry either has the package or it does not, the DOI
either resolves to the cited title or it does not, the reviewer either has the
hour or does not.

Two consequences follow immediately and neither is intuitive.

The first is that the cost of a defect is displaced onto whoever receives it.
The producer pays G. The receiver pays V, and pays it whether the artifact was
correct or not, because the only way to learn which case you are in is to run
the check.

The second is that any defence which itself relies on generation is spending
the cheap resource on the expensive problem. This is why the vault's hard gates
are deterministic scripts rather than model calls, a design rule argued out in
[[Constraint Beats Coaxing]] and stated as policy in [[The Firewall]].

## The cost ledger

| Artifact | What generating it costs now | What verifying it costs | Measured evidence |
| --- | --- | --- | --- |
| A package import | one token in a code block | one registry lookup, cheap and fully decidable | 19.7 percent of recommended packages did not exist across 16 models and 576,000 samples, 205,474 unique fake names (`spracklen-package-hallucination`) |
| A citation with a DOI | one line of text | one resolver call plus a title match, decidable | fabricated references, invalid DOIs and ISBNs, and DOIs pointing at unrelated papers are a documented taxonomy (`wikipedia-signs-of-ai-writing`) |
| A paragraph of analysis | seconds | a reader who knows the domain, minutes to hours, not decidable | human annotators flag slop spans at 0.34 versus 0.03 to 0.08 for models (`shaib-measuring-slop`) |
| A status update or handoff doc | seconds | roughly two hours per incident, borne by the recipient | `betterup-workslop` |
| A pull request in a mature repo | minutes | 19 percent longer task completion time for experienced developers | `metr-developer-slowdown` |

The rows are ordered by decidability, not by severity, and that ordering is the
whole architecture. Rows one and two are checkable by a script with no model in
the loop, so they become hard gates. Rows three to five are not, so they become
structural procedures that produce a written artifact a human can audit. See
[[Evidence Tiers]] for how a signal is assigned to a row.

## Case one: slopsquatting economics

Package hallucination is the cleanest instance because both sides of the
asymmetry are quantified.

On the generation side, the 2024 cohort hallucinated at 19.7 percent averaged
across 16 models, with commercial models at 5.2 percent against 21.7 percent
for open-source models (`spracklen-package-hallucination`). The 2026 frontier
cohort compressed hard, to a range of 4.62 percent to 6.10 percent, with Claude
Haiku 4.5 at 4.62 percent and GPT-5.4-mini at 6.10 percent
(`churilov-package-hallucination-2026`, a preprint verified at abstract level).
The 19.7 percent figure must therefore be quoted as a 2024-cohort number, never
as current.

The improvement does not close the attack, and this is the part that gets
missed. Two properties keep it open.

**Repetition.** 43 percent of hallucinations recurred across all ten reruns of
the same prompt and 58 percent recurred more than once
(`spracklen-package-hallucination`). A hallucinated name is not noise. It is a
stable, predictable target an attacker can enumerate by simply running the
model.

**Availability.** 53 hallucinated package names remained registerable at the
time of measurement in 2026 (`churilov-package-hallucination-2026`).

So the attacker's cost is one registration. The defender's cost, absent
tooling, is a developer noticing an unfamiliar import during review. Cutting
hallucination rates by a factor of four changes the volume of the attack
surface and changes nothing about its economics. That is why
[[Package Hallucination Evidence|Slopsquatting]] is gated by a registry lookup in [[Code Surface]] rather than
by asking a reviewer to be vigilant, and why the residual rate matters less
than the fact that verification is one cheap deterministic call.

## Case two: workslop and the displaced hour

The same asymmetry in an office. BetterUp Labs with the Stanford Social Media
Lab surveyed 1,150 United States desk workers and found 40 percent had received
workslop in the prior month, that roughly 15 percent of received content
qualified, and that each incident took about two hours to resolve
(`betterup-workslop`). These are self-reported survey estimates and are treated
as such throughout; the fuller accounting and its limitations are in
[[Workslop]].

Read the two-hour figure as a price. The sender spent a minute on G. The
receiver spent two hours on V, reconstructing what the sender meant, checking
what was asserted, and often redoing the work. Nothing about the transaction
required the content to be wrong. The receiver pays the two hours to find out.

This is the exact shape Willison's original behavioural definition of slop was
pointing at, and it is why [[AI Slop]] keeps imposed cost as a downstream
consequence rather than a definitional condition.

## Why this produces scanners instead of better prompts

If V is expensive and G is free, then the only defences that scale are the ones
where V happens to be cheap. There are not many, and they are worth enumerating
because they are the entire deterministic layer:

1. **Existence checks.** Does this package exist in its registry. Does this DOI
   resolve. Does this URL return something. One network call, no judgment.
2. **Title matching.** Does the resolved DOI's title match the cited title. A
   string comparison over an authoritative response.
3. **Literal pattern presence.** Vendor residue tokens and placeholder strings
   are grep targets with no false-positive class worth arguing about.
4. **House-style violations.** Banned characters and tokens are decidable by
   definition, because the house defines them. This is explicitly a style rule
   and never a slop verdict.

Everything outside that list falls back to a human, and the vault's job there
is not to replace the human but to spend their attention well: route them to
the specific span, hand them the specific question, and require a written
artifact. That is what [[The Attribution Test|Attribution Test]] and the rest of the procedures
folder are for.

## Where the asymmetry reverses

Honesty requires the counter-case. V is not always the expensive side.

- For a claim with a machine-readable ground truth, verification is cheaper
  than careful generation. This is the whole basis of the deterministic layer.
- For a text whose only defect is stylistic, there is no V at all, because
  there is nothing to be wrong about. Treating style as a defect to be verified
  is a category error, and it is the mistake catalogued in
  [[Signs Are Not The Problem]].
- For an artifact nobody will ever read, both sides are zero and the correct
  intervention is to stop producing it rather than to check it.

## Related

- [[AI Slop]]
- [[Workslop]]
- [[Constraint Beats Coaxing]]
- [[Signs Are Not The Problem]]
- [[Package Hallucination Evidence|Slopsquatting]]
- [[The Attribution Test|Fabricated Citations]]
- [[Package Hallucination Evidence|Package Hallucination Rates]]
- [[The Attribution Test|Attribution Test]]
- [[Code Surface]]
- [[The Firewall]]
- [[Evidence Tiers]]
