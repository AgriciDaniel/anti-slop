# Anti-Slop: build plan

**Status: historical. Written 2026-07-27, before the build. Superseded and
kept as the record of what was planned, not as a description of what shipped.**
It was approved and built; where this document and the shipped repository
disagree, the repository is right. For what actually shipped, read the root
[`README.md`](../README.md) and [`CHANGELOG.md`](../CHANGELOG.md). For what a
public-release review found wrong afterwards, read
[`release-review.md`](release-review.md), which is also historical.

Evidence base, as it stands today:

| Source cited below | Where it is now |
|---|---|
| Verification ledger | Published at [`research/verification-ledger.md`](../research/verification-ledger.md) |
| The original research report, then named `compass_artifact_*.md` | Published, renamed, at [`research/ai-slop-research-report.md`](../research/ai-slop-research-report.md). It is a preserved archive and is the one file exempt from the house dash rule |
| `.research/prior-art-humanizer-wikipedia.md` | Not published. Working notes on prior art, kept locally under the gitignored `.research/` directory. Its conclusions are in this document and in the `blader-humanizer` entry of `anti-slop-brain/references/source-ledger.json` |
| `.research/raw/` | Not published. Raw captures, including the Wikipedia wikitext snapshot. Third-party material is linked and attributed rather than mirrored; see `anti-slop-brain/THIRD_PARTY_NOTICES.md` |

Anything below that names a `.research/...` path, or "the existing research
report", refers to that unpublished working directory as it stood on
2026-07-27. Those paths will not resolve in a clone. The two live pointers are
the first two rows of the table above.

---

## 1. The one finding that determines the architecture

**A model cannot reliably judge slop.** Shaib, Chakrabarty, Garcia-Olano and
Wallace (arXiv 2509.19163, rev. 2026-01-24) measured LLM-as-judge agreement
with human slop labels at **kappa 0.01 for GPT-5, -0.01 for DeepSeek-V3, 0.03
for o3-mini**. Models under-flag by roughly 5x. Span-level extraction runs at
precision 0.14 and recall 0.11.

Worse, the bias runs the wrong way. Judges prefer LLM-written text 89% of the
time versus humans at 36% (Laurito et al., PNAS 122(31), peer reviewed). Judge
preference tracks style, not factuality or safety (Feuer et al., ICLR 2025).
Markdown-heavy formatting is preferred over plain text with a style bias of up
to 0.76 (Soumik, TMLR 2026). And when a model gates its own output, acceptance
scores rise while correctness falls, a measured "rubber-stamp regime" (Song,
Cai, Zhao, arXiv 2606.28438, 2026-06-26).

So the skill must **never** ask "does this look like slop?" and act on the
answer. Every check has to be a mechanical procedure that emits a verifiable
artifact. That is the design constraint the whole build hangs on, and it is
what separates this from every existing tool in the space.

## 2. What the prior art gets wrong

`blader/humanizer` v2.9.1 (31,520 stars, MIT, last push 2026-07-22) is the best
packaged prior art and its distribution discipline is worth copying. Its
substance is not. Its own upstream source says so, in bold, in the guide it was
built from:

> The patterns listed here are also only potential **signs** of a problem, not
> **the problem itself**. Please do not merely treat these signs as the problems
> to be fixed; that could just make detection harder.
> (Wikipedia:Signs of AI writing, WP:AICATCH, retrieved 2026-07-27)

Humanizer removes the signs and leaves unverified claims, synthesis, and hollow
analysis intact. It also has zero coverage of the three things that actually
carry harm: **fabricated citations**, **vendor residue markers**, and **code**.
Its no-fabrication rule is a prompt promise with no verification mechanism.

Meanwhile the research is now clear that surface-level humanizing makes things
worse: "all humanizers tend to degrade the quality of the original text"
(DAMAGE, Masrour, Emi, Spero, GenAIDetect at COLING 2025). Best-tier tools win
a fluency comparison against the original only **26.0%** of the time.

## 3. Design: three layers, one firewall

### Layer 0, deterministic scanners (no model judgment at all)

Python scripts, exit codes, unit tested. These are the only things allowed to
hard-fail, because they are the only things that are actually decidable.

