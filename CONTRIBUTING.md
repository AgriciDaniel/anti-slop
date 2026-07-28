# Contributing

Thanks for considering it. This project has unusual rules, and they exist for
reasons rather than taste. Read this before opening a pull request.

## The one rule that matters most

**Every factual claim needs a source in the ledger, or it does not ship.**

`anti-slop-brain/references/source-ledger.json` is the only place a citable
source may come from. A pull request that adds a number, a percentage, a study
finding, or a marker frequency must either cite an existing ledger id or add a
new entry with:

| Field | Required | Why |
|---|---|---|
| `url` | yes | must resolve, must not be a placeholder host |
| `title` | yes | **the real title of the real document**, not a description of it |
| `retrieved` | yes | ISO date, not in the future |
| `refresh_due` | yes | when the claim needs re-checking |
| `source_type` | yes | from the accepted enum |
| `evidence_tier` | yes | see the downgrade rules in the ledger |
| `claims` | yes | one quotable sentence per claim you rely on |
| `limitations` | when it applies | sample size, vendor conflict, preprint status |

We got this wrong ourselves. Five entries once carried invented descriptive
titles that resolved to no paper. If you add a source, open the URL and copy
the title from the document.

## Rules that a reviewer will hold you to

1. **No authorship verdicts.** Nothing in this project may say, imply, or
   compute who or what wrote a piece of text. Detectors are unreliable and
   their failures fall on English-language learners. See
   `anti-slop-brain/wiki/counterarguments/The ESL Objection.md`.
2. **No hard failure on a stylistic marker alone.** Markers route to a
   structural procedure. Tier 2 and Tier 3 never convict by themselves.
3. **Severity and confidence stay on separate axes.** Severity is impact.
   Confidence is certainty. Never compute a single blended score.
4. **No model self-gating.** The deterministic scanners re-run after any
   repair. A model does not approve its own output.
5. **No em dash and no en dash.** Use commas, periods, colons, parentheses.
   This is a house style rule, not a claim about AI authorship, and CI enforces
   it. The one exemption is `research/ai-slop-research-report.md`, which is a
   preserved archive.
6. **No local absolute paths.** They are wrong on every other machine, and CI
   fails on them.

Both gates live in the `house-style` job of `.github/workflows/ci.yml`. They
scan `anti-slop-brain/`, `anti-slop-plugin/`, `docs/`, `research/`, `.github/`
and `.claude-plugin/`, plus the root Markdown, `.cff` and `.yaml` files, across
`*.md`, `*.py`, `*.json`, `*.yml`, `*.yaml`, `*.svg` and `*.cff`. Files without
an extension, such as `LICENSE` and `NOTICE`, are outside both greps.

## Adding or editing a vault note

The vault is graded by its own subject matter, mechanically.

```bash
cd anti-slop-brain
python3 scripts/score_substance.py --vault wiki \
  --ledger references/source-ledger.json \
  --note-type concept,marker,procedure,surface
python3 scripts/check_links.py --vault wiki
```

Floors your note must clear: at least two distinct ledger citations, at least
one table or numbered procedure, at least 120 note-specific words, similarity
below 0.82 against every other note.

**Vary your heading structure.** Notes written to a shared outline get caught
as template convergence, which is this project's own instance of the problem it
documents. If your note has the same H2 skeleton as three others, the scorer
fails the build and it is right to.

## Running everything locally

```bash
cd anti-slop-brain
python3 -m compileall -q scripts tests
python3 tests/test_scanners.py     # 107 checks
python3 tests/test_adapters.py     # 207 checks
python3 tests/test_pipeline.py
python3 scripts/check_links.py --vault wiki
```

**Run the suites directly, not under pytest.** They are standalone scripts with
their own runner, and their test functions take a positional `tmp` path that
pytest would try to satisfy as a fixture that does not exist.
`anti-slop-brain/conftest.py` therefore tells pytest not to collect
`anti-slop-brain/tests/`, so `python3 -m pytest` reports `no tests ran` (exit
code 5) instead of a wall of collection errors. A second `conftest.py` at the
repository root prints the commands above in the pytest header, since that hook
only fires for a conftest at the rootdir and `-q` suppresses it. CI runs those
commands directly, and they are the only supported way to run the suites.

Every fix needs a test that **fails before the fix and passes after**. Verify
the first half by reverting your change and watching the test fail. A test that
only passes proves nothing about the bug.

## Licensing your contribution

The repository is split-licensed, and it matters which part you touch.

| You edited | Your contribution is under |
|---|---|
| `scripts/`, `tests/`, `schemas/` | Apache 2.0 |
| `anti-slop-plugin/references/`, `wiki/markers/` | **CC BY-SA 4.0**, copyleft, inherited from Wikipedia |
| Any other prose | CC BY 4.0 |

The marker taxonomies adapt Wikipedia's Signs of AI writing guide. That content
cannot be relicensed. If you add to it, your addition stays CC BY-SA 4.0.

## Reporting something rather than fixing it

Open an issue. Findings about this project's own accuracy are especially
welcome, and there is precedent: the most useful review this project has had
was an adversarial pass instructed to break it, and it found a false claim in
the file that exists to be honest about limits.
