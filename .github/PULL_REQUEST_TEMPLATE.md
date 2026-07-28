## Summary

<!-- What changed and why. If this fixes an issue, link it. -->

## The rules this project holds you to

- [ ] No authorship verdict is emitted, implied, or computed
- [ ] No stylistic marker can fail a build on its own
- [ ] Severity and confidence remain on separate axes
- [ ] No em dash or en dash added
- [ ] No local absolute paths added
- [ ] No credentials, tokens, or private content added

## Sources

- [ ] Every new factual claim cites a ledger id
- [ ] Any new ledger entry has a **real title copied from the document**, a
      resolving URL, `retrieved`, `refresh_due`, `source_type`,
      `evidence_tier`, and `claims`
- [ ] Limitations recorded where they apply: sample size, preprint status,
      vendor conflict of interest

## Verification

Run from `anti-slop-brain/`:

- [ ] `python3 -m compileall -q scripts tests`
- [ ] `python3 tests/test_scanners.py`
- [ ] `python3 tests/test_adapters.py`
- [ ] `python3 tests/test_pipeline.py`
- [ ] `python3 scripts/check_links.py --vault wiki`
- [ ] `python3 scripts/score_substance.py --vault wiki --ledger references/source-ledger.json --note-type concept,marker,procedure,surface`

## Tests

- [ ] Each fix has a test that **fails before the change and passes after**
- [ ] I verified the failing half by reverting my change and watching it fail

<!-- A test that only passes proves nothing about the bug it claims to fix. -->