| Scanner | What it decides | Why it is safe to hard-fail |
|---|---|---|
| `scan_residue.py` | vendor artifacts: `oaicite`, `[cite: 1]`, `【85†…】`, `(start_span)`, `grok-card`, `:::writing{`, `[attached_file:1]`, `utm_source=chatgpt.com`, `referrer=grok.com` | near-deterministic, cheap to grep, no false-positive class |
| `scan_placeholders.py` | `[Your Name]`, `INSERT_SOURCE_URL`, `access-date=2025-XX-XX`, `YYYY-MM-DD`, `TODO: quote` | unambiguous defects |
| `scan_refs.py` | every DOI, ISBN, arXiv ID and URL resolves, and the DOI title matches the cited title | fabrication is checkable |
| `scan_packages.py` | every imported package exists in its registry | slopsquatting gate |
| `lint_voice.py` | house style: no U+2014, U+2013, ` -- `; banned tokens from a voice file | house rule, explicitly **not** a slop verdict |

`lint_voice.py` takes its rule set and its fence-aware and backtick-aware
behaviour from `lint_prose.py` in claude-blog 2.1.0, which solved that problem
first, but implements them here against `scan_common.py`. Wrapping the original
was tried and reverted: claude-blog is not published, so the wrapper resolved
on one machine and left the linter dead everywhere else.

### Layer 1, structural procedures (the model executes, and must show work)

Each test is mechanical and produces an artifact. No ratings, no scores from
vibes. This is where the deletion / stranger / inversion tests live, plus two
the evidence demands.

1. **Deletion test.** Cut the span. State what was lost. If the answer is
   "nothing", it was padding. Artifact: the cut span plus the named loss.
2. **Inversion test.** Negate the claim. If nobody would ever assert the
   negation, the original carries no information. "X plays a crucial role in
   Y" inverts to "X plays no role in Y", which nobody would write, so the
   original said nothing. Artifact: the negation, written out.
3. **Stranger test.** Could someone who never read the source have written
   this sentence? If yes, it is generic. Artifact: name the specific fact that
   only someone who did the work would know.
4. **Attribution test.** Every "studies show", "experts say", "it is widely
   regarded" must resolve to a named source that actually supports the
   specific claim. Covers RAG-era misattribution, where superficial analysis
   is stapled to a real source that does not support it. Artifact: the
   resolved citation, or the finding.
5. **Load-bearing test (code).** Delete the comment, the wrapper, the
   try/except, the assertion-free test. Does anything break or become
   unclear? Artifact: what broke, or nothing.

### Layer 2, evidence-tiered soft signals (trigger Layer 1, never fail alone)

Tiering follows the corpus evidence, and every tier records its own citation
and its own false-positive class.

- **Tier 1, corpus-validated.** Excess vocabulary (Kobak et al., Science
  Advances 11(27), 2025-07-02: at least **13.5%** of 2024 abstracts, up to
  **40%** in some subcorpora). Puffery and undue emphasis. Over-attribution.
  Negative parallelism. Tricolons at nearly twice expert rate and hesitancy
  markers at twice human density (Bakhshi, arXiv 2604.19768).
- **Tier 2, measured but high false-positive.** Em-dash density. Burstiness.
  Uniform sentence length. The em-dash citation is now Czuma, arXiv
  2606.29540, 2026-06-28, pre-registered on 69,632 medRxiv preprints, whose
  own conclusion is adopted verbatim: **"The em-dash is a population-level
  indicator, not a per-paper detector of LLM use."** Pangram's numbers are
  dropped: the page is undated, uncited, and states two different human
  baselines on the same page.
- **Tier 3, folk wisdom.** Individual words in isolation. Recorded, never
  acted on alone.

### The firewall

Four rules, stated in the skill and enforced in the reviewer's output schema:

1. **Never emit an authorship verdict.** The skill reports defects, not origin.
2. **Never hard-fail on a Layer 2 signal.** Signals route to Layer 1 tests.
3. **Severity is impact; confidence is certainty.** Two axes, never merged.
4. **Never let the model gate its own rewrite.** Layer 0 re-runs after any fix.

