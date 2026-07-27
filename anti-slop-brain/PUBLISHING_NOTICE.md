# Publishing Notice

Anti-Slop Brain is operator-owned research infrastructure. It is not public-ready until source review, rights review, vault lint, audit, and release packaging pass.

## Rights Boundary

Public availability of a source does not automatically create permission to redistribute it. Treat copied source excerpts, screenshots, account exports, prompt text, private notes, and third-party documentation as restricted evidence unless a clear license permits reuse.

Public content policy: publish summaries, links, and compliant short quotes only.

## What Can Be Public

- Original summaries.
- Operating doctrine.
- Links to official public sources.
- Short compliant quotations within the quote policy.
- Sanitized visuals and reports that do not expose raw captures or private data.

## What Must Stay Private

- `.raw/` source captures and `.raw/.manifest.json`.
- Credentials, tokens, cookies, OAuth material, private user data, and local paths.
- Full third-party documents or large source excerpts.
- Internal ledgers excluded by public policy.
- Unreviewed generated archives in `dist/`.

## Public Exclusions

- `.raw`
- `.obsidian`
- `hot.md`
- `log.md`
- `references/source-ledger.json`
- `references/claim-ledger.md`

## Review Checklist

1. Run `python scripts/lint_vault.py --vault examples/sample-vault`.
2. Run `python scripts/audit_brain.py --json`.
3. Run a secret scan across tracked and untracked files.
4. Confirm `.raw/` is absent from public artifacts.
5. Run `node site/scripts/sanitize-public.mjs` after a Quartz build.
6. Confirm repository visibility and Pages visibility separately.
