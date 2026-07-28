> **Superseded figures warning.** This is the original research report, kept
> for provenance. Several of its figures were later found to be wrong and are
> corrected in `research/verification-ledger.md` and in
> `anti-slop-brain/wiki/evidence/Superseded Figures.md`. Most importantly, the
> Kobak prevalence figures quoted below as 10 and 30 percent come from a
> withdrawn preprint; the published figures are 13.5 and 40 percent. Do not
> quote this file directly. Quote the ledger.

> This file is preserved verbatim as a historical record, so it retains the
> em dashes and the original figures. It is deliberately excluded from the
> house style gate in CI: editing an archived document to satisfy a lint
> rule would falsify the archive.

# AI Slop: A Full-Depth Research Report

## TL;DR
- "Slop" is now the mainstream label for low-quality, mass-produced AI content: Merriam-Webster and the American Dialect Society both named it 2025 Word of the Year, and Merriam-Webster defines it as "digital content of low quality that is produced usually in quantity by means of artificial intelligence." The most useful working definition (Simon Willison's) is behavioral, not aesthetic: slop is unreviewed AI content "mindlessly generated and thrust upon someone who didn't ask for it" — meaning slop is defined by low effort and lack of human review/accountability, not merely by being AI-generated.
- The strongest evidence base for a detection skill is empirical corpus work on prose (PubMed "excess vocabulary" like "delve," "underscore," "meticulous"; em-dash and rule-of-three frequency) and on code (GitClear's churn/duplication data, package-hallucination rates, the METR productivity RCT). Many popular "tells" (em dashes, rule of three) are real statistical signals but have high false-positive rates against skilled/edited/non-native human writing — so the user's quality-based diagnostic tests (deletion/stranger/inversion) are better-founded than banned-word lists.
- Detection is losing the arms race: AI text detectors are unreliable (OpenAI withdrew its own classifier at 26% true-positive; Stanford found 61% false positives against non-native writers), and estimates that "50%+ of the web is AI" rest on those same shaky detectors. The mitigations with the best evidence are editorial/quality gates, provenance standards (C2PA, SynthID), and workflow changes — not detector-based policing.

## Key Findings

1. **The term is behavioral, not just aesthetic.** The differentiator between "AI-generated" and "slop" is effort, review, and whether it was unwanted — not the mere presence of AI. This validates the user's quality-test approach over origin-detection.
2. **Prose markers are empirically real but noisy.** Corpus studies robustly show vocabulary shifts (Kobak et al.: ≥10% of 2024 PubMed abstracts show LLM excess vocabulary, up to 30% in some subfields). But the same features that flag AI also flag ESL and formulaic human writing.
3. **Code slop has the hardest numbers.** GitClear (211M+ lines): copy/paste exceeded moved/refactored code for the first time in 2024; duplicated blocks rose ~8x. METR RCT: experienced devs were 19% slower with AI while believing they were 20% faster. Package hallucination (~20% of recommended packages don't exist) has spawned "slopsquatting" supply-chain attacks.
4. **Slop imposes measurable downstream cost.** BetterUp/Stanford "workslop": 40% of desk workers received it in a month, ~2 hrs to resolve each incident, ~$186/employee/month, ~$9M/yr for a 10,000-person firm.
5. **Platform harms are documented and named:** Facebook "Shrimp Jesus" engagement farms, Spotify's Velvet Sundown AI band, NewsGuard's tracking of 3,700+ unreliable AI news sites, Amazon's dangerous AI mushroom-foraging guides, and academic paper-mill "tortured phrases" like "vegetative electron microscopy."
6. **Model collapse is real in theory but contested in practice.** The Nature paper (Shumailov et al. 2024) shows recursive training degrades models, but critics note it assumes data *replacement*; with data *accumulation* plus curation, collapse is largely avoidable.
7. **Detection doesn't work well enough to police.** This is the single most important finding for the skill: build around quality, not origin-detection.

## Details

### 1. Definition and Etymology

**Origin of the term.** "Slop" as slang for AI content emerged around 2022 on 4chan, Hacker News, and YouTube comments, initially about low-quality AI images. It was popularized in 2024: a poet/technologist writing as "deepfates" posted that it was "the term for unwanted AI generated content," and developer **Simon Willison** amplified it in a **May 8, 2024** blog post arguing "slop" should become the standard term the way "spam" did for unwanted email. Willison's definition is the most-cited: "Not all AI-generated content is slop. But if it's mindlessly generated and thrust upon someone who didn't ask for it, slop is the perfect term for it." He also proposed "slom" for the AI-generated subset of spam. (Willison notes he was building on deepfates.)

**Etymological history.** "Slop" dates to Middle English (a "mud hole"); by the 1700s it meant soft mud, and by the 1800s food waste/pig swill and "a product of little or no value." The AI sense is a natural extension of "rubbish."

**Dictionary/lexicographer recognition.**
- **Merriam-Webster 2025 Word of the Year** (announced Dec 15, 2025): "digital content of low quality that is produced usually in quantity by means of artificial intelligence." President Greg Barlow described the flood of "absurd videos, weird advertising images, cheesy propaganda, fake news that looks real, junky AI-written digital books." Runners-up included "gerrymander," "touch grass," "performative," "tariff."
- **American Dialect Society** also selected "slop" for 2025.
- **Macquarie Dictionary** (Australia) named "AI slop" its Word of the Year for 2025, winning both Committee's and People's Choice.
- Related 2025 WOTY picks: **Oxford** chose "rage bait"; **Dictionary.com** chose "67"; Oxford's 2024 pick was "brain rot."

**Related and competing terms:**
- **Workslop** — AI-generated work output that looks polished but lacks substance, shifting labor downstream (BetterUp/Stanford, Sept 2025).
- **Slopaganda** — portmanteau of slop + propaganda, coined 2025 by Michał Klincewicz (Tilburg University); AI slop deployed with deliberate political/ideological intent.
- **Slopper** — a person overly reliant on generative AI (documented by Macquarie; "People Are Becoming 'Sloppers'").
- **Slopsquatting** — supply-chain attack registering hallucinated package names.
- **Slopwashing** — disguising AI slop as human/legitimate.
- **Model collapse / Habsburg AI** — degradation from training on AI output.
- **Enshittification** (Cory Doctorow), **brain rot**, **dead internet theory**, **churnalism**, **content farms**, **kitsch** — adjacent concepts.
- Lexical productivity has been so high it's been called a "slopocalypse."

**"Is all AI content slop?" — the definitional debate.** Willison, deepfates, and Scientific American explicitly say no: "not all AI-generated content is slop." Ben Congdon offers a competing, origin-based definition: "Content that is mostly-or-completely AI-generated that is passed off as being written by a human, regardless of quality." The Philosophical Salon argues the whole category is imprecise — "To say that 'AI produces only slop' is a simple statistical error… most human ideas are mediocre" — and compares the panic to historical moral panics about kitsch, television, and every prior mass medium. This is a genuine live disagreement: is slop about (a) quality, (b) origin + deception, or (c) the unwanted/low-effort act of publishing? The user's skill implicitly adopts (a)+(c), which is the most defensible.

### 2. Textual / Prose Slop — Linguistic Markers

**Empirical corpus studies (the strongest evidence):**
- **Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary"** (arXiv 2406.07016): analyzed 15M+ PubMed abstracts 2010–2024. Found an abrupt post-2022 rise in "excess" style words; estimated **at least 10% of 2024 abstracts were LLM-processed, up to 30% in some subfields/countries.** Method is detector-free (compares actual vs. extrapolated word frequencies, analogous to COVID excess-mortality). Excess words are overwhelmingly **stylistic verbs/adjectives** ("delves," "underscores," "showcasing," "potential," "crucial," "additionally").
- **Matsui, "Delving into PubMed Records"** (medRxiv 2024; PMC12679996): of 135 candidate AI-influenced terms, **103 showed meaningful increases (modified Z-score ≥3.5) in 2024**; top risers "delve," "underscore," "primarily," "meticulous," "boast." Crucially, these terms **began rising ~2020, before ChatGPT** — suggesting AI accelerated pre-existing academic-ese, complicating naive detection.

**Lexical markers (folk + corpus-backed):** delve, intricate, testament, tapestry, landscape, showcase, underscore, boasts, realm, pivotal, crucial, leverage, robust, seamless, navigate, foster, meticulous, commendable. Wikipedia adds puffery: "rich cultural heritage," "enduring legacy," "stands as a testament," "plays a vital/significant role."

**Syntactic/rhetorical markers:**
- **Negative parallelism / "not X, but Y"** ("It's not just about the music; it's about the movement") — Wikipedia flags this as a hallmark: AI "sets up a contrast where it corrects a misconception nobody actually had."
- **Rule of three / triads** — Pangram Labs measures AI using them ~4x as often as humans.
- **Em dashes** — humans average ~5 per 10,000 words; most model families exceed that 7–9x per Pangram. Em-dash usage in scientific abstracts more than doubled 2021–2025. But this is contested: em dashes signal *formal edited prose* (what AI trained on), so the "fingerprint" is really a formality marker, and skilled human writers use them heavily. Token-economy theories (an em dash is one token vs. three for ", and") and markdown-training theories exist.
- Other: sycophancy, hedging, "In conclusion," section summaries that restate, uniform sentence length / low burstiness/perplexity, vague attribution ("studies show," "experts say"), false ranges.

**Structural markers:** bullet-point overuse, bolded key terms, section inflation, formulaic essay structure, markdown artifacts.

**Wikipedia's WikiProject AI Cleanup & "Signs of AI Writing."** Launched 2023; by 2026 it had cleaned up 10,000+ AI articles and tagged 500+; since March 2026 the WP:LLM guideline prohibits LLM-generated article content. The "Signs of AI Writing" guide is a ~15,000-word field guide built from thousands of real cases. Key methodology point directly relevant to the user: it is **descriptive not prescriptive**, explicitly says no single sign proves AI, and recommends patterns as a *combined* signal. It also notes heavy LLM users can identify AI text ~90% of the time (so tagging 10 pages ≈ 1 false accusation), while non-users do "only slightly better than random." The highest-signal categories they flag: undue emphasis/puffery, over-attribution, superficial analysis, AI vocabulary, and markdown artifacts. This is the direct prior art for blader/humanizer's 33 patterns.

**Why these patterns emerge:** RLHF pushes toward "helpful/harmless" register and sycophancy; next-token prediction favors high-probability/typical phrasing (mode collapse toward the "average"); markdown-heavy training data; brevity/token incentives. The "Last Fingerprint" work (arXiv 2603.27006) links markdown training to em-dash/list habits and shows RLHF amplifies them.

**Cross-lingual:** the EU is localizing AI-content labels ("KI"/"IA"); the "excess vocabulary" effect is measurable across languages, and machine-translation prevalence is highest in low-resource languages (see Thompson et al. below).

### 3. Code Slop

**What it looks like:** redundant comments, ceremonial docstrings, over-abstraction, passthrough wrappers, defensive noise, generic naming, swallowed exceptions, assertion-free/coverage-padding tests, hallucinated APIs/packages.

**GitClear empirical data (the flagship dataset):**
- **AI Copilot Code Quality (Feb 2025)**, 211M changed lines 2020–2024: "moved" (refactored/reused) code fell from ~25% (2021) to <10% (2024); copy/pasted rose from 8.3% to 12.3%; **2024 was the first year copy/paste exceeded moved code**; duplicated blocks (5+ repeated lines) rose ~**8x**.
- **The Maintainability Gap (2026)**: block duplication climbed from 40.3 per million changed lines (2023) to 73.0 (2026 YTD), +81%; code churn roughly doubled from a ~3.3% pre-AI baseline to 5.7% (2024) and 7.1% (2025).
- Caveat: GitClear itself is correlational (AI adoption coincides with, not proven to cause, the decline), and GitClear sells code-quality tools.

**METR RCT (arXiv 2507.09089, July 2025):** 16 experienced open-source devs, 246 real tasks on mature repos they averaged 5 years on; using early-2025 AI (mostly Cursor Pro + Claude 3.5/3.7) **increased completion time by 19%**, though devs forecast 24% speedup and *still believed* post-hoc they were 20% faster. This perception gap is the headline. Caveats: small n; AI tools have improved since; other studies find gains for juniors/greenfield/boilerplate. METR's Feb 2026 follow-up couldn't get a clean signal because devs increasingly refused to work without AI.

**Slopsquatting & package hallucination:**
- **Spracklen et al. (USENIX Security 2025), "We Have a Package for You!"**: ~20% of packages recommended by code LLMs don't exist; **205,000 unique hallucinated names**; GPT-series hallucinate ~5.2% vs. ~21.7% for open-source models; **43% of hallucinations recurred across all 10 re-runs of the same prompt, 58% more than once** — making them predictable enough to weaponize.
- Term "slopsquatting" coined by **Seth Larson** (PSF), popularized by Andrew Nesbitt. Autonomous agents remove the human checkpoint, raising the risk tier. Real malicious packages exploiting this have accumulated tens of thousands of downloads; a related campaign (litellm/telnyx) and Aikido's Charlie Eriksen research documented propagation via AI-generated "skills" across 237 repositories.

**Open-source burden:**
- **curl/Daniel Stenberg:** began complaining ~2024; by mid-2025 ~20% of bug-bounty submissions were "AI slop"; instituted instant bans (May 2025) but volume hit 8x normal; **ended its HackerOne bug-bounty program effective Feb 1, 2026.** Real reports fell from ~1 in 6 (early 2025) to ~1 in 20–30 (late 2025). One fake report cited GDB sessions referencing a nonexistent function. Program had confirmed 87 vulnerabilities and paid $100,000+ over its life. Stenberg's rule: never report a bug you can't reproduce.
- The flip side: AI *can* find real bugs (e.g., Theori's autonomous system found a critical Redis use-after-free RCE). The defender takeaway is triage (require reproducible PoC), not blanket AI bans.

### 4. Visual, Audio, and Video Slop

**Images — "Shrimp Jesus":** Surreal AI images (Jesus fused with shrimp) flooded Facebook in 2024. Stanford Internet Observatory + Georgetown (DiResta & Goldstein, in HKS Misinformation Review) documented 125 Pages generating hundreds of millions of exposures, boosted by Facebook's "Suggested for You." 404 Media (Jason Koebler) traced the economy: creators in Pakistan, India, Vietnam, etc., using Microsoft AI Image Creator + Facebook creator-bonus payouts, running up to 10,000–13,000 fake accounts. Signs: broken physics, gibberish in-image text, recycled "Made it myself" captions, mismatched Page names.

**Music — Velvet Sundown:** A fully AI-generated "band" (made with Suno) peaked near **1.4M Spotify monthly listeners in late July 2025** (per The National and Music Ally, falling to ~594,000 by mid-August); spokesperson "Andrew Frelon" told Rolling Stone the music was made with Suno, calling it an "art hoax," before Rolling Stone reported Frelon was himself a hoaxer. The band's own bio now calls it "a synthetic music project ... composed, voiced, and visualized with the support of artificial intelligence." **Spotify's Sept 25, 2025 policy**: mandatory DDEX AI disclosure, ban on unauthorized voice cloning, spam filter; Spotify said it removed 75M+ spam tracks in 12 months. Deezer disclosed AI = 28% of uploads but only 0.5% of streams (Sept 2025), rising to ~44% of daily uploads by April 2026, 85% of AI streams flagged fraudulent. Third-party labelers (SoullessMusic, SlopTracker) exist because Spotify won't label.

**News/journalism — NewsGuard:** Tracks "Unreliable AI-Generated News" sites (UAINs): 49 in May 2023 → 125 two weeks later → 700+ by Feb 2024 → 966 → 3,749+ AI content-farm sites by the latest count, in 16 languages, mostly monetized via programmatic ads (~$2.6B/yr misdirected). Generic names ("Ireland Top News," "iBusiness Day"). Pink-slime local news and takeover of defunct domains (Hong Kong's Apple Daily).

**Books:** Amazon KDP flooding with AI titles; **dangerous AI mushroom-foraging guides** (404 Media/Samantha Cole, 2023) — NYMS warned "it can literally mean life or death"; Originality.ai scored four samples 100% AI; experts flagged advice to identify mushrooms by "smell and taste." Also AI obituary spam and travel guides (the MSN Ottawa food-bank listing).

**Video:** Sora/Veo-era clips, AI kids' "brain rot" content, disaster misinformation (LA Palisades fires; Hurricane Helene fake rescue images, one shared then deleted by a US senator).

### 5. Where Slop Appears and Downstream Harms

- **Search/SEO:** content farms, Google's "helpful content" and site-reputation-abuse updates; degraded results.
- **Academic publishing:** paper mills, "tortured phrases" (e.g., "counterfeit consciousness" for AI to dodge plagiarism software), "vegetative electron microscopy" (a "digital fossil" born from a 1959 two-column OCR error, propagated by CommonCrawl-trained models, defended by Elsevier before correction), and "as of my last knowledge update"/"I am an AI language model" appearing in published papers. Retraction Watch and the Problematic Paper Screener track these.
- **Workplace "workslop":** BetterUp Labs + Stanford Social Media Lab (HBR, Sept 2025), survey of 1,150 US desk workers: 40% received workslop in the prior month; ~2 hrs to resolve each; ~$186/employee/month; ~$9M/yr per 10,000 employees. 53% felt annoyed, 22% offended; ~half viewed senders as less creative/reliable/trustworthy. Caveat: self-reported estimates; "knowledge decay" framing is synthesized, not experimentally tested. Context: **MIT Project NANDA's July 2025 report "The GenAI Divide: State of AI in Business 2025"** (300 public deployments, 150 executive interviews) found that despite $30–40B in enterprise GenAI spending, 95% of organizations achieved zero return: "Just 5% of integrated AI pilots are extracting millions in value, while the vast majority remain stuck with no measurable P&L impact."
- **Hiring:** AI resumes/cover letters at scale met by AI screening — an arms race.
- **Social media / dead internet theory:** engagement bots on Reddit, X, LinkedIn, Facebook; **Imperva's 2025 Bad Bot Report (12th annual, Thales)** found automated traffic surpassed human activity for the first time in a decade at 51% of all web traffic in 2024 (bad bots 37%); the follow-up 2026 "Bad Bots in the Agentic Age" report put automated traffic at 53% in 2025 vs. 47% human.

### 6. Model Collapse and Training-Data Contamination

- **Shumailov et al., "AI models collapse when trained on recursively generated data," Nature 631:755–759 (2024)** (earlier as "The Curse of Recursion," 2023): recursively training on generated data causes early collapse (tails/variance lost) and late collapse (convergence to low-variance point estimate). Demonstrated on GMMs, VAEs, and OPT LLMs.
- **The debate:** Borji (arXiv 2410.12954) says it's a general statistical phenomenon of repeated resampling. But "Position: Model Collapse Does Not Mean What You Think" (arXiv 2503.03150) and the accumulation literature (Alemohammad et al. "Self-Consuming Generative Models Go MAD," 2023; Gerstgrasser et al.) argue collapse assumes data *replacement*; if synthetic data *accumulates* alongside human data, or if generated data is curated/filtered, collapse is largely avoided. Consensus tilt: model collapse is a real risk for naive recursive loops but is *not* an imminent existential threat to frontier models that curate data. Well-curated synthetic data is demonstrably beneficial (used across frontier training).
- **"Low-background steel" analogy:** pre-2022 (pre-ChatGPT) human data is prized as uncontaminated; Wikipedia notes text before Nov 30, 2022 is "very unlikely to be AI-generated."
- **How much of the web is AI?** Contested and detector-dependent. Graphite (May 2025): 52% of newly published English web articles "primarily" AI, using a single detector (Surfer, ~4.2% FPR); AI first passed human in Nov 2024. Graphite's own re-analysis with three detectors (Pangram, GPTZero, Copyleaks) lowered the figure ~3.3 points (Q4 2025 ≈ 50.9%). Only ~14% of *Google-ranking* articles were AI. Ahrefs (April 2025): 74% of ~900k new pages had *some* AI but only 2.5% were purely AI. Thompson et al. (AWS, ACL Findings 2024, arXiv 2401.05749): 57.1% of multi-parallel web sentences are machine-*translated* (not GenAI-authored) — routinely mis-cited as "57% of the web is AI." All figures rest on detectors of disputed reliability; Graphite itself acknowledges detection may be "impossible or highly inaccurate."

### 7. Detection

- **Text detectors are unreliable.** OpenAI launched its AI Text Classifier Jan 31, 2023 and **withdrew it July 20, 2023** "due to its low rate of accuracy" — it caught only **26% of AI text (true positives) and false-flagged human text 9% of the time.**
- **Bias:** **Liang et al., "GPT detectors are biased against non-native English writers," Patterns (2023)**: 7 detectors misclassified **61.3%** of TOEFL (non-native) essays as AI while near-perfectly clearing native essays; 19.8% unanimously flagged. Mechanism: non-native writing has lower perplexity. Prompting to "enhance word choice" cut misclassification to 11.6%; simplifying native essays raised theirs to 56.7%. Vanderbilt disabled Turnitin's AI detector (Aug 2023) citing false-positive risk (even 1% FPR = 750 false accusations/yr at their volume).
- **Statistical/zero-shot methods:** DetectGPT (Mitchell et al., ICML 2023) uses probability curvature (0.95 AUROC in one setting). Binoculars (Hans et al., ICML 2024) uses perplexity/cross-perplexity ratio from two paired LLMs, claiming >90% detection at 0.01% FPR. GPTZero (Edward Tian) uses perplexity + burstiness; vendor claims ~99% but independent tests report ~80–90% with higher FPR/FNR.
- **Watermarking:** Google DeepMind **SynthID-Text** (Dathathri et al., Nature Oct 2024) modifies token sampling ("Tournament Sampling"); deployed in Gemini, open-sourced; ~20M-response live test showed no quality loss. Limit: weakened by heavy paraphrasing; only works on content the model itself generates. Nature's editorial stresses robustness is unsolved.
- **Provenance:** **C2PA / Content Credentials** (Adobe, Arm, BBC, Intel, Microsoft, Truepic, 2021; now Google, Sony, OpenAI). Asserts positive provenance, does not detect fakes. Adopted by Adobe, OpenAI (DALL-E 3/Sora, paired with SynthID), Google Pixel 10 (signs every photo via hardware), TikTok (1.3B+ labeled). Key limitation: metadata routinely stripped by uploads/screenshots/recompression (RAND, June 2025: end-to-end compliance "unrealistic" in an open ecosystem).
- **Regulation:** EU AI Act **Article 50** transparency duties apply **Aug 2, 2026** (machine-readable marking of AI content; deployer labeling of deepfakes/AI text). EU Code of Practice on Transparency drafts Dec 2025 / March 2026; an EU "AI" visual label.
- **Why detection is the wrong frame (key for the skill):** Wikipedia editors deliberately skip detector software in favor of human pattern-recognition; detectors can't explain reasoning, produce false positives, and are trivially defeated by "humanizer" tools. The defensible frame is **editorial/quality assessment** — exactly the user's deletion/stranger/inversion tests.

### 8. Economics and Incentives

- **Generation/verification asymmetry** is the engine: generating plausible content is near-free; verifying/refuting it is expensive (Brandolini's law — the "bullshit asymmetry" — applied to AI). Slopsquatting economics are explicitly asymmetric: attacker registers one package cheaply; every defender must verify every dependency.
- **Monetization:** programmatic ad revenue (NewsGuard: ~$2.6B/yr misdirected to junk sites), platform creator-bonus programs (Facebook, pre-reform Spotify), SEO arbitrage, content-farm economics.
- **Labor displacement:** writers, illustrators, voice actors, translators; workslop shifts cleanup labor onto recipients (~$186/employee/month invisible tax).

### 9. Cultural and Epistemic Effects

- **Erosion of trust / "liar's dividend":** anything polished is now suspected of being AI (the em-dash panic; skilled human writers self-censoring em dashes). PBS/Merriam-Webster: the word is "defiant" — people "want things that are real."
- **Backlash:** "human-made" certification/labeling, artist/writer resistance, platform bans (Clarkesworld closed submissions after AI-story flood; Gentoo, NetBSD, QEMU-style AI-contribution bans in open source).
- **Effects on human style:** **Yakura et al., "Empirical evidence of Large Language Model's influence on human spoken communication" (arXiv 2409.01754)** analyzed 740,000+ hours across 824,634 podcast episodes and 20,000+ academic YouTube channels: "words preferentially generated by ChatGPT, such as delve, showcase, boast, intricacies and meticulous, increased abruptly in spontaneous human speech" — "delve" usage rose 48%, "realm" 35%, "adept" 51% within 18 months of ChatGPT's release; a preregistered experiment (N=496) confirmed entrenchment in active vocabulary. This is direct evidence of "human-LLM coevolution."
- **Counterarguments (important for balance):** accessibility benefits for non-native speakers and disabled writers; elitism critique of anti-AI style-policing; false-accusation risk (the ESL bias); The Philosophical Salon's argument that slop panic mirrors past moral panics. The strongest steel-man: style-based detection punishes exactly the humans (ESL, formulaic, plain writers) it shouldn't.

### 10. Mitigations and What Actually Works

- **Platform-level:** Google (helpful-content, site-reputation-abuse updates); YouTube (2025 monetization policy clarifying "inauthentic"/mass-produced content); Spotify (Sept 2025 AI disclosure/anti-impersonation); Amazon KDP (volume caps, AI disclosure requirement); Clarkesworld (closed subs); Medium; Reddit; Stack Overflow (temporary GPT ban); arXiv (2025 moderation tightening on AI-generated survey/position papers).
- **Editorial/institutional:** journal disclosure requirements; Wikipedia WP:LLM prohibition (March 2026); newsroom AI style guides.
- **Technical:** provenance/watermarking (C2PA + SynthID as complements), retrieval grounding, verification loops, evaluator/critic models, human-in-the-loop. Detector-based gates are discouraged.
- **Workflow/prompting:** evidence favors requiring sources/citations, reproducible artifacts (PoC for security, tests for code), and human review over "humanizer" tools (which just move the problem and defeat detectors without adding substance).
- **Existing anti-slop tooling:** humanizer/detector-bypass tools (adversarial, don't improve quality); editing skills/linters; the user's prior art (blader/humanizer 30.7k stars based on Wikipedia's 33 patterns; rand/cc-polymath; adewale/anti-slop-writing). The evidence-based lesson: **pattern lists have high false-positive rates; quality/deletion tests generalize better.**

### 11. Sources and Further Reading

Key papers/studies: Shumailov et al. (Nature 2024, model collapse); Kobak et al. (excess vocabulary, PubMed, arXiv 2406.07016); Matsui (medRxiv, PubMed terms); Spracklen et al. (USENIX 2025, package hallucination); METR (arXiv 2507.09089); GitClear reports (2025, 2026); Liang et al. (Patterns 2023, detector bias); Mitchell et al. (DetectGPT, ICML 2023); Hans et al. (Binoculars, ICML 2024); Dathathri et al. (SynthID-Text, Nature 2024); Thompson et al. (AWS, ACL 2024, arXiv 2401.05749); BetterUp/Stanford workslop (HBR 2025); MIT Project NANDA GenAI Divide (2025); Yakura et al. (spoken-language influence, arXiv 2409.01754); DiResta & Goldstein (Facebook AI spam, HKS Misinformation Review).

Key essays/criticism: Simon Willison ("Slop is the new name…," May 2024); Ted Chiang; Ed Zitron; Max Read; Jason Koebler & 404 Media reporting; The Philosophical Salon ("The Idea of 'AI Slop' Is Slop"); Ben Congdon ("AI Slop, Suspicion, and Writing Back").

Tracking projects: NewsGuard AI Tracking Center; Wikipedia WikiProject AI Cleanup & "Signs of AI Writing"; Retraction Watch / Problematic Paper Screener; SlopTracker/SoullessMusic (music labeling).

## Recommendations

For building the "anti-slop" skill:

1. **Lead with quality tests, not banned-word lists (highest confidence).** The evidence is unambiguous that origin-detection and lexical blocklists have unacceptable false-positive rates against skilled, edited, and non-native human writing. The deletion/stranger/inversion tests are the right foundation. Ship banned-word behavior only as *soft signals that trigger the quality tests*, never as hard fails. Benchmark that would change this: if a detector emerges with independently verified <1% FPR across ESL and expert-human corpora, revisit.

2. **Weight markers by evidence tier.** Tier 1 (corpus-validated): excess vocabulary (delve/underscore/meticulous), puffery/undue-emphasis, over-attribution ("studies show"), superficial-analysis padding, negative parallelism ("not just X, but Y"). Tier 2 (measured but high-FP): em-dash density, rule-of-three, uniform burstiness. Tier 3 (folk wisdom): specific single words in isolation. Encode the tier so the skill explains *why* it flags, mirroring Wikipedia's "combined signal, never a single tripwire" methodology.

3. **Add domain-specific modules.** For **code**: flag passthrough wrappers, swallowed exceptions, assertion-free tests, coverage padding, and — critically — **unverified package imports** (slopsquatting gate: check every dependency exists in the registry). For **docs/UI**: flag section inflation, template-convergence, and unsupported superlatives. The deletion test maps cleanly onto ceremonial comments/docstrings.

4. **Make the "inversion test" a first-class check for claims.** Much slop consists of non-claims ("X plays a crucial role in Y") that survive negation as absurd — this is your strongest differentiator from prior art and aligns with the over-attribution/undue-emphasis findings.

5. **Explicitly document the false-positive risk and the ESL/accessibility counterargument** in the skill's README. This is both ethically necessary and a credibility differentiator.

6. **Prefer verification artifacts over style edits.** Where possible have the skill demand grounding (sources, reproducible examples, tests) rather than just rewriting prose — this attacks the generation/verification asymmetry that causes slop.

Thresholds to revisit the design: a reliable low-FPR detector; a shift in platform norms toward mandatory provenance (C2PA/SynthID ubiquity post-EU-Article-50, Aug 2026); or new corpus studies overturning the current marker set.

## Caveats

- **Contested figures:** "50%+ of the web is AI" (Graphite) and "57%" (AWS) are detector-dependent or mis-cited (AWS is about machine *translation*). Treat as directional, not precise.
- **Model collapse** is real in recursive-replacement setups but likely overstated as a near-term frontier-model threat given data accumulation + curation.
- **Detector reliability** is genuinely poor; any claim of high accuracy is usually a vendor self-report contradicted by independent testing.
- **Workslop/knowledge-decay** economics rest on self-reported survey estimates, not controlled measurement.
- **GitClear** data is correlational and produced by a vendor with an interest in the finding.
- Some markers (em dash, rule of three) are **formality/edited-prose signals** as much as AI signals; do not treat them as proof.
- Several recent (2026) figures come from security vendors and SEO firms with commercial interests; these are flagged inline.