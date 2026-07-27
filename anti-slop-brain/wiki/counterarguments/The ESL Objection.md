---
type: "concept"
title: "The ESL Objection"
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
  - "[[Detector Bias Against Language Learners]]"
  - "[[Why Detection Fails]]"
  - "[[Human Expert Review]]"
  - "[[Evidence Tiers]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Moving Baseline Objection]]"
  - "[[The Accessibility Objection]]"
  - "[[What This Brain Does Not Claim]]"
source_urls:
  - "https://arxiv.org/abs/2512.09292"
  - "https://doi.org/10.1016/j.patter.2023.100779"
  - "https://arxiv.org/abs/2409.01754"
  - "https://arxiv.org/abs/2501.15654"
---

# The ESL Objection

Of every argument against this field, one is strong enough that the honest
response is not a rebuttal. It is a concession, followed by a change to the
product. This note records the concession and names the three things that
changed because of it.

## The objection put at full strength

Someone who learned English in a classroom writes English that was taught: even
register, explicit connectives, complete clauses, cautious modality, the
academic voice that textbooks reward. A model trained on published prose emits
the same register for the same reason. Any system that reasons from surface
features toward machine involvement is therefore reading a proxy for formal
instruction and calling it a proxy for generation. The people it misreads are
the people with the least standing to appeal, in the language they are being
penalised for having learned deliberately. A tool that gets this wrong does not
produce a small distributed error. It produces a concentrated one, aimed.

That argument is correct. What follows is where the ledger supports it, where
it does not, and what the support obliges.

## What the evidence licenses the objection to say

| # | Premise of the objection | Ledger support | Strength of that support |
| --- | --- | --- | --- |
| 1 | Detectors flag English-language-learner writing more often | `stowe-detector-bias` | 16 detection models, peer reviewed at ACL 2026 |
| 2 | The disparity compounds with race, not just ELL status | `stowe-detector-bias` | non-White ELL students flagged more than White ELL peers |
| 3 | Human readers do not reproduce the bias | `stowe-detector-bias` | control condition, no significant demographic bias |
| 4 | The problem was documented years before it was acted on | `liang-gpt-detectors-biased` | 61.3 percent of TOEFL essays flagged, n equals 91, 7 detectors, essays predate 2020 |
| 5 | The formal register being penalised is a taught register | none found | reasoning, not evidence; no ledger source measures this |

Row 4 carries a standing condition. The 61.3 percent figure may not appear in
this vault without its sample size of 91 essays, because ninety-one items place
a wide interval around a headline percentage and the detector cohort is now
several model generations old. Row 5 is the one this brain wants most and
cannot have. It is stated as reasoning and marked as such.

Row 3 is the load-bearing row. Without it, a defender of detection can argue
that the essays genuinely resembled machine output and that any careful reader
would have erred the same way. Careful readers did not. That closes the escape
route and moves the fault from the writing to the instrument.

## Why concede rather than qualify

A qualification keeps the feature and adds a warning. The warning is read once
and the feature is used daily, which means a qualified detector is an
unqualified detector with better paperwork. The costs are also not symmetric.

| Error | Who absorbs it | Recoverable |
| --- | --- | --- |
| False "this paragraph is unsupported" | the author, who argues the point | yes, by producing the source |
| False "this paragraph was machine-written" | the writer, in a disciplinary process | rarely, and not by evidence they control |

The right column decides it. A defect report is a claim about an artifact that
a third party can check without trusting the tool. An origin verdict is a claim
about a person that nobody can check at all, including the accused. That
asymmetry is what makes concession cheaper than qualification: giving up the
verdict costs this brain a feature, and keeping it costs somebody else a grade.

## The three things that changed

**Rule 1 removed the field, not the wording.** The firewall's first rule
forbids any output that a reader could take as a machine-authorship claim, and
it is enforced by the output schema having nowhere to put one rather than by an
instruction not to write one. Instructions survive until the first context
compaction. Missing fields survive indefinitely. The full rule set is in
[[The Firewall]], and the study behind it is worked through in
[[Detector Bias Against Language Learners]].

