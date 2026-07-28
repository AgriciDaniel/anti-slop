#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
PY = sys.executable

# Both generated trees the demo build writes. `examples/sample-vault` is the
# one CI diffs; `references/canon` is folded from the source ledger by the same
# run and used to drift silently, so a contributor who ran the documented
# command got a dirty tree they did not ask for.
GENERATED_TREES = (REPO / "examples" / "sample-vault", REPO / "references" / "canon")


def run(args: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run([PY, *args], cwd=REPO, text=True, capture_output=True, env={**os.environ, **(env or {})}, check=False)
    if proc.returncode:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise AssertionError(f"command failed: {' '.join(args)}")
    return proc


def run_cmd(args: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(args, cwd=REPO, text=True, capture_output=True, env={**os.environ, **(env or {})}, check=False)
    if proc.returncode:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise AssertionError(f"command failed: {' '.join(args)}")
    return proc


def tree_digest(*roots: Path) -> str:
    """Hash the relative path and bytes of every file under the given roots."""
    digest = hashlib.sha256()
    for root in roots:
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            digest.update(path.relative_to(REPO).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def test_demo_build_is_reproducible() -> None:
    """The demo build must depend on its inputs, not on the calendar.

    Regression: `build_demo_vault.py` stamped `date.today()` through
    `scaffold_vault.py`, `synthesize_brain.py` and `ingest_source.py`. The
    committed vault therefore matched a fresh build only on the day it was
    committed. Moving the clock forward one day produced 119 changed files,
    244 insertions and 244 deletions, so the CI drift check went red on the
    first pull request opened after release and stayed red.

    Two assertions are needed, not one. Byte-identical output at a pinned date
    proves reproducibility; different output at a different pinned date proves
    the pin is real, rather than the dates having been deleted outright.
    """
    try:
        run(["scripts/build_demo_vault.py", "--reference-date", "2019-03-04"])
        first = tree_digest(*GENERATED_TREES)
        run(["scripts/build_demo_vault.py", "--reference-date", "2019-03-04"])
        second = tree_digest(*GENERATED_TREES)
        assert first == second, "two builds at the same pinned date differ"

        # SOURCE_DATE_EPOCH is the reproducible-builds spelling of the same pin
        # and must land on the same UTC calendar date.
        run(["scripts/build_demo_vault.py"], env={"SOURCE_DATE_EPOCH": "1551657600"})
        assert tree_digest(*GENERATED_TREES) == first, "SOURCE_DATE_EPOCH did not match the equivalent --reference-date"

        run(["scripts/build_demo_vault.py", "--reference-date", "2021-11-09"])
        assert tree_digest(*GENERATED_TREES) != first, "a different pinned date produced identical output, so nothing is actually stamped"
    finally:
        # Restore the committed state, which is what the default pin builds.
        run(["scripts/build_demo_vault.py"])

    committed = subprocess.run(
        ["git", "diff", "--exit-code", "--", "examples/sample-vault", "references/canon"],
        cwd=REPO, text=True, capture_output=True, check=False,
    )
    if committed.returncode == 128:
        print("skip: git diff unavailable, generated trees not compared to the index")
    else:
        assert committed.returncode == 0, (
            "the default pinned date does not rebuild the committed trees:\n"
            + committed.stdout[:2000]
        )


def main() -> int:
    run(["-m", "compileall", "scripts", "anti_slop_brain", "tests"])
    run(["scripts/lint_vault.py", "--vault", "assets/template-brain", "--template"])
    with tempfile.TemporaryDirectory(prefix="anti-slop-brain-test-") as tmp:
        out_dir = Path(tmp) / "vaults"
        run(["scripts/scaffold_vault.py", "--client", "acme", "--client-name", "Acme Co", "--owner", "Test Owner", "--out-dir", str(out_dir)])
        vault = out_dir / "acme"
        run(["scripts/ingest_source.py", "--vault", str(vault), "--file", "tests/fixtures/sample-source.md"])
        # Point the canon fold at the throwaway vault. A test that synthesizes a
        # scratch vault must not restamp this repository's reference layer.
        run(["scripts/synthesize_brain.py", "--vault", str(vault), "--canon-dir", str(vault / "references" / "canon")])
        run(["scripts/generate_vault_visuals.py", "--vault", str(vault)])
        run(["scripts/render_brain_report.py", "--vault", str(vault), "--html-only"])
        run(["scripts/lint_vault.py", "--vault", str(vault)])
        assert (vault / "weekly-report.html").exists()
    test_demo_build_is_reproducible()
    audit = run(["scripts/audit_brain.py", "--json", "--report-only"])
    audit_result = json.loads(audit.stdout)
    market_ready = audit_result.get("market_ready") is True or audit_result.get("status") == "market-ready"
    gated = subprocess.run([PY, "scripts/package_release.py", "--version", "0.1.0", "--release-type", "market-ready"], cwd=REPO, text=True, capture_output=True, check=False)
    if market_ready:
        if gated.returncode:
            print(gated.stdout)
            print(gated.stderr, file=sys.stderr)
        assert gated.returncode == 0
        manifest = REPO / "dist" / "RELEASE_MANIFEST.json"
        assert manifest.exists()
        assert json.loads(manifest.read_text(encoding="utf-8")).get("release_type") == "market-ready"
    else:
        assert gated.returncode != 0
        assert "market-ready release blocked" in gated.stderr
    run(["scripts/package_release.py", "--version", "0.1.0"])
    assert (REPO / "dist" / "RELEASE_MANIFEST.json").exists()
    with tempfile.TemporaryDirectory(prefix="anti-slop-brain-install-") as tmp:
        env = {"ANTI_SLOP_BRAIN_INSTALL_HOME": tmp}
        run_cmd(["bash", "install.sh", "--target", "all"], env=env)
        assert (Path(tmp) / ".codex" / "skills" / "anti-slop-brain" / "SKILL.md").exists()
        assert (Path(tmp) / ".openclaw" / "skills" / "anti-slop-brain" / "SKILL.md").exists()
        assert (Path(tmp) / ".agent-skills" / "anti-slop-brain" / "SKILL.md").exists()
        assert (Path(tmp) / ".gemini" / "anti-slop-brain" / "GEMINI.md").exists()
        assert "anti-slop-brain-install:start" in (Path(tmp) / ".gemini" / "GEMINI.md").read_text(encoding="utf-8")
        custom_root = Path(tmp) / "custom-skills"
        run_cmd(["bash", "install.sh", "--target", "custom", "--path", str(custom_root)], env=env)
        assert (custom_root / "anti-slop-brain" / "SKILL.md").exists()
        run_cmd(["bash", "uninstall.sh", "--target", "all"], env=env)
        assert not (Path(tmp) / ".codex" / "skills" / "anti-slop-brain").exists()
        assert not (Path(tmp) / ".gemini" / "anti-slop-brain").exists()
        assert not (Path(tmp) / ".gemini" / "GEMINI.md").exists()
        run_cmd(["bash", "uninstall.sh", "--target", "custom", "--path", str(custom_root)], env=env)
        assert not (custom_root / "anti-slop-brain").exists()
    print("Pipeline tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
