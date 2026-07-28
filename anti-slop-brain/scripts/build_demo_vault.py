#!/usr/bin/env python3
"""Rebuild the committed demo vault under `examples/sample-vault`.

The demo vault is a generated artifact that is committed to the repository,
and CI proves it is current by rebuilding it and diffing. That check is only
meaningful if the build is reproducible. Before `DEFAULT_REFERENCE_DATE`
existed the build stamped `date.today()` into roughly 120 files, so the diff
went red on the first pull request opened after the vault was committed and
stayed red, for no reason anyone could act on.

Every date the build stamps is therefore pinned. Resolution order is
`--reference-date`, then `SOURCE_DATE_EPOCH`, then the constant below.

Changing `DEFAULT_REFERENCE_DATE` is a deliberate act: rerun this script with
no arguments and commit the regenerated `examples/sample-vault` and
`references/canon` alongside it, or the drift check will fail.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reference_date import (  # noqa: E402
    ReferenceDateError,
    add_reference_date_argument,
    resolve_reference_date,
)


REPO = Path(__file__).resolve().parent.parent
PY = sys.executable

# The calendar date the committed demo vault was generated against.
DEFAULT_REFERENCE_DATE = date(2026, 7, 28)


def run(args: list[str]) -> None:
    subprocess.run([PY, *args], cwd=REPO, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    add_reference_date_argument(parser)
    args = parser.parse_args(argv)
    try:
        stamp = resolve_reference_date(
            args.reference_date, fallback=DEFAULT_REFERENCE_DATE
        ).isoformat()
    except ReferenceDateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    pin = ["--reference-date", stamp]

    demo_parent = REPO / "examples"
    demo = demo_parent / "sample-vault"
    if demo.exists():
        shutil.rmtree(demo)
    run(["scripts/scaffold_vault.py", "--client", "sample-vault", "--client-name", "Sample Client", "--owner", "Daniel Agrici", "--out-dir", str(demo_parent), *pin])
    run(["scripts/ingest_source.py", "--vault", str(demo), "--file", "tests/fixtures/sample-source.md", "--source-type", "fixture", *pin])
    run(["scripts/synthesize_brain.py", "--vault", str(demo), *pin])
    run(["scripts/generate_vault_visuals.py", "--vault", str(demo)])
    run(["scripts/render_brain_report.py", "--vault", str(demo), "--html-only"])
    run(["scripts/lint_vault.py", "--vault", str(demo)])
    print(demo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
