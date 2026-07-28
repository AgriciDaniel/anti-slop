<!--
Published copy of the adversarial verification pass that grounds this project.
The raw source snapshots it was built from are not redistributed here; the
Wikipedia wikitext is CC BY-SA 4.0 and is described in
anti-slop-brain/wiki/sources/research-pack-2026-07-27.md instead.
-->

# Verification ledger for the AI slop research report

Adversarial verification pass run 2026-07-27 against
`compass_artifact_wf-a639de9d-87a5-5f8c-9363-441f24c102dd_text_markdown.md`.
Every row below was checked against a primary source. Use this file, not the
original report, as the citation backbone.

## Part A: verdicts on load-bearing claims

| # | Claim | Verdict | Primary source | Correct figure |
|---|---|---|---|---|
| 1 | Merriam-Webster 2025 WOTY is "slop" | VERIFIED, one detail wrong | M-W press release via GlobeNewswire, 2025-12-15; ADS vote 2026-01-09 | Definition exact. Runners-up are gerrymander, performative, touch grass, six seven, Lake Chargoggagoggmanchauggagoggchaubunagungamaugg. "tariff" was NOT a runner-up. |
| 2 | Willison May 2024 slop post | VERIFIED verbatim | https://simonwillison.net/2024/May/8/slop/ , 2024-05-08 | "Not all promotional content is spam, and not all AI-generated content is slop. But if it's mindlessly generated and thrust upon someone who didn't ask for it, slop is the perfect term for it." |
| 3 | Kobak et al. excess vocabulary | **WRONG figures, missed the peer-reviewed version** | Science Advances 11(27), 2025-07-02, DOI 10.1126/sciadv.adt3813 (arXiv 2406.07016 v5) | **at least 13.5%** of 2024 abstracts, **up to 40%** in some subcorpora. The 10%/30% pair is the superseded v1. |
| 4 | Liang et al. detector bias | VERIFIED, caveat missing | Patterns 4(7):100779, 2023-07-10, DOI 10.1016/j.patter.2023.100779 | 61.3% average FPR on TOEFL essays; 19.8% unanimous. **n = 91 essays, 7 detectors, all pre-2020.** |
| 5 | OpenAI classifier withdrawn | VERIFIED | OpenAI announcement 2023-01-31, withdrawal note 2023-07-20 | 26% true positive, 9% false positive, pulled "due to its low rate of accuracy". |
| 6 | Package hallucination | VERIFIED (but now a 2024-cohort figure, see B) | USENIX Security 2025, Spracklen et al. | 19.7% average; 205,474 unique names; 5.2% commercial vs 21.7% open source; 43% recurred in all 10 reruns. |
| 7 | METR 19% slowdown | VERIFIED | arXiv 2507.09089, 2025-07-12 | 16 devs, 246 tasks, +19% completion time. Forecast -24%, post-hoc self-estimate -20%. |
| 8 | GitClear duplication and churn | **MIXED, churn figure wrong** | GitClear AI Copilot Code Quality 2025 (Feb 2025, 211M lines); Maintainability Gap (Jan 2026, 623M changes) | Moved 24.8% to 9.5%; copy/paste 8.3% to 12.3%; 8x rise in 5+ line duplicated blocks; block duplication 40.3 to 73.0 per million (+81%). See correction 2. |
| 9 | Workslop economics | VERIFIED | HBR 2025-09-22; betterup.com/workslop | n = 1,150 US desk workers. 40% received in prior month, ~2 hrs per incident, $186/employee/month, $9M/yr at 10,000 staff. |
| 10 | Pangram em dash and triad rates | **PARTLY VERIFIED, vendor marketing, self-contradictory** | https://www.pangram.com/supporting-evidence , undated | Page states BOTH 2 and 5 as the human em-dash baseline. No sample size, no methodology, no date, no citation. Do not quote as fact. Use B4 instead. |
| 11 | Wikipedia WP:LLM | VERIFIED, status mislabeled | RfC close 2026-03-20, 44-2, SNOW | It is a **content guideline, not a policy**. Exceptions: copyedit of your own writing, and LLM-assisted translation, both under mandatory human review. |
| 12 | EU AI Act Article 50 | VERIFIED, plus a 2026 update the report lacks | artificialintelligenceact.eu; Digital Omnibus adopted EP 2026-06-16, Council 2026-06-29 | Art. 50 still applies 2026-08-02, not amended by the Omnibus. Generative systems already on market get until **2026-12-02** for the Art. 50(2) machine-readable marking. Penalties up to EUR 15M or 3% turnover. |
| 13 | arXiv 2603.27006 "The Last Fingerprint" | **EXISTS**, but mischaracterized | arXiv 2603.27006, 2026-03-27, E. M. Freeburg | Real, but a **single-author unaffiliated non-peer-reviewed preprint**. See correction 5. |
| 14 | Shumailov et al. model collapse | VERIFIED | Nature 631:755-759 (2024), DOI 10.1038/s41586-024-07566-y | Citation exact. An Author Correction exists (s41586-025-08905-3), scope unverified behind Nature's auth wall. |

