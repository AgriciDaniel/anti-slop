# Support

**Support for this directory is the repository's support policy:
[`../SUPPORT.md`](../SUPPORT.md).** That document lists where the common
answers already live, how to report a defect in this project's own accuracy,
which is the most valuable kind of report, and what is explicitly not
supported.

Security issues do not go through support. Use a private GitHub security
advisory. See [`../SECURITY.md`](../SECURITY.md).

## If your question is about this directory specifically

Include the command you ran, your Python version, your operating system, and
sanitized output. Most problems here are one of three things:

| Symptom | Usually |
|---|---|
| A scanner or the CLI is not found | Commands run from `anti-slop-brain/`, not from the repository root |
| `scan_refs` or `scan_packages` exits 0 and you expected it to check something | Both are offline by default. Offline they check shape and checksums only. Pass `--online` to resolve references or query registries |
| `build_demo_vault.py` leaves `examples/` dirty | The sample vault was hand-edited. Regenerate it rather than editing it; CI diffs that directory |

Scanner exit codes are 0 clean, 1 findings, 2 usage error. A finding is a
mechanical defect report and never a statement about who or what wrote the
text.
