#!/usr/bin/env python3
"""Layer 0 scanner: slopsquatting gate over imported and declared packages.

A generated snippet can import a package that does not exist. An attacker
who registers that name owns every machine that pastes the snippet. The
gate is mechanical: enumerate every third-party package name the code
depends on, then decide whether it exists.

Why the gate still matters, and why the usual number is stale:

- Spracklen et al., USENIX Security 2025, established package hallucination
  as a measured supply-chain risk, at roughly 19.7% of generated package
  references across the 2024 model cohort. That is the number the ecosystem
  still quotes.
- Churilov, arXiv 2605.17062 (2026-05-16), and Socket's replication
  (2026-07-22) measure 2026 frontier models at 4.62% to 6.10%.

So the honest reading is: the rate has fallen by roughly an order of
magnitude from the widely-quoted 20%, and the gate is still worth running,
because a 5% chance of a hostile install is not an acceptable risk and the
check costs nothing. Do not cite the 19.7% figure as current.

Sources of package names:

- Python: `ast.parse`, walking Import and ImportFrom nodes. Regex would
  match imports inside strings, comments and docstrings; ast does not.
  Relative imports (level > 0) are package-local and are skipped.
- `package.json`: dependencies, devDependencies, peerDependencies and
  optionalDependencies keys.
- `requirements.txt` and friends: requirement lines, with extras, markers
  and version specifiers stripped.

Offline is the default and makes no network requests. Offline, a name is
resolved against the Python standard library set, module names local to the
scanned tree, and an allowlist. Anything left over is reported as
`unverified`, which means "this scanner could not confirm it exists", not
"this is fake". `--online` queries the PyPI JSON API and the npm registry
for existence and reports a 404 as `missing`.

This scanner reports mechanical facts about package names. It never emits
an authorship verdict.

Usage:
    python3 scripts/scan_packages.py src/ package.json requirements.txt
    python3 scripts/scan_packages.py src/ --online --format json

Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import (  # noqa: E402
    SKIP_DIR_NAMES,
    Finding,
    UsageError,
    emit,
    run_cli,
)

TOOL = "scan_packages"

# A deliberately small, hand-checked allowlist. It is not a mirror of the
# registries. Its only job is to keep the common case quiet so that a real
# unknown stands out.
KNOWN_PYPI = frozenset({
    "aiohttp", "anthropic", "attrs", "beautifulsoup4", "boto3", "botocore",
    "certifi", "cffi", "charset_normalizer", "click", "cryptography", "dateutil",
    "django", "docutils", "fastapi", "flask", "fsspec", "google", "httpx",
    "huggingface_hub", "idna", "jinja2", "jsonschema", "lxml", "markdown",
    "markupsafe", "matplotlib", "mypy", "networkx", "numpy", "openai", "orjson",
    "packaging", "pandas", "pillow", "PIL", "pip", "platformdirs", "pluggy",
    "polars", "psycopg2", "pydantic", "pygments", "pytest", "pytz", "PyYAML",
    "yaml", "regex", "requests", "rich", "ruff", "scipy", "setuptools",
    "sklearn", "scikit_learn", "seaborn", "six", "sqlalchemy", "starlette",
    "sympy", "tenacity", "tiktoken", "torch", "tornado", "tqdm", "typer",
    "typing_extensions", "urllib3", "uvicorn", "werkzeug", "wheel", "yarl",
})
KNOWN_NPM = frozenset({
    "axios", "chalk", "commander", "cross-env", "dotenv", "esbuild", "eslint",
    "express", "fastify", "jest", "lodash", "next", "node-fetch", "nodemon",
    "prettier", "react", "react-dom", "rollup", "svelte", "tailwindcss",
    "typescript", "vite", "vitest", "vue", "webpack", "zod",
})

REQUIREMENT_FILE_RE = re.compile(r"^requirements.*\.txt$|^constraints.*\.txt$", re.IGNORECASE)
REQUIREMENT_NAME_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)")
LOCAL_SPEC_PREFIXES = ("file:", "link:", "workspace:", "portal:", "git+", "http:", "https:")


class Package:
    """One package name found in one place."""

    def __init__(self, ecosystem: str, name: str, path: str, line: int, origin: str) -> None:
        self.ecosystem = ecosystem
        self.name = name
        self.path = path
        self.line = line
        self.origin = origin
        self.status = "unverified"
        self.detail = ""

    def key(self) -> tuple[str, str]:
        return (self.ecosystem, self.name)

    def as_dict(self) -> dict:
        return {
            "ecosystem": self.ecosystem,
            "name": self.name,
            "path": self.path,
            "line": self.line,
            "origin": self.origin,
            "status": self.status,
            "detail": self.detail,
        }


def collect_targets(raw_paths: list[str]) -> list[Path]:
    """Expand the requested paths into files this scanner understands."""
    targets: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                if any(part in SKIP_DIR_NAMES for part in child.parts):
                    continue
                if child.suffix == ".py" or child.name == "package.json" \
                        or REQUIREMENT_FILE_RE.match(child.name):
                    targets.append(child)
            continue
        if not path.exists():
            raise UsageError(f"no such path: {raw}")
        targets.append(path)
    return targets


def local_module_names(targets: list[Path]) -> set[str]:
    """Names that resolve inside the scanned tree, so they are not third party."""
    names: set[str] = set()
    directories = {path.parent for path in targets if path.suffix == ".py"}
    extended = set(directories)
    for directory in directories:
        current = directory
        # Walk out of nested packages so the package root name is importable too.
        while (current / "__init__.py").exists() and current.parent != current:
            current = current.parent
            extended.add(current)
    for parent in extended:
        try:
            children = list(parent.iterdir())
        except OSError:
            continue
        for child in children:
            if child.is_file() and child.suffix == ".py":
                names.add(child.stem)
            elif child.is_dir() and (child / "__init__.py").exists():
                names.add(child.name)
    for path in targets:
        if path.suffix == ".py":
            names.add(path.stem)
    return names


def parse_python(path: Path, source: str) -> tuple[list[Package], list[Finding]]:
    packages: list[Package] = []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return packages, [
            Finding(
                path=str(path),
                line=exc.lineno or 1,
                column=(exc.offset or 0) + 1,
                rule="packages.parse_error",
                message=f"cannot parse Python source, imports were not checked: {exc.msg}",
                snippet=(exc.text or "").strip()[:160],
                severity="review",
            )
        ]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                packages.append(
                    Package("pypi", alias.name.split(".")[0], str(path), node.lineno, "import")
                )
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # relative import, resolves inside the package
            if not node.module:
                continue
            packages.append(
                Package("pypi", node.module.split(".")[0], str(path), node.lineno, "import-from")
            )
    return packages, []


def parse_package_json(path: Path, source: str) -> tuple[list[Package], list[Finding]]:
    packages: list[Package] = []
    try:
        data = json.loads(source)
    except ValueError as exc:
        return packages, [
            Finding(
                path=str(path), line=1, column=1, rule="packages.parse_error",
                message=f"cannot parse package.json: {exc}", snippet="", severity="review",
            )
        ]
    if not isinstance(data, dict):
        return packages, []
    lines = source.splitlines()
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        section = data.get(field)
        if not isinstance(section, dict):
            continue
        for name, spec in section.items():
            if isinstance(spec, str) and spec.startswith(LOCAL_SPEC_PREFIXES):
                continue
            line = 1
            for index, text in enumerate(lines, 1):
                if f'"{name}"' in text:
                    line = index
                    break
            packages.append(Package("npm", name, str(path), line, field))
    return packages, []


def parse_requirements(path: Path, source: str) -> tuple[list[Package], list[Finding]]:
    packages: list[Package] = []
    for line_no, raw in enumerate(source.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        if line.startswith(LOCAL_SPEC_PREFIXES):
            continue
        line = line.split(";", 1)[0].strip()
        match = REQUIREMENT_NAME_RE.match(line)
        if not match:
            continue
        packages.append(Package("pypi", match.group(1), str(path), line_no, "requirements"))
    return packages, []


def load_allowlist(path: Path | None) -> tuple[set[str], set[str]]:
    pypi = set(KNOWN_PYPI)
    npm = set(KNOWN_NPM)
    if path is None:
        return pypi, npm
    if not path.exists():
        raise UsageError(f"no such allowlist file: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("pypi:"):
            pypi.add(line[5:].strip())
        elif line.startswith("npm:"):
            npm.add(line[4:].strip())
        else:
            pypi.add(line)
            npm.add(line)
    return pypi, npm


def normalize_pypi(name: str) -> str:
    return re.sub(r"[-_.]+", "_", name).lower()


def classify_offline(
    packages: list[Package],
    pypi_allow: set[str],
    npm_allow: set[str],
    local_names: set[str],
) -> None:
    stdlib = set(sys.stdlib_module_names)
    pypi_norm = {normalize_pypi(name) for name in pypi_allow}
    for package in packages:
        if package.ecosystem == "pypi":
            if package.name in stdlib:
                package.status = "stdlib"
                continue
            if package.origin != "requirements" and package.name in local_names:
                package.status = "local"
                continue
            if normalize_pypi(package.name) in pypi_norm:
                package.status = "allowlisted"
                continue
            package.status = "unverified"
            package.detail = "not in the standard library, the local tree, or the allowlist"
        else:
            if package.name in npm_allow:
                package.status = "allowlisted"
                continue
            package.status = "unverified"
            package.detail = "not in the allowlist"


def registry_url(package: Package) -> str:
    if package.ecosystem == "pypi":
        return f"https://pypi.org/pypi/{package.name}/json"
    return "https://registry.npmjs.org/" + package.name.replace("/", "%2F")


def check_online(packages: list[Package], timeout: float) -> None:
    """Query PyPI and npm for existence. Network calls."""
    import urllib.error
    import urllib.request

    print(
        "NOTICE: --online queries pypi.org and registry.npmjs.org for every "
        "unverified package name. Offline mode is the default and never does this.",
        file=sys.stderr,
    )
    cache: dict[tuple[str, str], tuple[str, str]] = {}
    headers = {"User-Agent": "anti-slop-scan-packages/1.0 (+existence check)"}
    for package in packages:
        if package.status in {"stdlib", "local"}:
            continue
        key = package.key()
        if key not in cache:
            request = urllib.request.Request(registry_url(package), headers=headers, method="GET")
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    cache[key] = ("exists", f"HTTP {response.status}")
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    cache[key] = ("missing", "registry returned HTTP 404")
                else:
                    cache[key] = ("registry-error", f"HTTP {exc.code}")
            except Exception as exc:  # noqa: BLE001 - transport failure is not existence
                cache[key] = ("registry-error", f"{type(exc).__name__}: {exc}")
        package.status, package.detail = cache[key]


def build_findings(packages: list[Package]) -> list[Finding]:
    findings: list[Finding] = []
    for package in packages:
        if package.status == "missing":
            findings.append(
                Finding(
                    path=package.path, line=package.line, column=1,
                    rule="packages.missing",
                    message=f"{package.ecosystem} package '{package.name}' does not exist "
                            f"in the registry: {package.detail}",
                    snippet=package.origin, severity="defect",
                )
            )
        elif package.status == "unverified":
            findings.append(
                Finding(
                    path=package.path, line=package.line, column=1,
                    rule="packages.unverified",
                    message=f"{package.ecosystem} package '{package.name}' could not be "
                            f"confirmed offline: {package.detail}. Confirm it by hand or "
                            f"rerun with --online.",
                    snippet=package.origin, severity="unverified",
                )
            )
        elif package.status == "registry-error":
            findings.append(
                Finding(
                    path=package.path, line=package.line, column=1,
                    rule="packages.registry_error",
                    message=f"{package.ecosystem} package '{package.name}' lookup failed: "
                            f"{package.detail}",
                    snippet=package.origin, severity="unresolved",
                )
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scan_packages.py",
        description="Enumerate third-party package dependencies and check that they exist.",
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to scan.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--allowlist", default=None, help="Extra allowlist file.")
    parser.add_argument(
        "--online", action="store_true",
        help="Opt in to registry existence checks. Offline is the default.",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout.")
    parser.add_argument(
        "--stdin-kind", choices=("python", "requirements", "package-json"), default="python",
        help="How to parse stdin when no path is given.",
    )
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        raise UsageError("--timeout must be positive")

    packages: list[Package] = []
    findings: list[Finding] = []

    if not args.paths or args.paths == ["-"]:
        source = sys.stdin.read()
        label = Path("<stdin>")
        if args.stdin_kind == "python":
            found, errors = parse_python(label, source)
        elif args.stdin_kind == "package-json":
            found, errors = parse_package_json(label, source)
        else:
            found, errors = parse_requirements(label, source)
        packages.extend(found)
        findings.extend(errors)
        local_names: set[str] = set()
    else:
        targets = collect_targets(args.paths)
        local_names = local_module_names(targets)
        for path in targets:
            try:
                source = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                raise UsageError(f"cannot read {path}: {exc}") from exc
            if path.suffix == ".py":
                found, errors = parse_python(path, source)
            elif path.name == "package.json":
                found, errors = parse_package_json(path, source)
            elif REQUIREMENT_FILE_RE.match(path.name):
                found, errors = parse_requirements(path, source)
            else:
                continue
            packages.extend(found)
            findings.extend(errors)

    pypi_allow, npm_allow = load_allowlist(Path(args.allowlist) if args.allowlist else None)
    classify_offline(packages, pypi_allow, npm_allow, local_names)
    if args.online:
        check_online(packages, args.timeout)
    findings.extend(build_findings(packages))

    third_party = [
        package for package in packages if package.status not in {"stdlib", "local"}
    ]
    inventory = {
        "mode": "online" if args.online else "offline",
        "third_party_count": len({package.key() for package in third_party}),
        "packages": [package.as_dict() for package in packages],
    }
    if args.format == "text":
        seen: set[tuple[str, str]] = set()
        for package in sorted(third_party, key=lambda p: (p.ecosystem, p.name)):
            if package.key() in seen:
                continue
            seen.add(package.key())
            print(f"package: {package.ecosystem}\t{package.name}\t{package.status}")
    return emit(findings, args.format, TOOL, inventory=inventory)


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