Rule 1 is not decoration. Detector bias against English-language learners is
now peer-reviewed and current: Stowe et al. (Pindrop), **ACL 2026**, arXiv
2512.09292, found ELL essays disproportionately flagged, non-White ELL students
disproportionately flagged versus White ELL peers, while **human annotators
showed no significant demographic bias**. This supersedes the 2023 Liang
finding the field usually quotes.

## 4. What gets built

### 4.1 The brain: `anti-slop-brain/`

A Brainstein v3 brain, targeting SSS+ (score at least 90, zero criticals) and
`market-ready` on the maturity ladder. Non-negotiable structural facts from the
generator contract:

- `slug` must end in `-brain`, so: `anti-slop-brain`.
- The scaffolder does **not** create `specs/`, a repo-root `wiki/`, or
  `tests/fixtures/sample-vault.sha256`. All three must be added by hand or the
  audit loses points and `brainstein upgrade` cannot resolve the spec.
- The domain string will contain "ai", which trips `FAST_MOVING_TERMS`. That
  forces the strict tier: **at least 2 primary sources and every `refresh_due`
  must parse and be in the future**, or it is a critical failure. Planning for
  the strict tier from the start.
- C8.1 requires a mean of 80+ lines per note and C8.2 requires 8+ wikilinks
  per note, across every wiki root.
- C8.3 requires `wiki/sources/research-pack-*.md` with at least 60 URLs and 60
  dates. The verification ledger already supplies most of that.
- C8.9 mechanically rejects em dashes and en dashes in SVG assets.

I will also port the **wiki substance scorer** from Claude Blog Brain
(`scripts/audit_brain.py:442`), which the Brainstein generator does not
produce. It is the single best anti-slop mechanism already on this machine and
it is thematically perfect here: near-duplicate detection at 0.82 similarity,
skeleton reuse, anchor reuse, generic citation-bundle reuse, a 120
note-specific-word density floor, and coverage floors of 0.90 for
table-or-procedure and 0.95 for specific citations. Caveat: `audit_brain.py` is
generator-owned, so `brainstein upgrade --apply` will clobber it. Documented in
the release checklist.

Wiki content, roughly 60 to 80 spoke notes across:
`concepts/` (slop as a category, distributional convergence, the
generation-verification asymmetry, mode collapse, sycophancy),
`markers/` (the tiered taxonomy, one note per marker class with its citation
and its false-positive class), `tests/` (the five structural procedures),
`surfaces/` (prose, code, docs, commits, PR descriptions, chat),
`detection/` (why detectors fail, provenance, watermarking, regulation),
`evidence/` (the corpus studies), `counterarguments/` (ESL bias, accessibility,
the moral-panic critique), plus the mandatory `gaps/`, `questions/`,
`experiments/`, `flows/` and `meta/` policy notes.

### 4.2 The plugin: `anti-slop/`

```
anti-slop/
  .claude-plugin/plugin.json        # allowed-tools declared (rubric C7.3)
  skills/
    anti-slop/SKILL.md              # router hub
    slop-review/SKILL.md            # read-only; severity x confidence; no rewrites
    slop-rewrite/SKILL.md           # consumes findings; never re-derives them
    slop-code/SKILL.md              # code and docs surface
    slop-verify/SKILL.md            # citations, links, packages
  agents/
    slop-grader.md                  # tools: Read, Grep, Glob (explicit, not inherited)
    slop-verifier.md                # fresh-context adversarial check
  scripts/                          # the Layer 0 scanners, all unit tested
  references/                       # tiered marker tables, loaded on demand
  hooks/hooks.json                  # optional, see decision 3
```

Authoring constraints taken from the live v2.1.220 contract:

- Non-negotiable rules go in the **first 5,000 tokens** of each SKILL.md.
  Auto-compaction keeps only that much per skill, under a combined 25,000-token
  budget. Everything after is deleted at first compaction.
- Write **standing instructions, not step lists**. "Never emit an authorship
  verdict" survives compaction; "step 4: check for verdicts" does not.
- The reviewer gets `disallowed-tools: Write, Edit` so it cannot helpfully
  rewrite what it is supposed to be judging. Note the trap: `allowed-tools` on
  a skill is permission pre-approval, **not** a restriction. Only
  `disallowed-tools` restricts.
- SKILL.md bodies stay under 500 lines; depth goes in `references/` with
  explicit load triggers.

### 4.3 Reuse, not reinvention

