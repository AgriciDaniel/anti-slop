---
type: "concept"
title: "Evidence Quality Ladder"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/concept"
  - "#confidence/contested"
confidence: "contested"
related:
  - "[[Evidence Tiers]]"
  - "[[Superseded Figures]]"
  - "[[Why Pangram Is Not Cited]]"
  - "[[The Code Slop Disagreement]]"
  - "[[Humanizers|Humanizer Quality Degradation]]"
  - "[[The Em Dash|Em Dash Population Prevalence]]"
  - "[[Corpus Study Method]]"
  - "[[Note Conventions]]"
  - "[[Provenance Trace Policy]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://arxiv.org/abs/2507.00788"
  - "https://arxiv.org/abs/2606.29540"
  - "https://www.pangram.com/supporting-evidence"
  - "https://arxiv.org/abs/2501.03437"
  - "https://www.gitclear.com/the_ai_code_quality_maintainability_gap"
  - "https://arxiv.org/abs/2603.27006"
---

# Evidence Quality Ladder

Rank the source before reading the number. In a field where the loudest figures
come from companies selling the remedy, the ordering of evidence does more work
than any individual result.

## Five rungs

| Rung | Kind of source | What it buys | Ledger `confidence` ceiling |
| --- | --- | --- | --- |
| 1 | Pre-registered study with an analysis plan fixed before data | rules out outcome-driven analysis | high |
| 2 | Peer-reviewed publication | independent methodological review | high |
| 3 | Unrefereed preprint | a readable method, no external check | medium |
| 4 | Vendor report with published methodology | a real measurement with a stated interest | medium |
| 5 | Vendor marketing with no methodology | nothing quotable | low |

The rungs are not a ranking of how interesting a result is. They are a ranking
of how much of the result survives contact with someone who wants it to be
false.

Rungs 1 and 2 are independent axes that happen to be adjacent here.
borg-null-result is both, which is why it sits at the top of the code section.
czuma-em-dash-prevalence is rung 1 without rung 2: pre-registered on OSF as
HFT8C, still a preprint. That combination beats an unregistered peer-reviewed
paper on any question where the analyst had freedom to choose an outcome, and
loses to one on questions of technical correctness.

## Downgrade rules carried from the ledger

The ledger fixes five downgrades. They are applied at intake, not at citation
time, so a note cannot quietly promote a source by writing about it warmly.

1. Vendor study with no methodology or sample size: cap confidence at low and
   tier at CONTESTED.
2. Single-author unaffiliated preprint: cap confidence at medium and tier at
   CONTESTED.
3. Marketing page with no date and no citation: tier FOLKLORE, never quoted as
   a measured figure.
4. Preprint verified at abstract level only: cap tier at CONTESTED regardless
   of how strong the claim reads.
5. Vendor selling a product the finding would sell more of: record the conflict
   in the entry's limitations.

Rule 4 is the one that bites hardest in this domain. Most 2026 sources in the
ledger were verified at abstract level, which means the abstract's claim was
confirmed to exist and match the title, not that the tables were read. A brain
that treats abstract-level verification as full verification is producing
exactly the confident unsourced assertion it was built to catch.

## Worked application: a null result outranks a vendor chart

borg-null-result is a preprint, arXiv 2507.00788, not a published paper. Its
In-Principle Acceptance was granted at ICSME, and it carries no journal
reference. Across 151 participants, its pre-registered Phase 2 found no
significant differences in subsequent code evolution, completion time, or
quality between AI-assisted and unassisted development. In-Principle Acceptance
means the venue committed to accepting whatever came out. The null result could
not have been buried.

The null is Phase 2 only, and citing it alone is incomplete. Phase 1 of the same
study was observational and ran the opposite direction: a 30.7 percent median
reduction in completion time using an AI assistant, and an estimated 55.9
percent speedup for habitual AI users. Both phases are quoted together here or
not at all.