## Part C: corrections to apply

1. **Kobak figures are stale.** Use 13.5% and 40%, and cite Science Advances 2025, not the preprint.
2. **GitClear churn 7.1% is a discarded projection, not a measurement.** The real table reads 2020 3.1%, 2021 3.3%, 2022 3.3%, 2023 4.5%, 2024 projected 7.1%, **2024 actual 5.7%**. No year has a 7.1% actual. The 2026 report's churn figure is "two-week code churn +15%", not a level. These numbers are from the Feb 2025 report, not the 2026 one.
3. **Pangram is uncited vendor marketing and contradicts itself.** The only independent measurement found puts the human em-dash baseline at 32.3 per 10,000 words, roughly 6x to 16x higher than Pangram's claim.
4. **WP:LLM is a guideline, not a policy.**
5. **"The Last Fingerprint" is over-credited.** Its actual thesis is that em-dash rate is a signature of a specific fine-tuning procedure, not a universal AI tell. RLHF can also **eliminate** it: base Llama 3.1 8B 0.49 per 1,000, instruction-tuned 0.00.
6. **"tariff" was not an M-W runner-up.**
7. **Liang et al. needs its n = 91 caveat** whenever the 61.3% is quoted.
8. **METR's Feb 2026 follow-up** is a blog post, https://metr.org/blog/2026-02-24-uplift-update/ , not a paper.

## Part B: 2026 findings the report lacks

### B1. The finding that constrains the whole architecture

**Measuring AI "Slop" in Text**, Shaib, Chakrabarty, Garcia-Olano, Wallace,
arXiv 2509.19163, rev. 2026-01-24. LLM-as-judge agreement with human slop
labels is near zero: **GPT-5 kappa 0.01, DeepSeek-V3 -0.01, o3-mini 0.03**.
Models flag at 0.03 to 0.08 versus humans at 0.34, under-flagging by ~5x.
Span extraction: GPT-5 precision 0.14 / recall 0.11; a fine-tuned Qwen-7B
reached 0.32 / 0.30.

Compounding evidence that judges are biased toward slop features:

- **AI-AI bias**, Laurito et al., PNAS 122(31):e2415697122, 2025-07-29, peer reviewed. GPT-4 preferred LLM-written pitches 89% vs humans 36%.
- **Style Outweighs Substance**, Feuer et al., ICLR 2025, arXiv 2409.15268. Judge preferences do not correlate with factuality or safety.
- **Judging the Judges**, Soumik, TMLR 2026, arXiv 2604.23178. Style bias 0.10 to 0.76 (markdown preferred over plain text) vs position bias under 0.04. Verbosity bias is family-specific: Gemini and Llama +0.24 to +0.44, **Claude -0.12**.
- **Limits to scalable evaluation at the frontier**, Dorner, Nastl, Hardt, ICLR 2025, arXiv 2410.13341. When the judge is no more accurate than the evaluated model, no debiasing cuts required ground-truth labels by more than half.
- **LLM Evaluators Recognize and Favor Their Own Generations**, Panickssery et al., arXiv 2404.13076.

