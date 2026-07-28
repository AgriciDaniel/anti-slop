# Security policy

## Scope

This project runs locally, makes no network calls by default, and stores no
credentials. The realistic risk surface is narrow but not empty.

| Area | Risk |
|---|---|
| `scan_packages.py --online` | queries public package registries; leaks the dependency names being checked |
| `scan_refs.py --online` | resolves DOIs and URLs found in the scanned file |
| `hooks/hooks.json` | **not skill-gated.** Runs `lint_voice.py` after every `Write` and `Edit`, in every session and every project, for as long as the plugin is installed |
| Adapter input | untrusted JSON is schema-validated before use, and refusals are structured |

Everything else is offline and standard library only. There are no third-party
runtime dependencies, so there is no dependency supply chain to compromise.

### The hook, in full, because you should know before you install

`anti-slop-plugin/hooks/hooks.json` registers one `PostToolUse` hook with
`"matcher": "Write|Edit"`. There is no condition on which skill is active, so:

- It fires on **every** `Write` and `Edit` you make, including in repositories
  that have nothing to do with this project.
- It runs `anti-slop-brain/scripts/lint_voice.py` over the file just written.
  On a house style hit it exits 2, which **blocks** the write and feeds the
  linter output back to the model to correct. House style here means no em
  dash, no en dash, no spaced double hyphen, plus banned tokens. That is a
  punctuation preference chosen by this repository's owner, and it will be
  applied to your files too.
- It is a silent no-op when the sibling `anti-slop-brain` directory is absent,
  when the tool input carried no `file_path`, or when the written path no
  longer exists.
- It is plugin-scoped in the sense that installing or removing the plugin
  installs or removes it. It writes nothing to `~/.claude/settings.json`.

If you want the linter without the global blocking behaviour, delete
`anti-slop-plugin/hooks/hooks.json` before installing, or install the skills
individually instead of the plugin directory, and run `lint_voice.py` yourself.
The `slop-rewrite` skill separately declares its own hooks in SKILL.md
frontmatter; those are scoped to that skill's lifecycle and only run while it
is active, which is the documented behaviour for skill frontmatter hooks.

## Reporting a vulnerability

Open a **private security advisory** through the GitHub Security tab rather
than a public issue.

Please include what you were running, what you expected, and what happened.
A reproducible case matters more than severity language: this project's own
documentation argues that unreproducible reports are the problem, so we hold
ourselves to the same standard when receiving them.

Expect an acknowledgement within seven days.

## What counts as a vulnerability here

In addition to the obvious, these are treated as security-relevant because the
project's guarantees depend on them:

1. **Bypassing the firewall.** Any input that causes an authorship verdict to
   be emitted, or that causes a Tier 2 or Tier 3 marker alone to produce a
   finding, or that merges severity and confidence into one score. One such
   bypass has already been found and fixed: a hand-written envelope skipped
   importer validation.
2. **A scanner passing content it should flag**, or flagging content it should
   not, in a way an author could exploit to launder a defect.
3. **A path traversal or arbitrary write** from adapter input or a vault path.
4. **Anything that makes a scanner non-deterministic**, since determinism is a
   stated guarantee and reviewers rely on it.

## What is not a vulnerability

- A false positive from a Tier 2 or Tier 3 marker. Those are documented as
  high false-positive by design and never fail a build alone.
- `scan_packages` reporting a real package as `unverified` in offline mode.
  Offline it enumerates rather than verifies, which is stated in its output.
- Disagreement with a marker's evidence tier. Open a normal issue with a
  source.
