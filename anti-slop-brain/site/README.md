# Anti-Slop Brain Site

`site/` is the sanitized Quartz publish surface for the public subset of the vault.

Content should be built from the reviewed wiki only. Do not publish `.raw/`, source captures, internal ledgers, credentials, local paths, or private client data.

Public exclusions: .raw, .obsidian, hot.md, log.md, references/source-ledger.json, references/claim-ledger.md.

After a build, run:

```bash
node site/scripts/sanitize-public.mjs
```

Review `PUBLISHING_NOTICE.md` before publishing.