**No marker may hard-fail.** Every stylistic signal in [[Evidence Tiers]] is a
routing decision toward a structural procedure, and no tier licenses a block on
its own. This matters specifically for the ESL case because the markers whose
density rises with formal instruction are exactly the ones a naive threshold
would catch: hedging, connective density, tricolon rate, even punctuation. A
threshold on any of them is authorship detection wearing a linter's clothes,
and it inherits the demographic skew measured in `stowe-detector-bias` without
inheriting the paper's caveats.

**Baselines are per author, never per population.** This is the change that is
least visible and does the most work.

## Population baseline against per-author calibration

| Question | A population baseline answers | A per-author baseline answers |
| --- | --- | --- |
| What is being compared | this text against a corpus average | this text against the same person's earlier text |
| Whose register sets the reference | the corpus majority | the author |
| What a deviation means | this writer is unusual | this writer changed |
| Effect of a taught formal register | permanent offset, flagged forever | absorbed into the baseline, invisible |
| Effect of vocabulary drift in the wider language | reference moves under the writer | both sides move together |
| What it can conclude about origin | it invites the inference | nothing, and it is not asked to |

A learner writing careful academic English sits far from a population mean on
every pass, forever, and nothing they do resolves it. The same learner compared
against their own last five documents sits at the centre of their own
distribution, and the only thing that registers is a change. That is the whole
mechanism: the offset that the population comparison mistakes for evidence is
constant per author, so it cancels.

Drift is the second reason. `yakura-spoken-convergence` measured words
preferentially generated by ChatGPT rising in spontaneous human speech, with
delve up 48 percent, realm up 35 percent and adept up 51 percent within 18
months of release, across a corpus of more than 740,000 hours of podcast and
academic video audio, and a preregistered experiment with n equal to 496
confirming entrenchment in active vocabulary. That source is a preprint
verified at abstract level and its corpus arm infers rather than isolates
causation. Even read conservatively it means a fixed population reference is
drifting under everyone, which is the subject of
[[The Moving Baseline Objection]] and the reason [[Marker Cohort Rot]] is a
standing maintenance obligation rather than a one-off cleanup.

## Running a per-author calibration

1. Collect at least five prior documents by the same author in the same genre,
   written before the period under review. Fewer than five is a sample, not a
   baseline, and should be labelled as such.
2. Measure only structural quantities on that set: claims per paragraph,
   proportion of claims that resolve to a named source, citation resolution
   rate, spans surviving [[The Deletion Test]] with no named loss.
3. Do not measure stylistic markers into the baseline. They are the quantities
   contaminated by register, and folding them in reintroduces the bias the
   calibration exists to remove.
4. Record the baseline with its date and document count. It expires as the
   author's work changes; treat anything older than the author's last major
   role change as stale.
5. Compare the new document against that baseline and report deltas, not
   absolute positions.
6. If a delta exceeds the author's own range, run the structural procedure it
   routes to and report the procedure's artifact. The delta is never the
   finding.
7. If no prior documents exist, there is no baseline. Fall back to artifact
   checks that need no reference class at all: do the references resolve, do
   the sources say what is claimed, do the numbers reconcile.

Step 7 is the honest floor. For a first-time author this brain has no
calibration and says so, rather than substituting a population comparison and
calling it one.

## What the concession does not license

It does not follow that markers are worthless. It follows that markers may
point and may not decide, which is a narrower claim than the objection's
strongest form and the one the evidence actually supports.

It also does not follow that nothing can be assessed. `russell-expert-detectors`
found that a majority vote of five expert annotators misclassified 1 of 300
articles, outperforming commercial and open-source detectors even under
paraphrase evasion. Careful humans remain the best available instrument, which
is the argument in [[Human Expert Review]]. This brain declines to build the
automated version of that instrument, for the reasons in
[[Why Detection Fails]], and confines itself to defects a reader can verify.

## Related

- [[The Firewall]]
- [[Detector Bias Against Language Learners]]
- [[Why Detection Fails]]
- [[Human Expert Review]]
- [[Evidence Tiers]]
- [[Marker Cohort Rot]]
- [[The Moving Baseline Objection]]
- [[The Accessibility Objection]]
- [[What This Brain Does Not Claim]]
- [[The Deletion Test]]
- [[Superseded Figures]]