Design consequence: never ask the model for a holistic "is this slop" rating.
Every check must be a **structural procedure with a verifiable artifact**.

### B2. Human experts beat detectors

**Russell, Karpinska, Iyyer, ACL 2025**, arXiv 2501.15654. Majority vote of
five expert annotators misclassifies **1 of 300** articles, beating commercial
and open-source detectors even under paraphrase evasion. This is the primary
behind Wikipedia's "~90%" figure.

### B3. Model-specific fingerprints, including Claude

- **Idiosyncrasies in LLMs**, Sun et al., ICML 2025, arXiv 2502.12150. 97.1% accuracy on five-way model attribution; survives rewriting, translation, summarization.
- **StoryScope**, Russell et al., arXiv 2604.03136, 2026-04-03. 61,608 stories. 93.2% macro-F1 human vs AI on narrative features alone. **Claude signature: notably flat event escalation.**
- **The Rise of Verbal Tics in LLMs**, Wu et al., arXiv 2604.19139, 2026-04-21. 160,000 responses, 8 models. Verbal Tic Index: Gemini 3.1 Pro 0.590 worst, GPT-5.4 0.411, **Claude Opus 4.7 0.317**, DeepSeek V3.2 0.295 best. Human eval n=120: **r = -0.87** between sycophancy and perceived naturalness.
- **Voice Under Revision**, van Nuenen, arXiv 2604.22142, 2026-04-24. Function words, contractions and first-person pronouns fall; vocabulary diversity and word length rise, **even under explicit preserve-voice prompts**. Rewritten texts converge in feature space.
- **Saying More Than They Know**, Bakhshi, arXiv 2604.19768, 2026-03-27. LLMs produce tricolons at nearly **twice** the expert rate and hesitancy markers at twice human density.

### B4. Em dashes: the citation that replaces Pangram

**Em-ergence of the em-dash**, Czuma, arXiv 2606.29540, 2026-06-28.
**Pre-registered (OSF HFT8C)**, 69,632 medRxiv preprints. Discussion-section
prevalence rose from **4.23% pre-ChatGPT to 11.58% post** (+7.35 pp, 95% CI
6.94 to 7.77, OR 2.96). Trajectory ~4% through 2023, **8.0% in 2024, 20.3% in
2025**. Placebo split within the pre-LLM era showed no change (+0.13 pp).
Author's conclusion, to be adopted verbatim: **"The em-dash is a
population-level indicator, not a per-paper detector of LLM use."**

### B5. Excess-vocabulary successors

- Gray, arXiv 2512.01560, 2025-12-01: LLMs likely contributed to over 10% of all published papers in 2024, cross-disciplinary.
- Sanger and Maurer, arXiv 2602.03864, 2026-01-28: 149,452 ASCE abstracts 2000-2025.
- Miletic and Falk, arXiv 2605.19936, 2026-05-19: 37,000+ ACL Anthology papers. LLM-modified text has **lower lexical diversity** but expert readers rated it **more understandable and exciting**. Complicates the "slop is obviously worse" premise.
- Geng, Dong, Poibeau, arXiv 2603.25638, 2026-03-26: current classifiers struggle to identify which model produced a text.

### B6. Detection and provenance

**SynthID.** Google 2026-05-19: verification rolling out to Search and Chrome;
Gemini app verification used 50 million times; C2PA verification being added.
Independent work is uniformly negative on robustness. Han et al., TrustCom
2025 (peer reviewed), arXiv 2508.20228: vulnerable to paraphrase, copy-paste,
back-translation. DAMAGE Table 2: SynthID TPR@5%FPR falls **87.6% to 5.4%**
after DIPPER paraphrase. Omidi, Dong, Wang, arXiv 2603.03410, 2026-03-03:
layer-inflation attack. The widely repeated "SynthID 100% to 21%" figure from
The Register **could not be verified; do not cite it**.