gitclear-maintainability-gap reports block duplication rising from 40.3 per
million changed lines in 2023 to 73.0 in 2026 year to date, a rise of 81
percent, across 623 million changes. That is a large sample and a stated method,
so it earns rung 4 rather than rung 5. But it is correlational, it has no
control group, and GitClear sells code-quality tooling, so downgrade rule 5
applies.

The ordering is not close. A pre-registered controlled comparison with a
committed publication venue outranks a correlational vendor time series no
matter how many lines the vendor counted. The ledger records the consequence as
an instruction: cite borg-null-result whenever vendor code-slop figures are
cited. [[The Code Slop Disagreement]] carries both sides in full.

## Worked application: pre-registration beats a marketing page

Both czuma-em-dash-prevalence and pangram-supporting-evidence make claims about
how often em dashes appear in human and machine text.

| Property | czuma-em-dash-prevalence | pangram-supporting-evidence |
| --- | --- | --- |
| Sample | 69,632 medRxiv preprints | not stated |
| Method | published, pre-registered OSF HFT8C | none published |
| Date | 2026-06-28 | none |
| Negative control | placebo split, plus 0.13 points | none |
| Internal consistency | one baseline | two conflicting human baselines |
| Stated limit | population indicator, not a per-paper detector | none |

The Pangram page is not merely weaker. It is unusable, because a page that
states both 2 and 5 as the human baseline has told you it does not know. It sits
at FOLKLORE in the ledger and is recorded so this brain can explain why it is
not used, never quoted as a measurement. The full argument is in
[[Why Pangram Is Not Cited]]; the specific figures are logged in
[[Superseded Figures]].

## Worked application: a finding against the author's own interest

masrour-damage-humanizers was written by Pangram employees, who sell a detector.
Downgrade rule 5 is triggered. But the rule asks which direction the interest
points, and this paper makes two distinct claims that point opposite ways.

- "Humanizer tools evade detectors" is commercially convenient for a detector
  vendor, since it argues the arms race needs their product. Treat it with the
  discount the rule implies.
- "All humanizers tend to degrade the quality of the original text" is not
  convenient. It argues the customer's problem is smaller than feared. The
  supporting numbers are a fluency win rate of humanized text against the
  original of 26.0 percent for best-tier tools, 14.67 percent medium, and 2.67
  percent worst, with documented failure modes including hallucinated citations,
  comment leakage, and nonsensical strings.

A finding that cuts against the author's commercial interest is stronger
evidence than the same finding from a disinterested party, because the incentive
to publish it was negative. The ledger records this reasoning in the entry's
limitations rather than leaving it to the reader. [[Humanizers|Humanizer Quality Degradation]]
is where the result is applied.

## Promotion is forbidden

A note inherits the weakest confidence of its sources. That is why this note is
tagged `contested`: it discusses pangram-supporting-evidence at `low` and
freeburg-last-fingerprint at `low`, and no amount of careful framing about
stronger sources changes the floor. The alternative, letting a note assert more
than its sources support, is the single most common way a knowledge base starts
lying to its own maintainers.

## Applying the ladder to a new claim

1. Identify the strongest source for the claim, not the first one found.
2. Place it on a rung and apply every downgrade rule that fires.
3. Ask which direction the author's interest points for this specific claim.
4. Ask whether a null result on this question would have been publishable.
5. Record the resulting confidence in the ledger entry before writing the note.
6. Write the note at or below that confidence, and mark single-source claims as
   single-source per [[Note Conventions]].

## Related

- [[Evidence Tiers]]
- [[Superseded Figures]]
- [[Why Pangram Is Not Cited]]
- [[The Code Slop Disagreement]]
- [[Humanizers|Humanizer Quality Degradation]]
- [[Corpus Study Method]]
- [[Note Conventions]]
- [[Provenance Trace Policy]]
- [[What This Brain Does Not Claim]]
