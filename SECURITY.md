# Security policy

## Scope

This project runs locally, makes no network calls by default, and stores no
credentials. The realistic risk surface is narrow but not empty.

| Area | Risk |
|---|---|
| `scan_packages.py --online` | queries public package registries; leaks the dependency names being checked |
| `scan_refs.py --online` | resolves DOIs and URLs found in the scanned file |
| `hooks/hooks.json` | runs a linter on files you write while an anti-slop skill is active |
| Adapter input | untrusted JSON is schema-validated before use, and refusals are structured |

Everything else is offline and standard library only. There are no third-party
runtime dependencies, so there is no dependency supply chain to compromise.

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
