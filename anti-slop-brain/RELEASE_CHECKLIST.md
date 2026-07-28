# Release Checklist

**Last run 2026-07-28, against `anti-slop-brain` at version 0.1.0, by hand plus
the commands quoted below.** Ticks record what was verified on that date and by
what. An unticked box is honest and means the check was not run or could not be
run here; a wrongly ticked box is the exact defect this project exists to
catch, so leave it unticked when in doubt.

Re-run this list before every release. A tick does not survive a change to the
thing it was verifying.

## Product

- [x] README states buyer, promise, outputs, boundaries, and quick start.
      All five headings are present in `README.md`.
- [x] `SKILL.md` maps commands accurately. Every command it documents (`new`,
      `ingest`, `synthesize`, `report`, `visuals`, `lint`, `next`) is a real
      subparser in `anti_slop_brain/cli.py`.
- [x] License and distribution stance is explicit. `LICENSE`, plus the
      repository-root `LICENSE`, `LICENSE-CONTENT` and `NOTICE`, plus the
      licence table in the root `README.md`. The split is Apache 2.0 for code,
      CC BY-SA 4.0 for Wikipedia-derived marker material, CC BY 4.0 for other
      prose.
- [x] Third-party notices are current. `THIRD_PARTY_NOTICES.md` names five
      items with source, licence and what was taken.

## Research

- [x] Maturity is documented and not overstated. `README.md` states
      market-ready and names the command that produced it and the date it ran.
- [x] `references/current-requirements.md` has dated official/primary sources.
- [x] `references/source-ledger.json` lists dated official/primary sources,
      refresh dates, source types, and supported claims. 43 entries, each with
      `retrieved`, `refresh_due`, `source_type`, `evidence_tier`, `claims` and
      `limitations`.
- [x] `references/source-map.md` explains import strategy and source schemas.
- [x] `references/safety-gates.md` lists refusal rules and failure paths.
- [x] Stale source claims were browsed and refreshed before release.
      `audit_brain.py` reports 0 overdue and 0 inside the 14 day warning band;
      the earliest `refresh_due` is 2026-08-26, 29 days out.

## Vault

- [ ] Template vault opens in Obsidian. Not verified here: this needs a human
      opening `assets/template-brain/` in the Obsidian application. The
      `.obsidian/` config ships, and `lint_vault.py` passes, but neither of
      those is the same check.
- [x] Hot/Index/Wiki notes and hubs are connected. `check_links.py --vault
      wiki` reports 62 notes and every wikilink resolving.
- [x] Raw sources stay immutable under `.raw/`. Each capture is recorded in
      `.raw/.manifest.json` with a SHA-256, and nothing writes back to it.
- [x] Deliverables cite source notes or raw-file hashes. `Health Scorecard.md`
      carries a source-coverage table with the raw file hash and retrieval date.
- [x] `PUBLISHING_NOTICE.md` has been reviewed before public publish or ZIP
      release. Rewritten 2026-07-28 after review found it forbade publishing
      artifacts this project publishes on purpose.

## Verification

- [x] `python -m compileall scripts anti_slop_brain tests`
- [x] `python tests/test_pipeline.py`. Also `tests/test_scanners.py`, 107
      checks, and `tests/test_adapters.py`, 207 checks. All pass.
- [x] `python scripts/build_demo_vault.py --reference-date 2026-07-28`, which is
      the form CI runs, followed by the `git diff --exit-code` step in
      `.github/workflows/ci.yml` over `examples/sample-vault` and
      `references/canon`. Run-to-run determinism is verified: two consecutive runs
      produce byte-identical output. The committed vault now matches a fresh
      regeneration: `python3 scripts/build_demo_vault.py` followed by
      `git diff --exit-code -- examples/sample-vault references/canon` exits 0.
      Always pin the reference date; without it the run is dated from the clock
      and the diff means nothing.
- [ ] `python scripts/package_release.py --version 0.1.0`. Not re-run in this
      pass. The existing `dist/RELEASE_MANIFEST.json` was generated
      2026-07-28T01:19:45+00:00, records all four of its scans as passed, and
      its checksums verify against the ZIPs with `sha256sum -c SHA256SUMS`.
      That is evidence it ran before, not evidence it passes now.
- [x] No secrets, private client data, or local absolute paths in artifacts.
      Grepped every tracked file for API key, token and private-key patterns:
      zero matches. Grepped for the three home-directory prefixes the CI gate
      looks for: the only match is the CI step that implements that gate. The
      gate itself is the `No local absolute paths` step in
      `.github/workflows/ci.yml`; do not paste its patterns into a document in
      this directory or you will trip it.
- [x] Market-ready release is blocked unless audit score is at least 90 with no
      critical failures. `audit_brain.py --json` returns score 100, status
      `market-ready`, all eleven categories at 100, zero critical failures and
      zero warnings.
- [x] `references/adapter-manifest.json` names real schemas, importer paths,
      synthesis modules, report renderers, fixtures, and tests before
      domain-adapted or market-ready release. `test_adapters.py` asserts each
      named path exists, and its 207 checks pass.

## Known gap carried into this release

`dist/RELEASE_MANIFEST.json` records `"release_type": "scaffold"` because the
packaging run predates the market-ready audit. Re-run
`package_release.py --version <v> --release-type market-ready` before
attaching artifacts to a public release, so the manifest and the audit agree.
