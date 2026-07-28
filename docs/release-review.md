# Public release review

Scope: everything tracked in this repository, judged against what a stranger
needs in order to trust, install, and legally reuse it. Written 2026-07-28.

**Status: all blockers and quality issues resolved 2026-07-28.** A separate
adversarial verification pass ran afterwards and found further defects,
including a false verification claim in the vault's own limitations note.
Those are recorded in `anti-slop-brain/wiki/log.md` and are also fixed. The
findings below are kept as the record of what was wrong, not as outstanding
work.

## Blockers, must fix before the repo is public

### B1. The LICENSE file forbids the thing you are about to do

`anti-slop-brain/LICENSE` is the Brainstein placeholder. It reads:

> Replace this file with the final license before distribution. Until then, all
> rights are reserved.

Publishing with that file in place means the repository is all-rights-reserved.
Nobody may legally fork, adapt, or run it, which defeats the point of putting
it out. There is also no LICENSE at the repository root, which is where GitHub
looks to display a licence badge.

### B2. Share-alike obligations are real and are not satisfied by a single MIT file

The marker taxonomies, the words-to-watch lists, and the ineffective-indicators
list in `anti-slop-plugin/references/` are adapted from Wikipedia's Signs of AI
writing guide, which is **CC BY-SA 4.0**. That licence is copyleft: adaptations
must stay under CC BY-SA 4.0 and must carry attribution.

The plugin README already states this correctly at lines 290 to 323. The
repository licence must not contradict it. A blanket MIT LICENSE at the root
would be a licence violation on those files.

The correct shape is a split, which is standard practice for projects mixing
original code with encyclopedic source material:

| Part | Licence | Why |
|---|---|---|
| Scanners, adapters, tests, schemas | permissive, MIT or Apache 2.0 | original work |
| Wikipedia-derived reference prose | CC BY-SA 4.0 | inherited, non-negotiable |
| Original wiki notes and brain content | your choice, CC BY 4.0 is a good fit | original prose |

### B3. Continuous integration will never run

`anti-slop-brain/.github/workflows/ci.yml` exists and is correct, but GitHub
only reads `.github/` at the **repository root**. As laid out, the workflow is
an ordinary file that nothing executes. Every quality claim this project makes
would go unverified on every push.

### B4. There is no root README

A visitor lands on a directory listing containing `PLAN.md`, `STATUS.md`, a
file named `compass_artifact_wf-a639de9d-87a5-5f8c-9363-441f24c102dd_text_markdown.md`,
and two subdirectories. Nothing explains what the project is, what the two
subdirectories are for, or which one to install.

### B5. Repository URLs point at two different repositories that do not exist

| File | Claims |
|---|---|
| `anti-slop-brain/.claude-plugin/plugin.json` | `github.com/AgriciDaniel/anti-slop-brain` |
| `anti-slop-brain/.claude-plugin/marketplace.json` | `github.com/AgriciDaniel/anti-slop-brain` |
| `anti-slop-plugin/.claude-plugin/plugin.json` | `github.com/AgriciDaniel/anti-slop` |
| `anti-slop-plugin/README.md` | clone `github.com/AgriciDaniel/anti-slop.git` |

This is one repository. Two of these are wrong whichever name is chosen, and
all of them currently 404.

## Should fix, quality and credibility

### S1. The status documents are stale and actively misleading

`STATUS.md` still says nineteen notes and the adapters are missing. They are
done. `PLAN.md` still says "Status: proposed, awaiting approval". A reader who
trusts either file will be misinformed about the state of the work. For a
project whose subject is unverified claims, shipping stale status text is the
worst available look.

### S2. The research artifact has a machine-generated filename

`compass_artifact_wf-a639de9d-87a5-5f8c-9363-441f24c102dd_text_markdown.md`
is a real research document with a filename that reads like debris. It also
contains the superseded figures that `wiki/evidence/Superseded Figures.md`
exists to correct, with no warning at the top of the file.

### S3. The plugin has no marketplace.json

`anti-slop-plugin/.claude-plugin/` contains only `plugin.json`. Without a
marketplace manifest, the documented install path is a manual symlink. The brain
has a `marketplace.json`; the plugin does not.

### S4. `allowed-tools` in plugin.json is rejected by strict validation

`claude plugin validate --strict` rejects `allowed-tools` as an unrecognised
field. It is retained because Brainstein rubric item C7.3 requires it. That
tension should be a comment in the file, not tribal knowledge.

### S5. Nothing enforces the house style at build time

The em-dash rule is currently held by convention plus a skill-scoped hook. The
repository has a working linter, `scripts/lint_voice.py`, that is not wired into
CI. One `grep` step in the workflow would make the guarantee real.

## Verified clean, no action needed

- **No secrets.** Scanned for keys, tokens, bearer strings and password
  patterns across every tracked file type. The only matches are documentation
  telling agents not to include credentials.
- **No local absolute paths** in tracked files. Two were found in vault notes
  during the build and removed.
- **No em or en dashes** in any deliverable.
- **Working tree clean**, five commits, consistent author identity.
- **`.research/` is gitignored**, so the raw Wikipedia wikitext snapshot and
  the verification ledger are not currently published. Whether they should be
  is a decision, not a defect. See the open question below.

## Open questions for the owner

1. **Licence pair.** Recommendation: Apache 2.0 for code, CC BY-SA 4.0 for the
   Wikipedia-derived references, CC BY 4.0 for original prose. Apache 2.0 over
   MIT because it grants patent rights explicitly and states contribution terms,
   which matters more for a tool people will run in CI.
2. **Canonical repository name.** `anti-slop` is the better public name; the
   brain is a component, not the product.
3. **Publish `.research/`?** It holds the verification ledger, which is arguably
   the most reusable artifact in the whole project, plus a 206 KB raw Wikipedia
   wikitext snapshot. Publishing the ledger is a strong credibility signal.
   Publishing the snapshot is legal under CC BY-SA with attribution but bloats
   the repository.
4. **Push, or prepare only?** This review prepares the repository. Creating a
   GitHub repository and pushing is an outward-facing action and is not taken
   without an explicit instruction.
