---
type: "procedure"
title: "The Firewall"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/procedure"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Why Structural Not Judgmental]]"
  - "[[The Deletion Test]]"
  - "[[The Inversion Test]]"
  - "[[The Stranger Test]]"
  - "[[The Attribution Test]]"
  - "[[The Load Bearing Test]]"
  - "[[Evidence Tiers]]"
  - "[[Detector Bias Against Language Learners]]"
  - "[[Why Detection Fails]]"
  - "[[Note Conventions]]"
source_urls:
  - "https://arxiv.org/abs/2512.09292"
  - "https://doi.org/10.1016/j.patter.2023.100779"
  - "https://arxiv.org/abs/2606.29540"
  - "https://arxiv.org/abs/2606.28438"
  - "https://arxiv.org/abs/2509.19163"
---

# The Firewall

Four rules sit between every signal this brain can observe and every action it
is allowed to take. They are constraints, not advice. A procedure that breaks
one of them is not a weaker procedure, it is a different and worse product: a
detector. This brain is not a detector, and [[Why Detection Fails]] is the
reason.

Each rule below states what is forbidden, what is permitted instead, and the
evidence that forced it. The rules are ordered by how much damage breaking them
does, worst first.

## Rule 1: never emit an authorship verdict

Forbidden: any output of the form "this was written by a model", "this looks
AI-generated", a percentage likelihood of machine authorship, or a score that a
reader could reasonably read as one.

Permitted instead: a named defect with a location, a severity, a confidence,
and the artifact that convicted it. "The second paragraph survives deletion
with no loss of information" is a defect report. "The second paragraph reads
like ChatGPT" is a verdict.

The evidence is `stowe-detector-bias`, published at ACL 2026 and peer
reviewed. Sixteen detection models were run over student essays labelled for
gender, race and ethnicity, English-language-learner status, and socioeconomic
status. English-language-learner essays were disproportionately flagged, and
non-White ELL students were disproportionately flagged relative to their White
ELL peers. The finding that matters most for this rule is the control: human
annotators looking at the same essays showed no significant demographic bias.
The bias is a property of automated authorship judgment, not of the essays.

This supersedes the 2023 result the field usually quotes,
`liang-gpt-detectors-biased`, which found seven detectors misclassifying 61.3
percent of TOEFL essays as AI-generated with 19.8 percent flagged unanimously.
That study rests on 91 essays written before 2020, and the sample size must be
stated whenever the figure is used. Both papers point the same way. The 2026
one points there with a demographic breakdown and a human control.

The practical consequence: an authorship verdict has a victim and a defect
report does not. A false "this is padded" costs the author an argument. A false
"this is machine-written" costs a student a grade. See
[[Detector Bias Against Language Learners]] for the full treatment.

## Rule 2: never hard-fail on a stylistic marker alone

Forbidden: a marker count crossing a threshold and blocking a merge, a
publication, or a review. No em-dash density, no tricolon rate, no word from a
banned list, no burstiness measure may on its own decide anything.

Permitted instead: the marker routes to a structural procedure. The marker is a
reason to look, and the procedure is the thing allowed to convict. See
[[Evidence Tiers]] for the tiering that governs which markers may route where.

The evidence is `czuma-em-dash-prevalence`, pre-registered on OSF as HFT8C over
69,632 medRxiv preprints. Em-dash prevalence in Discussion sections rose from
4.23 percent before ChatGPT to 11.58 percent after, a rise of 7.35 points with
a 95 percent confidence interval of 6.94 to 7.77 and an odds ratio of 2.96. The
trajectory runs at roughly 4 percent through 2023, 8.0 percent in 2024, and
20.3 percent in 2025. A placebo split inside the pre-LLM era moved 0.13 points,
which is the control that makes the main result readable.

That is a large, well-controlled, pre-registered effect. It is also useless as
a per-document decision rule, and the author says so. This brain adopts the
conclusion verbatim: the em-dash is a population-level indicator, not a
per-paper detector of LLM use. A signal can be real at the level of 69,632
papers and carry almost no information about the paper in front of you.

Rule 2 and Rule 1 fail together. Marker-based hard failure is authorship
detection with extra steps, and it inherits the demographic bias in
`liang-gpt-detectors-biased` because marker density correlates with writing
that was learned formally rather than acquired natively.

## Rule 3: severity is impact, confidence is certainty

Forbidden: one number. A single score collapses "I am sure this is trivial"
and "I suspect this is catastrophic" into the same output, and a reader cannot
recover which one you meant.

