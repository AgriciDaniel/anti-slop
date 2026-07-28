# Security

**The security policy for this directory is the repository policy:
[`../SECURITY.md`](../SECURITY.md).** Read that one. This file is a pointer so
nobody reports through the wrong channel because they opened the
subdirectory first.

**Report privately through a GitHub security advisory, using the Security tab
on the repository.** Do not open a public issue, and do not include
credentials or private client data in anything you file.

The root policy also defines what counts as a vulnerability here beyond the
obvious, including firewall bypasses, scanners that can be made to launder a
defect, path traversal from adapter input or a vault path, and anything that
makes a scanner non-deterministic.

## What this directory contributes to that surface

- `scripts/package_release.py` gates every release on scans for common API
  keys, private keys, OAuth tokens, local home paths, symlinks, untracked
  drift, and forbidden or unsafe ZIP entries. A hit blocks packaging.
- `scripts/scan_refs.py --online` resolves DOIs and URLs found in the file
  being scanned. `scripts/scan_packages.py --online` queries public package
  registries and so discloses the dependency names being checked. Both are
  offline by default.
- Adapter input is schema-validated before use. Hand-writing an adapter
  envelope to skip importer validation was a real firewall bypass, and it is
  fixed and regression-tested.
- Captures under `.raw/` are immutable after capture and are hashed in
  `.raw/.manifest.json`. Silently editing one invalidates every deliverable
  that cites it.
- Vaults created with `anti-slop-brain new <client>` belong to the operator.
  Nothing from a client vault belongs in this repository. See
  `PUBLISHING_NOTICE.md`.