**C2PA.** Spec 2.4, April 2026. 2.3 (Jan 2026) added live video provenance and
plain text. Interim Trust List frozen 2026-01-01. First independent security
analysis is damning: Golaszewski, Krawetz, Sherman et al., arXiv 2604.24890,
2026-04-27, concludes the specs "fail to achieve their claimed security goals"
and "should not yet be relied upon for high-stakes uses such as financial
disclosures, journalism, or legal evidence", and that 2.4 does not fix it.
**ISO 22144 could not be verified as published**; the claim appears only in
marketing blogs.

**Pangram, independently assessed.** The only third-party peer-reviewed
evaluation found is IJEI 22:16 (2026), DOI 10.1007/s40979-026-00226-w, behind
a Springer wall and unread. The strongest positive result (NBER WP 34223) is
unrefereed, and two of the most-cited "independent" results have Pangram
employees as co-authors. Two 2026 preprints report failure: **Base Models Look
Human To AI Detectors**, Xu et al. (CMU), arXiv 2605.19516, found Llama3-8B
*base* output rated **98.8% human**, concluding detectors capture "artifacts of
instruction tuning" rather than machine generation; Ren et al., arXiv
2606.25152, measured Pangram at **24.1%** on adversarial text.

**Detector bias, the 2026 replacement for Liang et al.** *Identifying Bias in
Machine-generated Text Detection*, Stowe, Afanaseva, Raimundo, Sun, Patil
(Pindrop), **ACL 2026, peer reviewed**, arXiv 2512.09292. 16 detection models
on student essays labelled for gender, race, ELL status, SES. ELL essays more
likely flagged; **non-White ELL students disproportionately flagged versus
White ELL peers**; **human annotators showed no significant demographic bias**.

Also: PAN 2026 (arXiv 2602.09147) adds a Reasoning Trajectory Detection task.
Best 2026 zero-shot successor to Binoculars is **Triospect**, Bao et al.,
arXiv 2606.31074, TACL, +22.3% AUROC on Humanize-16K. RAID has no v2 and its
leaderboard 404s. Curtin University disabled Turnitin AI detection from
2026-01-01.

### B7. Humanizers degrade quality

**DAMAGE**, Masrour, Emi, Spero, GenAIDetect at COLING 2025 (peer reviewed but
Pangram-authored), arXiv 2501.03437. Fluency win rate of humanized vs original
judged by GPT-4o: best tier **26.0%**, medium 14.67%, worst 2.67%. Verbatim:
**"all humanizers tend to degrade the quality of the original text."**
Documented failure modes: hallucinated citations, comment leakage, nonsensical
strings. Evasion: Binoculars 94.15% to 28.23% TPR@5%FPR.

Corroborating: TH-Bench (arXiv 2503.08708) finds no attack excels on evasion,
quality and cost at once. Adversarial Paraphrasing (Cheng et al., NeurIPS 2025,
arXiv 2506.07001) reaches 87.88% average T@1%F reduction with only slight
quality loss, so research-grade attacks preserve quality far better than
commercial tools. Base Models Look Human quantifies the tradeoff: iterative
paraphrasing hits 100% human-probability by round 10, but semantic preservation
collapses from 99-100 to a 33-99 range.

**Stated gap:** no peer-reviewed study measures commercial humanizer output
with human raters or standard writing rubrics, and none quantifies introduced
factual errors.

### B8. Agentic coding slop, 2026

Pro-thesis:

