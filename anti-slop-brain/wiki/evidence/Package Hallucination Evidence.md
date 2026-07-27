---
type: "concept"
title: "Package Hallucination Evidence"
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
  - "[[Dependency Surface]]"
  - "[[The Generation Verification Asymmetry]]"
  - "[[Code Surface]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Marker Cohort Rot]]"
  - "[[Superseded Figures]]"
  - "[[Documentation Surface]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall]]"
  - "[[Corpus Study Method]]"
source_urls:
  - "https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf"
  - "https://arxiv.org/abs/2605.17062"
  - "https://arxiv.org/abs/2606.28438"
---

# Package Hallucination Evidence

A hallucinated dependency is the rarest thing in this vault: a defect that is
fully decidable. The name resolves in a registry or it does not, and no
judgement enters anywhere. That property is what makes the evidence here worth
assembling carefully, and it is also what makes the argument in this note
survive a rate that dropped by an order of magnitude.

## What the 2024 cohort measured

`spracklen-package-hallucination` was published at USENIX Security 2025, which
puts it at the top of the evidence rungs used in [[Evidence Quality Ladder]].
It sampled **16 models across 576,000 code-generation samples** and counted the
recommended package names that did not exist.

- **19.7 percent** of recommended packages did not exist, averaged across all
  models.
- **205,474 unique hallucinated names** were observed.
- **5.2 percent** for commercial models against **21.7 percent** for open-source
  models, a spread of roughly four to one.

The unique-name count is the figure that describes the problem's shape. A 19.7
percent rate tells you how often a developer meets a bad suggestion. Two hundred
thousand distinct names tells you how large the registrable namespace is that an
attacker could pre-position in, and those are different quantities serving
different arguments.

## Repetition is the load-bearing number

The rate and the name count together still would not make this an attack. What
makes it one is that the same wrong names come back.

The same study found that **43 percent of hallucinations recurred across all ten
reruns of the same prompt**, and **58 percent recurred more than once**. A name
that surfaces once is noise, worth nothing to anyone. A name that surfaces in
every rerun of a common prompt is a **channel**: an attacker registers it once
and waits.

This is why slopsquatting differs from classic typosquatting in kind rather than
degree. A typosquatter has to guess what a human will mistype. A slopsquatter
does not have to guess at all, because the model publishes the target list
repeatedly, identically, and for free. The reconnaissance step of the attack is
performed by the defender's own tooling.

## The 2026 compression

`churilov-package-hallucination-2026` measured the current cohort and found the
rate collapsed.

| Cohort | Rate | Scale | Ledger id |
| --- | --- | --- | --- |
| 2024, all 16 models | 19.7 percent | 576,000 samples | `spracklen-package-hallucination` |
| 2024, commercial subset | 5.2 percent | same study | `spracklen-package-hallucination` |
| 2024, open-source subset | 21.7 percent | same study | `spracklen-package-hallucination` |
| 2026 frontier range | 4.62 to 6.10 percent | corroborated across 199,845 responses | `churilov-package-hallucination-2026` |
| Claude Haiku 4.5 | 4.62 percent | same study | `churilov-package-hallucination-2026` |
| GPT-5.4-mini | 6.10 percent | same study | `churilov-package-hallucination-2026` |

Two things changed and both are real improvements. The rate fell by roughly an
order of magnitude from the 2024 average, and the four-to-one spread between
commercial and open-source families compressed to a band barely 1.5 points wide.
The corroboration from Socket across **199,845 responses** on 2026-07-22 matters
because it is an independent measurement of the same quantity, which is rarer in
this domain than it should be.

One thing did not change. **53 hallucinated package names remained registerable
at time of measurement.** That is the number the gate is built around, and it is
not a rate.

