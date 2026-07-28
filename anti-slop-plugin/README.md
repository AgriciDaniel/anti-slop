# anti-slop

A Claude Code plugin that finds and repairs AI slop in prose, code,
documentation, commit messages, pull request descriptions and agent output.

**It reports defects. It does not report authorship.** There is no percentage,
no score, no verdict about who or what wrote anything, and there is no way to
make it produce one. Section [Limits](#limits-stated-honestly) explains why that
is a design constraint rather than a disclaimer.

---

## What makes this different

Most tools in this space remove the *signs* of machine writing. This one is
built around the objection to that approach, which comes from the upstream
source those tools were built from:

> The patterns listed here are also only potential **signs** of a problem, not
> **the problem itself**. Please do not merely treat these signs as the problems
> to be fixed; that could just make detection harder.
>
> Wikipedia:Signs of AI writing, retrieved 2026-07-27

Strip the em dashes from an unsourced paragraph and you still have an unsourced
paragraph, now with the warning label removed. So this plugin puts the
deterministic, harmful defects first (fabricated citations, packages that do
not exist, vendor residue, placeholder text) and treats stylistic markers as
what they are: a way of choosing which sentence to test next.

The second constraint is measurement. A model cannot reliably judge slop.
LLM-as-judge agreement with human slop labels is near zero (kappa 0.01 for
GPT-5, minus 0.01 for DeepSeek-V3, 0.03 for o3-mini; Shaib, Chakrabarty,
Garcia-Olano and Wallace, arXiv 2509.19163, rev. 2026-01-24), models under-flag
by roughly five times, and span-level extraction runs at precision 0.14 and
recall 0.11. So the plugin never asks a model whether something looks like
slop. It asks the model to perform an operation and report what happened.

---

## The three layers

**Layer 0, deterministic scanners.** Python scripts with exit codes: 0 clean,
1 findings, 2 usage error. These are the only things allowed to hard-fail,
because they are the only things actually decidable. They live in the sibling
repository at `../anti-slop-brain/scripts/`.

| Script | Decides |
|---|---|
| `scan_residue.py` | vendor artifacts: `oaicite`, `[cite: 1]`, lenticular-bracket citations, `(start_span)`, `grok-card`, `:::writing{`, `[attached_file:1]`, `utm_source=chatgpt.com`, `referrer=grok.com` |
| `scan_placeholders.py` | `[Your Name]`, `INSERT_SOURCE_URL`, `access-date=2025-XX-XX`, `YYYY-MM-DD`, `TODO: quote` |
| `scan_refs.py` | DOI, ISBN and arXiv shape and checksums offline; resolution over the network with `--online` |
| `scan_packages.py` | dependency inventory offline; registry existence with `--online` |
| `lint_voice.py` | house style: no U+2014, no U+2013, no spaced double hyphen, plus banned tokens from a voice file |
| `score_substance.py` | near-duplicate, skeleton-reuse and specific-word-density floors over a note vault (`--vault DIR`) |

**Layer 1, structural procedures.** Five mechanical tests. Each one produces a
named artifact: a concrete thing you can hand to someone who does not trust the
reviewer. A test that was not actually run produces no artifact and therefore
no finding.

**Layer 2, evidence-tiered soft signals.** Markers, ranked by how well the
corpus evidence supports them, each carrying its own citation and its own
false-positive class. A Layer 2 hit does exactly one thing: it selects a span
for a Layer 1 test.

- **Tier 1, corpus-validated.** Excess vocabulary, puffery and undue emphasis,
  over-attribution, negative parallelism, tricolons, hesitancy markers.
- **Tier 2, measured but high false positive.** Em-dash density, burstiness,
  uniform sentence length. Never fails anything alone.
- **Tier 3, folk wisdom.** Individual words in isolation. Recorded so it can be
  argued with, never acted on.

---

## The five structural tests

1. **Deletion.** Cut the span. Name what was lost. If nothing was lost, it was
   padding. Artifact: the cut span plus the named loss.
2. **Inversion.** Negate the claim and write the negation out. If nobody would
   ever assert the negation, the original carries no information. Artifact: the
   negation, in full.
3. **Stranger.** Could someone who never read the source have written this? If
   yes, it is generic. Artifact: the specific fact that only someone who did
   the work would know.
4. **Attribution.** Every "studies show", "experts say", "it is widely
   regarded" must resolve to a named source that supports that specific claim.
   Artifact: the resolved citation, or the finding that it does not resolve.
5. **Load-bearing (code).** Delete the comment, the wrapper, the try/except,
   the assertion-free test. Artifact: what broke, or nothing broke, with the
   evidence.

Worked examples of every artifact format are in
[`references/structural-tests.md`](references/structural-tests.md).

---

## The firewall

Four rules bind every skill and agent in this plugin. They are standing
instructions, not checklist steps, and they hold even when the user asks for
the opposite.

1. **Never emit an authorship verdict.** Report defects, not origin.
2. **Never hard-fail on a stylistic marker alone.** A marker is a routing hint.
   Its only legitimate output is "run a structural test on this span".
3. **Severity is impact. Confidence is certainty.** Two axes, never merged into
   one score, never traded against each other.
4. **Never let the model gate its own rewrite.** The deterministic scanners
   re-run after any fix and their exit codes decide.

Rule 4 exists because self-gating has been measured: Song, Cai and Zhao, arXiv
2606.28438, 2026-06-26, found AI self-review gates entering a "rubber-stamp
regime where acceptance scores rise while benchmark correctness falls".

Rule 1 exists because false accusation has a measured victim. See
[Limits](#limits-stated-honestly).

---

## What is in the box

```
anti-slop-plugin/
  .claude-plugin/plugin.json
  skills/
    anti-slop/SKILL.md          router hub, picks the leaf skill
    slop-review/SKILL.md        read-only findings, no Write or Edit tool
    slop-rewrite/SKILL.md       consumes findings, never re-derives them
    slop-code/SKILL.md          code, tests, config, commits, PR text
    slop-verify/SKILL.md        citations, links, packages, vendor residue
  agents/
    slop-grader.md              bounded read-only second opinion
    slop-verifier.md            fresh-context adversarial check of a review;
                                not read-only, also holds Bash and WebFetch
  references/
    structural-tests.md         the five tests, worked
    markers-tier1.md            corpus-validated markers
    markers-tier2.md            measured but high false positive
    markers-tier3.md            folk wisdom, recorded and unusable
    code-markers.md             code-specific defects and the split evidence
    false-positives.md          what not to flag, and the ethics
  hooks/hooks.json              house style gate; not skill-gated, fires on
                                every Write and Edit in every project
  README.md
```

`slop-review` declares `disallowed-tools: Write, Edit, NotebookEdit` so it
cannot helpfully rewrite what it is supposed to be judging. Note the trap this
avoids: `allowed-tools` on a skill is permission pre-approval, not a
restriction. Only `disallowed-tools` restricts.

---

## Install

**Requirements.**

- Claude Code.
- Python 3.
- The sibling repository `anti-slop-brain` checked out next to this plugin, in
  the same parent directory. The Layer 0 scanners live there. Without it, the
  structural tests still work, the deterministic layer does not, and every
  skill will tell you so rather than substituting judgement for a scanner.

Expected layout:

```
anti-slop/
  anti-slop-plugin/     this repository
  anti-slop-brain/      scanners, wiki, source ledger
```

**Local install.**

```sh
git clone https://github.com/AgriciDaniel/anti-slop.git
cd anti-slop
claude plugin validate ./anti-slop-plugin
ln -s "$PWD/anti-slop-plugin" ~/.claude/skills/anti-slop
```

Anything under `~/.claude/skills/<name>/` auto-loads on the next session as
`<name>@skills-dir`. Confirm with `claude plugin list`.

**Marketplace install.** Not yet published. When it is, the path is
`/plugin marketplace add AgriciDaniel/anti-slop` followed by
`/plugin install anti-slop@anti-slop`.

**Verify.**

```sh
python3 ../anti-slop-brain/scripts/scan_residue.py --help
python3 ../anti-slop-brain/scripts/lint_voice.py README.md ; echo "exit=$?"
```

**Uninstall.** Remove the symlink. The hook goes with it; nothing was written
to `~/.claude/settings.json` and nothing global was changed.

---

## Use

| Ask | Skill |
|---|---|
| "review this", "what is wrong with this draft" | `slop-review` |
| "fix it", "clean this up", "de-slop this" | `slop-rewrite` |
| code, tests, comments, READMEs, commits, PR descriptions | `slop-code` |
| citations, DOIs, dead links, imported packages, vendor residue | `slop-verify` |
| not sure | `anti-slop`, the router |

Order matters when more than one applies. `slop-verify` first, because
fabricated citations and hallucinated packages are the only HIGH-severity
defect class a rewrite can silently launder. Then `slop-review`. Then
`slop-rewrite`, which consumes the review's findings and never re-derives them.

**The hook.** `hooks/hooks.json` registers a `PostToolUse` hook on `Write` and
`Edit` that runs the voice linter over the file just written. On a house style
violation it exits 2, which is the blocking code: the linter output is fed back
so the model can correct itself. Exit code 1 would be silently ignored, which
is why the wrapper translates the linter's own exit 1 into 2. The hook is a
silent no-op when the sibling repository is absent. It is scoped to this
plugin, so installing or removing the plugin installs or removes it.

`lint_voice.py` enforces **house style**, chosen by the operator. A hit is a
style violation and never evidence about a text's origin.

---

## Limits, stated honestly

**It does not detect AI authorship, and it cannot be used to accuse anyone.**

That is not caution, it is the finding. Stowe, Afanaseva, Raimundo, Sun and
Patil (Pindrop), ACL 2026, peer reviewed, arXiv 2512.09292, ran 16 detection
models over student essays labelled for gender, race and ethnicity,
English-language-learner status and socioeconomic status. English-language
learners were disproportionately flagged. Non-White ELL students were
disproportionately flagged relative to White ELL peers. **Human annotators on
the same essays showed no significant demographic bias.** The bias is a
property of automating the judgement, not of the judgement.

Every defect this plugin reports is a defect regardless of who produced it, and
every one is fixable by the author without any admission about process. That is
the entire design. There is no percentage in this plugin, no score, and no way
to coax one out of it.

**Other limits, without softening.**

- **Markers rot, and this set will.** Vocabulary cohorts shift by model
  generation, and human usage is converging on model usage: Yakura et al.,
  arXiv 2409.01754, measured delve up 48 percent, realm up 35 percent and adept
  up 51 percent in spontaneous human speech within 18 months of ChatGPT's
  release. Every marker entry carries its retrieval date for this reason.
- **Several 2026 citations are arXiv preprints verified at abstract level
  only.** Those are tagged CONTESTED in the source ledger and flagged inline
  wherever they are used.
- **Rewriting can make things worse, measurably.** Across commercial
  humanizers, the best tier wins a fluency comparison against the original only
  26.0 percent of the time, and the paper's own conclusion is that all
  humanizers tend to degrade the quality of the original text (DAMAGE, Masrour,
  Emi and Spero, GenAIDetect at COLING 2025, arXiv 2501.03437). `slop-rewrite`
  is deliberately conservative and refuses to run without a findings report.
- **The evidence on machine-written code is genuinely split**, and this plugin
  presents both sides rather than picking one. The strongest degradation
  figures come from vendors selling engineering-intelligence products; the
  strongest null result is Borg et al., arXiv 2507.00788, a preprint rather than
  a published paper, pre-registered with In-Principle Acceptance granted at
  ICSME, 151 participants: Phase 2 found no significant differences in code
  evolution, completion time or quality, while Phase 1, observational, found a
  30.7 percent median reduction in completion time. Both phases belong in any
  citation of it. See
  [`references/code-markers.md`](references/code-markers.md).
- **The deterministic layer needs the sibling repository and, for resolution
  and registry checks, the network.** `scan_refs.py` and `scan_packages.py`
  default to offline and require `--online` to decide anything. An offline run
  is not a clean bill of health, and the skills are instructed to say so.
- **`score_substance.py` scores a note vault, not an arbitrary file.** It takes
  `--vault DIR` and a frontmatter `--note-type`. It is not a general prose
  scanner.
- **`allowed-tools` in `plugin.json` is inert.** `claude plugin validate`
  accepts it and `claude plugin validate --strict` rejects it as an
  unrecognized field. It is kept because the sibling brain's audit rubric
  requires the declaration; it does nothing at load time either way.
- **This plugin has no test suite of its own.** The scanners it drives are unit
  tested in the sibling repository. The skills and references are prose and are
  verified by the `slop-verifier` agent and by review.

---

## Prior art and credits

**Wikipedia:Signs of AI writing** and **Wikipedia:WikiProject AI Cleanup**
(https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), retrieved
2026-07-27, used under **Creative Commons Attribution-ShareAlike 4.0
International (CC BY-SA 4.0)**. The marker taxonomy, the words-to-watch lists,
the citations and markup defect categories, the ineffective-indicators list,
the cluster rule, the era-dependence of the vocabulary cohorts, and the
doctrine that the signs are not the problem itself all come from that guide.
The adapted material is in `references/markers-tier1.md`,
`references/markers-tier2.md`, `references/markers-tier3.md`,
`references/code-markers.md` and `references/false-positives.md`, and each file
carries the attribution. Adaptations of that material remain under CC BY-SA
4.0. The rest of this plugin is Apache-2.0 for code and CC BY 4.0 for prose. See LICENSE-CONTENT in this directory.

**blader/humanizer** (https://github.com/blader/humanizer), MIT, v2.9.1 as of
2026-07-22, is the best packaged prior art in this space and is credited as
**comparative prior art**. No text was copied from it. Its packaging discipline
is worth copying and was: a hard line budget per skill file, version sync
enforced in CI, and no tool preapprovals. Its substance is where this plugin
diverges, and the divergence is documented rather than implied: humanizer
removes the signs and has no coverage of fabricated citations, vendor residue
markers, or code, and its no-fabrication rule is a prompt instruction with no
verification mechanism. This plugin puts a scanner behind each of those.

Corpus evidence is cited inline throughout `references/`. The full source
ledger, with retrieval dates, refresh dates, confidence, evidence tier and
recorded limitations for every source, is in the sibling repository at
`../anti-slop-brain/references/source-ledger.json`. Nothing in this plugin
quotes a figure that is not in that ledger or in the project's verification
ledger.

---

## Licence

Apache-2.0 for code and CC BY 4.0 for prose, except for material adapted from Wikipedia:Signs of AI writing, which
remains under CC BY-SA 4.0 and is attributed at the point of use.