- **MSR 2026, peer reviewed**, Chowdhury et al.: PRs handled only by code-review agents merge at **45.20%** vs **68.37%** human-only; 60.2% of closed CRA-only PRs fall in the 0-30% signal range.
- Faros AI, 2026-04-12, vendor, 22,000 devs: churn +861%, bugs per developer +54%, incidents-to-PR ratio +242.7%, PRs merged without review +31.3%.
- LinearB, vendor, 8.1M PRs: AI PR acceptance 32.7% vs 84.4% manual; agentic PRs wait 5.3x longer for pickup.
- Sonar State of Code 2026, n=1,149: 96% do not fully trust AI code correctness; 61% agree it "often produces code that looks correct but isn't reliable"; 38% say reviewing AI code takes more effort than a colleague's.
- **Debt Behind the AI Boom**, Liu et al., arXiv 2603.28592: 302.6k AI-authored commits; over 15% of commits from every assistant introduce at least one issue; 22.7% of AI-introduced issues survive.
- Veracode Spring 2026, vendor: only 55% of generation tasks produce secure code; Java 29%.

Counter-evidence the report entirely lacks:

- **Borg et al., pre-registered with In-Principle Acceptance** (granted at ICSME), arXiv 2507.00788, a **preprint** rather than a published paper, 151 participants: Phase 2 found **no significant differences** in subsequent code evolution, completion time, or quality, while observational Phase 1 found a **30.7 percent median reduction in completion time**. Methodologically the strongest item in the area, and it must be cited with both phases.
- Greptile, vendor, several million PRs: reverts per 1,000 PRs, Codex 1.19, Claude 1.80, **human baseline 2.72**. Agent PRs revert *less* than human PRs.
- Meta RADAR, arXiv 2605.30208, 535k+ diffs: automated low-risk review cut revert rate to 1/3 and production incidents to 1/50.
- Mao et al., arXiv 2603.27130: real-world AI vs human differences are "rather small"; security alerts per KLOC AI 12.81 vs human 11.58.

Honest pattern: the strongest slop numbers come from vendors selling
engineering-intelligence products; the strongest null results come from
academia.

**curl reversed in 2026.** Stenberg, "High-Quality Chaos", 2026-04-22: **"the
slop situation is not a problem anymore."** Report frequency is about double
the 2025 rate, confirmed-vulnerability rate is back to 15-16%, and curl
**returned to HackerOne on 2026-03-01**, bounty-free. The report's narrative
stops at the Feb 2026 shutdown and misses the return.

**Recursive collapse now shown in code.** Song, Cai, Zhao, arXiv 2606.28438,
2026-06-26: AI self-review gates enter a **"rubber-stamp regime where
acceptance scores rise while benchmark correctness falls."** Directly relevant
to any skill that uses a model to gate its own output.

**Package hallucination improved by an order of magnitude.** Churilov, arXiv
2605.17062, 2026-05-16, and Socket, 2026-07-22, 199,845 responses: 2026
frontier models hallucinate at **4.62% to 6.10%** (Claude Haiku 4.5 4.62%,
GPT-5.4-mini 6.10%). **53 hallucinated names remain registerable.** The "~20%"
figure is now a 2024-cohort number.

**Sycophancy with numbers.** ELEPHANT, Cheng et al., Science, DOI
10.1126/science.aec8352: LLMs preserve user face **45 pp more than humans**;
affirm both sides in 48% of moral conflicts. SycEval, AIES 2025: overall
sycophancy 58.19%, persistence 78.5%. Anthropic, 2026-04-30, ~639k
conversations: 9% of guidance conversations sycophantic overall, 25%
relationships, 38% spirituality; Opus 4.7 roughly half the rate of Opus 4.6.
**No published study counts "You're absolutely right" in coding-agent
transcripts.**

## Caveats on this verification

- The session WebSearch budget was exhausted. Loose ends: the Martian code-review leaderboard, the Nature Author Correction to Shumailov, the Springer-walled IJEI Pangram evaluation.
- Blocked or paywalled, stated rather than guessed: merriam-webster.com (Cloudflare), openai.com blog (403), sciencedirect.com (403), nature.com (auth wall), hbr.org (body), iso.org (403), Claude Opus 5 System Card (PDF over fetch limit).
- Most 2026 items are arXiv preprints verified at abstract level only. Every arXiv ID was confirmed to resolve with a matching title, including 2603.27006.