Permitted instead: two axes, always reported together, never multiplied.

### Severity: what it costs if the finding is real

| Severity | Definition | Example |
| --- | --- | --- |
| `critical` | The artifact is wrong or unsafe if shipped. Someone downstream acts on a falsehood. | A citation that resolves to a real paper making the opposite claim. A package import that does not exist. |
| `high` | A load-bearing claim or construct is unsupported. The artifact survives but its argument does not. | "Studies show" with no resolvable study. A test with no assertion gating a release. |
| `medium` | Reader cost with no factual harm. Time is wasted, nothing is false. | A paragraph that deletes with no loss. A docstring restating the signature. |
| `low` | House style only. | An em dash in a repository that bans them. |

### Confidence: how certain the finding is

| Confidence | Definition | What produced it |
| --- | --- | --- |
| `confirmed` | A deterministic check fired, or a structural test produced an artifact that is not arguable. | A scanner exit code. A deleted span whose named loss is empty. A build that broke. |
| `probable` | A structural test produced an artifact, but a competent reader could name a loss that the test missed. | A deletion whose loss is rhythm or onboarding rather than information. |
| `possible` | Only a stylistic marker fired. No procedure has been run. | Tier 2 or Tier 3 signals from [[Evidence Tiers]]. |

### The combination rule

A `possible` finding never hard-fails, at any severity. That is the whole point
of separating the axes: a suspected critical defect is a reason to run a
procedure, not a reason to block. `critical` plus `confirmed` may block.
Everything else reports.

The reason `possible` is capped is `shaib-measuring-slop`, which measured
GPT-5 span-level slop extraction at precision 0.14 and recall 0.11. Roughly six
in seven model-nominated spans are not what the model says they are. A finding
sourced from model suspicion alone cannot be promoted above `possible` without
an artifact, because the underlying operation is barely better than chance.

## Rule 4: never let the model gate its own rewrite

Forbidden: the model that produced or repaired a span deciding whether the
repair worked. No self-approval, no "I have verified the fix", no confidence
statement standing in for a re-run.

Permitted instead: the deterministic scanners re-run after every repair, and
the structural procedure that convicted the span re-runs against the new text.
The gate is the scanner exit code, not the model's opinion of the scanner exit
code.

The evidence is `song-rubber-stamp-regime`, which measured AI self-review gates
for code entering what the authors call a rubber-stamp regime: acceptance
scores rise while benchmark correctness falls. The two curves separate. That is
precisely the failure a self-gating repair loop would produce, and the loop
would report success the whole way down. This source is a 2026 preprint
verified at abstract level only, tiered `CONTESTED`, and this note does not
claim more for it than that. It is also the only rule here whose evidence is
contested, which is why the note carries `practitioner` confidence rather than
`evidence-based`.

The independent argument for Rule 4 does not depend on that preprint at all,
and it is in [[Why Structural Not Judgmental]]: a judge that is no more
accurate than the thing it judges cannot be debiased into usefulness.

## Where each rule is enforced

| Rule | Enforcement point | Failure mode if it is only a prompt |
| --- | --- | --- |
| 1 | Output schema has no authorship field, so a verdict has nowhere to go | Verdicts leak into free-text summary |
| 2 | Markers carry a tier and a routing target, never an exit code | Threshold creeps into a linter and becomes policy |
| 3 | Two required fields, no derived total | Reviewers invent a combined score downstream |
| 4 | Scanners re-run on the repaired file, exit code is the gate | Repair loop declares victory against itself |

Rules stated as standing constraints survive context compaction. Rules stated
as numbered steps in a checklist do not. Every skill surface in this project
states these four as constraints in its first section for that reason.

## What the firewall costs

It is worth being honest about the price. The firewall makes this brain unable
to answer the question most people actually want answered, which is "did a
model write this". It will refuse that question permanently. It also makes the
output slower to read, because two axes are harder to sort than one, and it
makes some real defects unreportable when no procedure can produce an artifact
for them. Those are accepted losses. The alternative is a tool whose errors
land on the same people every time.

## Related

- [[Why Structural Not Judgmental]]
- [[The Deletion Test]]
- [[The Attribution Test]]
- [[The Load Bearing Test]]
- [[Evidence Tiers]]
- [[Why Detection Fails]]
- [[Detector Bias Against Language Learners]]
- [[The Em Dash|Em Dash Population Prevalence]]
- [[Marker Cohort Rot]]
- [[Note Conventions]]
