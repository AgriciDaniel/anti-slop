# Contributing

**The contributing rules for this directory live at the repository root:
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).** There is one set of rules and
that is it. This file is a pointer so nobody reads a different policy by
walking into the subdirectory first.

Read the root document before opening a pull request. The rules that catch
people out are the ledger-source requirement for every factual claim, the ban
on em dashes and en dashes, the ban on local absolute paths, and the
requirement that every fix ships with a test verified to fail before the fix.

## The part that is specific to this directory

Commands below run from `anti-slop-brain/`.

```bash
python3 -m compileall -q scripts anti_slop_brain tests
python3 tests/test_scanners.py     # 107 checks
python3 tests/test_adapters.py     # 207 checks
python3 tests/test_pipeline.py
python3 scripts/check_links.py --vault wiki
python3 scripts/score_substance.py --vault wiki \
  --ledger references/source-ledger.json \
  --note-type concept,marker,procedure,surface
python3 scripts/audit_brain.py --json
```

If you touched `examples/sample-vault/`, regenerate it rather than editing it
by hand, then confirm the tree is clean:

```bash
python3 scripts/build_demo_vault.py
git status --short examples/
```

CI diffs that directory, so a hand edit that the generator would not reproduce
fails the build.

Before editing a vault note, read `docs/PRODUCT_BOUNDARIES.md` and
`wiki/meta/Note Conventions.md`. Before publishing anything from here, read
`PUBLISHING_NOTICE.md`. Raw captures under `.raw/` are immutable after capture:
their SHA-256 hashes are what provenance traces resolve to.
