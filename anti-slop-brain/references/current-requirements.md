# Current Requirements

Status: researched. Last full verification pass 2026-07-27.

## Refresh Cadence

30 days for model-specific marker cohorts and detector claims. 90 days for
corpus studies and regulation. Before every release for any numeric claim.

## Required Source Standard

Use official, primary, vendor, standards-body, regulator, or API documentation
first. Record URL, retrieval date, version, deprecation or sunset notes, and
confidence. Every entry also carries an evidence tier so a vendor marketing
page can never be quoted as if it were a measured study.

Downgrade rules live in `references/source-ledger.json` under
`rules.downgrade_rules` and are applied on ingest, not at review time.

## Requirements That Bind The Product

| Requirement | Current state | Source | Retrieved | Confidence |
|---|---|---|---:|---|
| No holistic model judgment as a gate | Enforced by design; procedures must emit artifacts | shaib-measuring-slop | 2026-07-27 | high |
| No authorship verdict | Enforced by firewall rule 1 | stowe-detector-bias | 2026-07-27 | high |
| No hard fail on a stylistic marker | Enforced by firewall rule 2 | czuma-em-dash-prevalence | 2026-07-27 | high |
| No model self-gating of its own repair | Enforced by firewall rule 4 | song-rubber-stamp-regime | 2026-07-27 | medium |
| Dependency existence gate retained | Rates fell but the asymmetry persists | churilov-package-hallucination-2026 | 2026-07-27 | medium |
| Marker lists carry an expiry | Cohorts shift and the human baseline moves | yakura-spoken-convergence | 2026-07-27 | medium |

## Current Regulatory Position

EU AI Act Article 50 transparency duties apply from 2026-08-02 and were not
amended by the Digital Omnibus, which deferred high-risk deadlines only.
Generative systems already on the market before that date have until
2026-12-02 for the Article 50(2) machine-readable marking requirement.
Penalties reach 15 million euro or 3 percent of turnover. Source
eu-ai-act-article-50, retrieved 2026-07-27. That source is a consolidated
third-party rendering rather than the Official Journal text, so it is
confidence medium and must be checked against EUR-Lex before any compliance
advice is given.

Wikipedia has prohibited LLM-generated or LLM-rewritten article content since
its RfC closed 2026-03-20 by 44 to 2 under SNOW. It is a content guideline,
not a policy, and it carries two exceptions: copyediting your own writing, and
LLM-assisted translation, both under mandatory human review. Source
wikipedia-llm-guideline, retrieved 2026-07-27.

## Known Stale Or Superseded Requirements

| Superseded claim | Correct position | Source |
|---|---|---|
| Kobak prevalence of 10 to 30 percent | 13.5 percent minimum, up to 40 percent | kobak-excess-vocabulary |
| Package hallucination at 20 percent | 4.62 to 6.10 percent for 2026 models | churilov-package-hallucination-2026 |
| curl abandoned bug bounties permanently | Returned to HackerOne 2026-03-01, bounty free | stenberg-high-quality-chaos |
| GitClear churn of 7.1 percent | A discarded projection; the 2024 actual was 5.7 percent | gitclear-copilot-quality-2025 |

## Open Requirements Not Yet Satisfied

1. No peer-reviewed study measures commercial humanizer output with human
   raters or counts introduced factual errors. Recorded as a gap.
2. The Nature Author Correction to shumailov-model-collapse could not be read
   behind the publisher auth wall, so its scope is unverified.
3. The Springer-walled independent evaluation of Pangram could not be read.