| Asset | Action |
|---|---|
| claude-blog `lint_prose.py` | reimplement its rules against `scan_common.py`, credit the design; wrapping it would add an unpublished dependency |
| claude-blog `style_learn.py` | reuse for per-author calibration, the honest answer to the ESL false-positive problem |
| claude-blog structural thresholds | generalize the 12 numeric diagnostics beyond blog prose |
| Claude Blog Brain substance scorer | port and adapt |
| claude-seo `content_humanize.py` | reuse but **demote** to last-mile assist behind the structural tests, never primary |
| claude-blog 100-point score, factcheck, GEO | call, do not clone |
| Gogh `[[AI Slop]]`, `[[Distributional Convergence]]` | cross-link; Gogh owns visual slop, this owns text, code and reasoning |
| Claude Blog Brain E-E-A-T notes | cross-link; it owns Google policy ground |
| RL Brain | cite for reward hacking and RLHF; it has **zero** coverage of sycophancy and mode collapse, so those two get written into it as the authoritative home |

## 5. Execution: multi-agent orchestration

Phases run in order; agents inside a phase run in parallel.

**Phase A, foundations (sequential).** `git init`. Write the spec YAML against
the hand-rolled parser's exact constraints (two-space list indent, no nested
maps, no folded scalars). Run `brainstein new`. Add the missing `specs/`,
repo-root `wiki/`, and `tests/fixtures/sample-vault.sha256`.

**Phase B, source ledger and research pack (2 agents, parallel).** Build
`references/source-ledger.json` from the verification ledger, in the v1 schema
shape, with strict-tier `refresh_due` dates. Build the 60+ URL research pack.
Every entry carries `retrieved`, `last_verified`, `refresh_due`, `source_type`,
`confidence`, `evidence_tier`, and `claims`.

**Phase C, wiki content (5 to 6 agents, parallel by folder).** Each agent owns
one folder, writes to the 80-line and 8-wikilink floors, and must cite from the
ledger. Enforced by the substance scorer, so no agent can pad its way through.

**Phase D, scanners and tests (3 agents, parallel).** Layer 0 scripts plus unit
tests. Each scanner ships with a test that proves it fires and a test that
proves it does not fire on the legitimate case.

**Phase E, skills and agents (2 agents, parallel).** The five SKILL.md files
and two subagents, written to the compaction-survival rules.

**Phase F, adversarial verification (fresh context, sequential).** A verifier
that never saw the build checks: every citation resolves and says what we claim,
no fabricated arXiv IDs, no em dashes anywhere, scanners actually fire, the
skill does not contradict itself, and the firewall rules hold. Then
`audit_brain.py --checklist`, iterate to SSS+.

**Phase G, release.** Commit, run the test suite, package.

Estimated 15 to 18 agent invocations across the phases.

## 6. Honest risks

- **The brain will be graded by its own subject matter.** An anti-slop brain
  padded to hit an 80-line floor is self-refuting. The substance scorer is the
  mitigation, and I would rather ship 60 dense notes than 200 thin ones even
  though C8.1 rewards volume.
- **Marker lists rot.** Vocabulary cohorts shift by model generation, and
  human speech is converging on LLM vocabulary (delve +48%, realm +35%, adept
  +51% within 18 months). Every marker note carries a `refresh_due` and an
  explicit "this will age" statement.
- **`brainstein upgrade --apply` will clobber the ported substance scorer.**
  Documented, with `--only` guidance in the release checklist.
- **Several 2026 citations are arXiv preprints verified at abstract level
  only.** They are tagged `contested` in the ledger, not `evidence-based`.
- **The WebSearch budget was exhausted during verification.** Three loose ends
  remain unresolved and are recorded as open questions rather than papered over.

## 7. Decisions needed before Phase A

1. Confirm the definitions of the deletion, stranger and inversion tests in
   section 3. They are referenced in the existing research report but defined
   nowhere on disk; section 3 is my reconstruction, not your original.
2. Confirm scope: brain plus plugin, or brain only.
3. Confirm whether to install a global style hook. This edits
   `~/.claude/settings.json`, which is outside ordinary workspace edits, so it
   needs explicit approval. Nothing currently enforces your em-dash rule at the
   harness level.
