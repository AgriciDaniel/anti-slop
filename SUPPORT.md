# Support

## Questions about using it

Open a **GitHub Discussion** if the repository has them enabled, otherwise an
issue labelled `question`.

Before asking, the fastest answers are usually already written down:

| Question | Where |
|---|---|
| What is this, in one page | `README.md` |
| Why not just use an AI detector | `anti-slop-brain/wiki/detection/Why Detection Fails.md` |
| Why not just ask a model | `anti-slop-brain/wiki/procedures/Why Structural Not Judgmental.md` |
| What are the five tests | `anti-slop-brain/wiki/procedures/` |
| What will it refuse to claim | `anti-slop-brain/wiki/counterarguments/What This Brain Does Not Claim.md` |
| Where did a number come from | `anti-slop-brain/references/source-ledger.json` |
| Which figures are wrong in the wild | `research/verification-ledger.md` |

## Reporting a defect in this project's own accuracy

This is the most valuable kind of report and it gets priority. If a citation
does not say what a note claims, or an identifier resolves to a different
paper, open an issue with the source URL and what it actually says.

There is precedent. An adversarial review found five ledger entries whose
titles matched no real paper, and a false verification claim in the file that
exists to state limits. Both are documented in `anti-slop-brain/wiki/log.md`
rather than quietly fixed.

## Reporting a security issue

Use a private security advisory. See `SECURITY.md`.

## What is not supported

- Using this to determine whether a person used AI. It cannot do that, it is
  built so it cannot, and requests to add it will be declined.
- Evading AI detectors. Removing the surface signs while leaving the substance
  defects is the failure mode this project exists to argue against.
