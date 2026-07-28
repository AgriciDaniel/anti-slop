---
type: "concept"
title: "Workslop"
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
  - "[[The Generation Verification Asymmetry]]"
  - "[[AI Slop]]"
  - "[[Documentation Surface]]"
  - "[[Commit and Review Surface|Pull Request Descriptions]]"
  - "[[Commit and Review Surface|Commit Messages]]"
  - "[[Agent Output Surface|Chat And Agent Output]]"
  - "[[The Stranger Test|Stranger Test]]"
  - "[[The Deletion Test|Deletion Test]]"
  - "[[The Code Slop Disagreement|METR Developer Slowdown]]"
  - "[[Evidence Tiers]]"
source_urls:
  - "https://www.betterup.com/workslop"
  - "https://arxiv.org/abs/2507.09089"
  - "https://arxiv.org/abs/2509.19163"
  - "https://arxiv.org/abs/2507.00788"
---

# Workslop

Workslop is the office-internal case: content produced with a generative tool
and sent to a colleague, which looks like completed work and turns out to
contain none. The term is useful precisely because it names a transfer rather
than a text. The document is not the harm. The handoff is.

## The coinage and the study behind it

The term was introduced in a Harvard Business Review piece published
2025-09-22, reporting research by BetterUp Labs with the Stanford Social Media
Lab (`betterup-workslop`). The survey covered 1,150 United States desk workers
and was fielded in September 2025. The HBR article body sits behind a paywall,
so the figures used here were confirmed against BetterUp's own page.

That last detail is a citation-hygiene point, not a footnote. The figures are
being read from the organisation that produced the research and benefits from
its circulation. The rule from [[Note Conventions]] applies: the URL supports
what was said, not whether it is right.

## The published figures

| Figure | Value | What it is a measure of |
| --- | --- | --- |
| Desk workers who received workslop in the prior month | 40 percent | reach, self-reported |
| Share of received content qualifying as workslop | roughly 15 percent | density, self-reported |
| Time to resolve one incident | about two hours | recipient cost, self-estimated |
| Cost per employee per month | 186 United States dollars | derived from the above |
| Annual cost at 10,000 employees | about 9 million United States dollars | extrapolated |

The two money figures do not reconcile under naive multiplication: 186 dollars
per employee per month across 10,000 employees would be roughly 22 million
dollars a year, not 9 million. They do reconcile if the 186 dollars is applied
only to the 40 percent who reported receiving workslop, which yields
approximately 8.9 million. That reconciliation is arithmetic performed here,
not a published methodology, and it is offered as the most likely reading
rather than as a source claim. Anyone quoting the 9 million figure should quote
the population assumption with it.

## The downstream-cost framing

The reason to keep this concept separate from general prose slop is that it
isolates a specific accounting error organisations make.

When a task is completed with a generative tool in one tenth of the time, the
saving is visible, attributable, and lands on the sender's ledger. The two
hours the recipient spends reconstructing what was meant is invisible,
unattributed, and lands on someone else's ledger. Aggregate productivity can
fall while every individual reports a gain, and nobody in the chain is lying.

This is [[The Generation Verification Asymmetry]] instantiated inside an
organisation, and it is the same structure as the perception gap measured in
software work: allowing AI increased task completion time by 19 percent for
experienced developers on mature repositories, while those developers forecast
a 24 percent speedup and still estimated a 20 percent speedup after the fact
(`metr-developer-slowdown`). Sixteen developers and 246 tasks is a small
sample, and the study's own follow-up could not obtain a clean signal because
developers increasingly refused to work without AI. But the direction of the
error, self-report showing gain where measurement showed loss, is the same
direction the workslop numbers depend on.

## Reading the survey honestly

These are self-reported survey estimates, not controlled measurement. Every
number in the table above inherits that. Specifically:

1. **Reach is a recall estimate.** "Received workslop in the prior month"
   depends on the respondent noticing, remembering, and classifying. It is
   plausibly under-reported for subtle cases and over-reported for salient ones.
2. **The two hours is a self-estimate of time spent, not a measurement.**
   Time-on-task self-report is a well-known weak instrument, and the METR result
   above is evidence in this exact domain that practitioners misestimate their
   own time in the presence of AI tooling.
3. **Classification is unblinded.** Respondents knew the survey was about
   AI-generated content when they classified what they had received. There is
   no reported control condition of equivalently vague human-written work.
4. **No causal claim is available.** The design cannot separate workslop from
   the pre-existing baseline of vague, padded, or low-effort colleague output.
5. **The comparison this needs does not exist in the ledger.** A pre-registered
   design with an unassisted control is what would settle it. The closest
   methodological model in this vault's evidence base is the pre-registered null
   result on code maintainability (`borg-null-result`, a preprint, 151
   participants, In Principle Acceptance before data collection), whose
   pre-registered Phase 2 found no significant differences in subsequent code
   evolution, completion time or quality, and whose observational Phase 1 found a
   30.7 percent median reduction in completion time. That is
   a different question on a different surface, and it is cited here only as the
   standard of evidence the workslop survey does not meet.

The conclusion is not that workslop is fictional. The conclusion is that its
magnitude is unestablished and its existence is well attested.

## What a recipient can actually do

Because the defect is in the handoff, the intervention belongs at the receiving
end, and it is a routing decision rather than a judgment.

1. Apply [[The Stranger Test|Stranger Test]] to the document. Name one fact in it that only
   someone who did the work could know. If nothing qualifies, the document did
   not transfer any work.
2. Apply [[The Deletion Test|Deletion Test]] to each section. Cut it, state what was lost. Sections
   that lose nothing are the padding the two hours is being spent on.
3. Return the specific missing item, not a verdict about the document. Asking
   "which build did you see this on" is actionable. Saying "this reads like AI"
   is an authorship verdict, which [[The Firewall]] forbids and which is also
   unfalsifiable across a desk.
4. Where the surface has a structure, use it. Handoff artifacts are covered
   individually in [[Commit and Review Surface|Pull Request Descriptions]], [[Commit and Review Surface|Commit Messages]] and
   [[Documentation Surface]], each of which has cheaper checks available than
   general prose does.

Step 3 is the whole discipline. The measured failure of holistic slop judgment
(`shaib-measuring-slop`, where LLM judges agree with human labels at kappa 0.01
to 0.03) applies to humans in an organisational setting for a different reason:
not that people cannot tell, but that the accusation cannot be resolved and the
missing fact can.

## Related

- [[The Generation Verification Asymmetry]]
- [[AI Slop]]
- [[The Stranger Test|Stranger Test]]
- [[The Deletion Test|Deletion Test]]
- [[Documentation Surface]]
- [[Commit and Review Surface|Pull Request Descriptions]]
- [[Commit and Review Surface|Commit Messages]]
- [[Agent Output Surface|Chat And Agent Output]]
- [[The Code Slop Disagreement|METR Developer Slowdown]]
- [[The Code Slop Disagreement|Borg Null Result]]
- [[The Firewall]]
- [[Evidence Tiers]]