The 2026 source is a preprint verified at abstract level, capped at `medium`
confidence and tier CONTESTED under [[Evidence Tiers]]. The 2024 source is
peer-reviewed at a top-tier security venue and is tier EVIDENCE-BASED. Quoting
19.7 percent as a current figure is a cohort error of exactly the kind
[[Marker Cohort Rot]] exists to prevent, and it belongs in the same category as
the corrections logged in [[Superseded Figures]]. Quote it as the 2024 cohort
measurement it is, paired with the 2026 range.

## Why the gate survives the rate drop

The instinct after an order-of-magnitude improvement is to relax the control.
The instinct is wrong here, and the reason is arithmetic rather than caution.

Consider the two sides of the exchange:

| Side | Unit of work | Cost per unit | How many units |
| --- | --- | --- | --- |
| Attacker | register one hallucinated name | one registration, near zero | 1 |
| Defender | verify one dependency in one change | one registry lookup, milliseconds | every dependency in every change, forever |
| Attacker payoff | arbitrary code execution on install | whatever the payload reaches | unbounded |
| Defender loss if the check is skipped once | same | same | 1 is enough |

The attacker pays once and the defender pays continuously, but the defender's
per-unit cost is a cached index lookup while the attacker's payoff is the
contents of a developer machine and everything the build can reach. A control
whose cost is bounded and small, protecting against a loss that is unbounded,
does not get removed because incidence fell. The rate governs how often the gate
fires. It does not govern whether the gate should exist.

There is a second reason, specific to this vault. The dependency check is the
cleanest worked example of [[The Generation Verification Asymmetry]] running the
**favourable** direction. Generating a plausible package name is free, and
verifying one is nearly free as well. Almost everything else in this brain deals
with the unfavourable direction, where a claim is cheap to produce and expensive
to check, and where the model's confidence is worth nothing. When verification
is cheap, automate it and stop reasoning about it.

That also rules out the tempting shortcut. Asking a model whether a package
exists reintroduces judgement into a decidable check, and
`song-rubber-stamp-regime` reports that model-based self-review gates drift into
a regime where acceptance scores rise while correctness falls. The gate consults
a registry, not a model. See [[The Firewall]] for the general rule and
[[Dependency Surface]] for the scanner's definition.

## Quoting these figures correctly

1. Attach a cohort year to every rate. "19.7 percent" without "2024 models" is a
   false current claim.
2. Pair the 2024 figure with the 2026 range whenever it appears, in the same
   sentence or the adjacent one.
3. Keep the **rate** and the **registerable-name count** apart. They answer
   different questions and only the second one justifies the gate.
4. State the verification tier: peer-reviewed for `spracklen-package-hallucination`,
   abstract-level preprint for `churilov-package-hallucination-2026`.
5. Never present a per-model number as a durable property. Haiku 4.5 at 4.62
   percent is a measurement of one release, and the next release resets it.
6. Do not extend any of this to prose. These figures describe package names in
   generated code, and nothing here supports a claim about text.

## What is still unmeasured

- **No figure in this ledger counts actual slopsquat installs.** Everything
  above measures the availability of the attack, not its exploitation.
- **No study covers install commands inside documentation**, though a fabricated
  install line in a README is executed by a human just as readily as one in a
  script. [[Documentation Surface]] treats that as in scope on reasoning, not on
  measurement.
- **No independent replication of the 53-name count** exists in the ledger. It
  is a single-source figure from a preprint and is marked as such.
- **No breakdown by ecosystem** for the 2026 cohort, so whether the compression
  is uniform across PyPI, npm, and the rest is unknown.

Recording these is not a hedge. A note that lists what it does not know can be
extended by the next person; one that reads as complete gets treated as
finished. [[Corpus Study Method]] holds the general standard.

## Related

- [[Dependency Surface]]
- [[Code Surface]]
- [[The Generation Verification Asymmetry]]
- [[Evidence Quality Ladder]]
- [[Marker Cohort Rot]]
- [[Superseded Figures]]
- [[Documentation Surface]]
- [[Evidence Tiers]]
- [[The Firewall]]
- [[Note Conventions]]
