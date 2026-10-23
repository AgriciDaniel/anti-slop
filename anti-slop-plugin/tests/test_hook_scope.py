#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "anti-slop-plugin"
HOOKS = PLUGIN / "hooks" / "hooks.json"


def check(name: str, passed: bool, detail: str = "") -> bool:
    print(f"{'pass' if passed else 'FAIL'}: {name}")
    if not passed and detail:
        print(f"  {detail}")
    return passed


def run_hook(command: str, project: Path, plugin: Path, path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CLAUDE_PLUGIN_ROOT"] = str(plugin)
    env["CLAUDE_PROJECT_DIR"] = str(project)
    payload = json.dumps({"tool_input": {"file_path": str(path)}, "cwd": str(project)})
    argv = shlex.split(command)
    argv[0] = sys.executable
    return subprocess.run(
        argv,
        cwd=project,
        env=env,
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    manifest = json.loads(HOOKS.read_text(encoding="utf-8"))
    failures = 0
    if not check(
        "hooks.json uses only supported top-level keys",
        set(manifest) == {"description", "hooks"},
        f"found keys: {sorted(manifest)}",
    ):
        failures += 1
    command = manifest["hooks"]["PostToolUse"][0]["hooks"][0]["command"]

    with tempfile.TemporaryDirectory(prefix="anti-slop-hook-test-") as tmp:
        root = Path(tmp)
        project = root / "project"
        project.mkdir()
        dash = chr(0x2013)

        dirty = project / "dirty.md"
        dirty.write_text(f"This sentence contains {dash} a style violation.\n", encoding="utf-8")
        result = run_hook(command, project, PLUGIN, dirty)
        if not check(
            "in-project prose is linted and findings are returned",
            result.returncode == 2 and bool(result.stderr),
            f"exit={result.returncode}, stderr={result.stderr[:300]!r}",
        ):
            failures += 1

        clean = project / "clean.md"
        clean.write_text("This sentence follows the house style.\n", encoding="utf-8")
        result = run_hook(command, project, PLUGIN, clean)
        if not check(
            "clean in-project prose passes",
            result.returncode == 0 and not result.stderr,
            f"exit={result.returncode}, stderr={result.stderr[:300]!r}",
        ):
            failures += 1

        for name, relative in (("configuration", "settings.yml"), ("code", "example.py")):
            path = project / relative
            path.write_text(f"value = 'text {dash} text'\n", encoding="utf-8")
            result = run_hook(command, project, PLUGIN, path)
            if not check(
                f"in-project {name} files are skipped",
                result.returncode == 0 and not result.stderr,
                f"exit={result.returncode}, stderr={result.stderr[:300]!r}",
            ):
                failures += 1

        outside = root / "outside.md"
        outside.write_text(f"This sentence contains {dash} a style violation.\n", encoding="utf-8")
        result = run_hook(command, project, PLUGIN, outside)
        if not check(
            "prose outside the project is skipped",
            result.returncode == 0 and not result.stderr,
            f"exit={result.returncode}, stderr={result.stderr[:300]!r}",
        ):
            failures += 1

        linked = project / "linked-outside.md"
        try:
            linked.symlink_to(outside)
        except OSError as exc:
            print(f"skip: symlink escape check unavailable ({exc})")
        else:
            result = run_hook(command, project, PLUGIN, linked)
            if not check(
                "symlink paths resolving outside the project are skipped",
                result.returncode == 0 and not result.stderr,
                f"exit={result.returncode}, stderr={result.stderr[:300]!r}",
            ):
                failures += 1

    if failures:
        print("Hook scope tests failed")
        return 1
    print("Hook scope tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
