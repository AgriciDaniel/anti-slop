# Market Research

Status: researched. Last verification pass 2026-07-27.

## Buyer Hypothesis

Writers, engineers, and agent operators who ship AI-assisted work and need a
defensible, source-cited way to find and fix substance defects without
accusing anyone of using AI.

## Why The Need Is Real

The cost is measured, not assumed. A survey of 1,150 United States desk
workers found 40 percent received low-substance AI output in the prior month,
each incident taking roughly two hours to resolve, at an estimated 186 dollars
per employee per month. Source betterup-workslop, retrieved 2026-07-27,
confidence medium because the figures are self-reported survey estimates
rather than controlled measurement.

The demand for a defensible method rather than a detector is also evidenced.
Detectors are unreliable and their failures fall on identifiable groups: 16
detection models disproportionately flagged English-language-learner essays,
and non-White ELL students more than White ELL peers, while human annotators
showed no significant demographic bias. Source stowe-detector-bias, ACL 2026,
retrieved 2026-07-27.

## Competitive Position

| Prior art | What it does | What it lacks | Source |
|---|---|---|---|
| blader/humanizer v2.9.1 | 33 surface patterns, strong packaging | citations, residue markers, code, severity, confidence | blader-humanizer |
| Wikipedia signs guide | The definitive taxonomy, descriptive | not executable, not packaged, wiki-specific | wikipedia-signs-of-ai-writing |
| Commercial detectors | An origin verdict | accuracy, explainability, demographic fairness | stowe-detector-bias |
| Commercial humanizers | Detector evasion | they measurably degrade the text they edit | masrour-damage-humanizers |

The gap this product fills is the one Wikipedia names itself: the signs are not
the problem, and a tool that removes the signs while leaving unverified claims
in place has made the situation worse rather than better.

## Evidence Log

| Evidence | Source | Retrieved | Confidence | Notes |
|---|---|---:|---|---|
| Downstream cost is measurable | betterup-workslop | 2026-07-27 | medium | Self-reported survey |
| Detectors fail and are biased | stowe-detector-bias | 2026-07-27 | high | Peer reviewed, ACL 2026 |
| Humanizers degrade quality | masrour-damage-humanizers | 2026-07-27 | medium | Vendor authored, but against interest |
| Model judgment cannot substitute | shaib-measuring-slop | 2026-07-27 | high | Kappa near zero |
| Expert human review works | russell-expert-detectors | 2026-07-27 | high | One error in 300, ACL 2025 |
| The category is mainstream | merriam-webster-woty-2025 | 2026-07-27 | medium | Lexicographic, not empirical |

## Demand Questions And Answers

1. Who pays. Teams that ship AI-assisted prose or code and carry the review
   burden downstream.
2. What raw materials they already have. Drafts, diffs, commit messages, pull
   request descriptions, agent transcripts.
3. What output saves time. A findings report separating impact from certainty,
   with a verifiable artifact behind every finding.
4. What brings them back. Marker cohorts rot on a 30 day cycle, so the refresh
   loop is structural rather than manufactured.

## Honest Limits On This Research

No primary market sizing was performed. The buyer hypothesis rests on measured
downstream cost and on the documented failure of the alternatives. That is
evidence the problem exists. It is not evidence that a given number of people
will pay for this specific solution, and the distinction is recorded here
rather than smoothed over.
