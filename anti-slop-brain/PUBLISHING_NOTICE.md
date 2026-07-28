# Publishing Notice

This directory is published as part of the public
[`anti-slop`](../README.md) repository. That is the distribution model, and it
is not incidental: the project's whole argument is that a claim you cannot
inspect is worth nothing, so the evidence has to ship with the claims.

An earlier version of this file was generator boilerplate written for a
different model, a private client vault, and it listed the source ledger, the
vault logs and the Obsidian config as things that must never be published. All
four were already published, deliberately. That contradiction is the reason
this file was rewritten rather than trimmed.

## The rights boundary

This notice states the rights boundary for this project: what can be public,
what must stay private, and who is accountable for the difference.

Two things make the boundary unusual here. The source ledger and the claim
ledger are deliberately public, because an evidence argument nobody can inspect
is not an evidence argument. And `.raw/` source evidence stays immutable
whether or not it is published, which is a separate rule from secrecy and is
set out below.

## The rule this file exists to hold

**Publish the evidence. Do not publish other people's material or anybody's
secrets.**

Everything below follows from that one sentence.

## Deliberately public, because the argument depends on it

| Artifact | Why it is public |
|---|---|
| `references/source-ledger.json` | The centrepiece. Every numeric claim in the repository resolves to an id in here, carrying a URL, a retrieval date, a refresh date, an evidence tier and stated limitations. Hiding it would leave the claims unfalsifiable, which is the defect this project exists to catch |
| `references/claim-ledger.md` | Records which claims rest on a single source and which were second-sourced. The single-source rows are the ones a critic should attack first, so they have to be visible |
| `wiki/` | The vault itself, including `hot.md` and `log.md`. The log records this project's own errors, including a false verification claim in its own limitations note. A corrections log that nobody can read is not a corrections log |
| `wiki/meta/dashboard.md` | Materialised counts, so a reader can check them against `find` rather than take them on trust |
| `.obsidian/` | Tracked in two places only, `examples/sample-vault/.obsidian` and `assets/template-brain/.obsidian`, so the demo output and the scaffold template each open as a working Obsidian vault rather than a bare folder of Markdown. `wiki/` ships no `.obsidian` of its own: opening it in Obsidian creates a fresh local config, which is untracked |
| `examples/sample-vault/` | The demo output, regenerated deterministically by `scripts/build_demo_vault.py`. CI diffs it, so a drifting demo fails the build |
| `research/verification-ledger.md`, at the repository root | The adversarial pass over the research base, including the corrections to figures this field repeats incorrectly |

Public here means published, not unowned. Reuse is governed by the split
licence at the repository root: Apache 2.0 for code, CC BY-SA 4.0 for the
Wikipedia-derived marker material, CC BY 4.0 for other prose.

## Must not be published

These are real exclusions, and none of them is currently in the repository.

- **Credentials of any kind.** API keys, tokens, cookies, OAuth material,
  private keys. Release packaging scans for them and refuses.
- **Private client or operator material.** Vaults built with
  `anti-slop-brain new <client>` are the operator's, not this repository's.
  Nothing from a client vault belongs here, including its `.raw/` captures, its
  logs, and its deliverables.
- **Local absolute paths.** Wrong on every other machine, and CI fails on them.
- **Full third-party documents or large source excerpts.** Public availability
  of a source does not create permission to redistribute it. Link, summarise,
  and quote within the quote policy. The one archived third-party snapshot,
  Wikipedia's wikitext for the Signs of AI writing guide, is CC BY-SA 4.0 and
  attributed in `THIRD_PARTY_NOTICES.md`; it is kept out of the published tree
  under a gitignored `.research/` directory because a link plus attribution
  serves the reader better than a mirrored copy.
- **Unreviewed generated archives.** `dist/` holds release ZIPs produced by
  `scripts/package_release.py`. They are release outputs and are reviewed
  before they are attached to a release.

## `.raw/` is immutable, which is a separate rule from secrecy

`.raw/` holds captured source material and `.raw/.manifest.json` holds a
SHA-256 for each capture. The immutability rule still applies in full: **never
edit a file under `.raw/` after capture.** Provenance traces resolve to those
hashes, and an edited capture silently invalidates every deliverable that cites
it. If a source changed, capture it again as a new entry.

Immutability is not the same as privacy. In this repository the one shipped
capture, `examples/sample-vault/.raw/sources/sample-source.md`, is a fixture
written for the demo and is published on purpose. In an operator's client vault
the captures are the client's and stay private. Both follow the same rule: do
not edit them, and do not publish material that is not yours to publish.

## Review before publishing or cutting a release

1. `python3 scripts/audit_brain.py --json`
2. `python3 scripts/lint_vault.py --vault examples/sample-vault`
3. `python3 scripts/check_links.py --vault wiki`
4. `python3 scripts/build_demo_vault.py`, then confirm `git status` is clean.
   A dirty tree means the demo is not deterministic.
5. Secret scan across tracked and untracked files.
6. Confirm no local absolute path is in any tracked file.
7. `python3 scripts/package_release.py --version <v>`, which repeats the secret,
   local-path, symlink, untracked-drift and unsafe-ZIP-entry scans and writes
   `dist/RELEASE_MANIFEST.json` and `dist/SHA256SUMS`.
8. If a Quartz site is being built, run `node site/scripts/sanitize-public.mjs`
   after the build, and confirm repository visibility and Pages visibility
   separately.
