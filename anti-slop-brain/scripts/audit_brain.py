#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO = Path(__file__).resolve().parent.parent
RESEARCH_FILES = [
    "references/current-requirements.md",
    "references/market-research.md",
    "references/source-map.md",
    "references/safety-gates.md",
]
SOURCE_PACK_FILES = [
    "references/product-spec.md",
    "references/source-map.md",
    "references/current-requirements.md",
    "references/market-research.md",
    "references/safety-gates.md",
    "references/source-manifest-template.md",
    "references/research-plan.md",
    "references/adapter-plan.md",
    "references/source-ledger.json",
    "references/adapter-manifest.json",
]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"research required", re.I),
    re.compile(r"release blocked", re.I),
    re.compile(r"add .* before release", re.I),
    re.compile(r"replace this example", re.I),
]
HIGH_STAKES_TERMS = {
    "accounting",
    "tax",
    "legal",
    "medical",
    "health",
    "finance",
    "financial",
    "compliance",
    "payroll",
    "security",
    "insurance",
    "investment",
}
FAST_MOVING_TERMS = {
    "ads",
    "advertising",
    "api",
    "platform",
    "social",
    "youtube",
    "tiktok",
    "meta",
    "google",
    "linkedin",
    "ai",
}
PRIMARY_SOURCE_TYPES = {
    "official",
    "primary",
    "vendor",
    "regulator",
    "government",
    "standards",
    "standards-body",
    "authority",
    "api-docs",
}
DISALLOWED_SOURCE_HOSTS = {
    "example.com",
    "www.example.com",
    "example.org",
    "www.example.org",
    "example.net",
    "www.example.net",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}
MATURITY_SCORE_CAP = {
    "scaffolded": 59,
    "researched": 74,
    "domain-adapted": 84,
    "demo-verified": 89,
    "market-ready": 100,
}
MATURITY_ORDER = ["scaffolded", "researched", "domain-adapted", "demo-verified", "market-ready"]

# A refresh_due date is a plan, not a cliff. Inside this many days either side
# of the date a source is a prominent warning; only past the far edge does it
# become a critical failure. Without the band an entire cohort of sources
# sharing one date drops the brain from market-ready to scaffolded overnight,
# with no code change and no notice.
REFRESH_WARNING_DAYS = 14


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Anti-Slop Brain maturity gates.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require", choices=MATURITY_ORDER)
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument(
        "--reference-date",
        default=None,
        metavar="YYYY-MM-DD",
        help="Calendar date the freshness checks are anchored to. Defaults to today.",
    )
    args = parser.parse_args(argv)

    today = date.today()
    if args.reference_date:
        parsed = parse_iso_date(clean_string(args.reference_date))
        if parsed is None:
            print(
                f"ERROR: --reference-date must be an ISO date in YYYY-MM-DD form: {args.reference_date}",
                file=__import__("sys").stderr,
            )
            return 2
        today = parsed

    result = audit_repo(today)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Status: {result['status']}")
        print(f"Score: {result['score']}")
        print(refresh_window_line(result["refresh_window"]))
        for failure in result["critical_failures"]:
            print(f"CRITICAL: {failure}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")

    if args.require and MATURITY_ORDER.index(result["status"]) < MATURITY_ORDER.index(args.require):
        print(f"ERROR: required maturity {args.require}, got {result['status']}", file=__import__("sys").stderr)
        return 1
    if args.report_only:
        return 0
    return 1 if result["critical_failures"] else 0


def audit_repo(today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    categories: dict[str, dict[str, Any]] = {}
    critical: list[str] = []
    warnings: list[str] = []

    add_category(categories, "product_clarity", *check_product_clarity())
    add_category(categories, "source_pack", *check_source_pack())
    research_ok, research_score, research_notes, research_critical = check_research(today)
    add_category(categories, "current_research", research_ok, research_score, research_notes)
    critical.extend(research_critical)
    adapter_ok, adapter_score, adapter_notes, adapter_critical = check_adapters()
    add_category(categories, "domain_adapters", adapter_ok, adapter_score, adapter_notes)
    critical.extend(adapter_critical)
    citation_ok, citation_score, citation_notes, citation_critical = check_citations()
    add_category(categories, "source_citation", citation_ok, citation_score, citation_notes)
    critical.extend(citation_critical)
    add_category(categories, "demo_determinism", *check_paths(["examples/sample-vault/CODEX.md", "examples/sample-vault/.raw/.manifest.json", "examples/sample-vault/wiki/hot.md", "examples/sample-vault/wiki/reports/Weekly Report.md"]))
    add_category(categories, "tests", *check_paths(["tests/test_pipeline.py", ".github/workflows/ci.yml"]))
    add_category(categories, "packaging", *check_packaging())
    add_category(categories, "installability", *check_paths(["install.sh", "uninstall.sh", "pyproject.toml"]))
    add_category(categories, "docs", *check_paths(["README.md", "docs/OPERATOR_KIT.md", "docs/PRODUCT_BOUNDARIES.md", "RELEASE_CHECKLIST.md"]))
    add_category(categories, "obsidian_vault_quality", *check_paths(["assets/template-brain/CODEX.md", "assets/template-brain/.raw/.manifest.json", "assets/template-brain/wiki/hot.md", "assets/template-brain/wiki/index.md", "assets/template-brain/wiki/overview.md", "assets/template-brain/wiki/log.md", "assets/template-brain/wiki/meta/dashboard.md", "assets/template-brain/wiki/canvases/Onboarding Canvas.canvas"]))

    for name, category in categories.items():
        if not category["ok"]:
            warnings.append(f"{name}: " + "; ".join(category["notes"][:3]))

    refresh_window = summarize_refresh_window(today)
    if refresh_window["in_warning_band"]:
        warnings.insert(0, refresh_window_line(refresh_window))

    raw_score = round(sum(category["score"] for category in categories.values()) / len(categories))
    status = determine_status(categories, raw_score, critical)
    score = min(raw_score, MATURITY_SCORE_CAP[status])
    return {
        "status": status,
        "score": score,
        "market_ready": status == "market-ready",
        "critical_failures": critical,
        "warnings": warnings,
        "refresh_window": refresh_window,
        "categories": categories,
    }


def summarize_refresh_window(today: date) -> dict[str, Any]:
    """Count where every ledger source sits relative to its refresh_due date.

    Printed on every run, whether or not anything is wrong, so that a cohort of
    sources sharing one refresh date is visible weeks before it expires rather
    than on the morning it detonates.
    """
    summary: dict[str, Any] = {
        "reference_date": today.isoformat(),
        "warning_band_days": REFRESH_WARNING_DAYS,
        "sources_with_refresh_due": 0,
        "due_soon": 0,
        "recently_overdue": 0,
        "in_warning_band": 0,
        "critically_overdue": 0,
        "earliest_refresh_due": None,
        "earliest_days_remaining": None,
        "earliest_refresh_due_count": 0,
    }
    data, errors = load_json_object(REPO / "references" / "source-ledger.json")
    if errors:
        return summary
    sources = data.get("sources")
    if not isinstance(sources, list):
        return summary

    earliest: date | None = None
    for source in sources:
        if not isinstance(source, dict):
            continue
        refresh_due = parse_iso_date(clean_string(source.get("refresh_due")))
        if refresh_due is None:
            continue
        summary["sources_with_refresh_due"] += 1
        remaining = (refresh_due - today).days
        if remaining < -REFRESH_WARNING_DAYS:
            summary["critically_overdue"] += 1
        elif remaining < 0:
            summary["recently_overdue"] += 1
        elif remaining <= REFRESH_WARNING_DAYS:
            summary["due_soon"] += 1
        if earliest is None or refresh_due < earliest:
            earliest = refresh_due

    summary["in_warning_band"] = summary["due_soon"] + summary["recently_overdue"]
    if earliest is not None:
        summary["earliest_refresh_due"] = earliest.isoformat()
        summary["earliest_days_remaining"] = (earliest - today).days
        summary["earliest_refresh_due_count"] = sum(
            1
            for source in sources
            if isinstance(source, dict)
            and parse_iso_date(clean_string(source.get("refresh_due"))) == earliest
        )
    return summary


def refresh_window_line(summary: dict[str, Any]) -> str:
    """One line naming the next refresh cliff, printed on every audit run."""
    if not summary.get("sources_with_refresh_due"):
        return "Refresh window: no ledger source carries a refresh_due date."
    earliest = summary["earliest_refresh_due"]
    remaining = summary["earliest_days_remaining"]
    when = f"in {remaining} day(s)" if remaining >= 0 else f"{-remaining} day(s) ago"
    return (
        f"Refresh window: earliest refresh_due {earliest} ({when}) shared by "
        f"{summary['earliest_refresh_due_count']} source(s); "
        f"{summary['due_soon']} due within {summary['warning_band_days']} day(s), "
        f"{summary['recently_overdue']} overdue but inside the warning band, "
        f"{summary['critically_overdue']} overdue by more than "
        f"{summary['warning_band_days']} day(s)."
    )


def add_category(categories: dict[str, dict[str, Any]], name: str, ok: bool, score: int, notes: list[str]) -> None:
    categories[name] = {"ok": ok, "score": max(0, min(100, score)), "notes": notes}


def check_product_clarity() -> tuple[bool, int, list[str]]:
    text = (read(REPO / "README.md") + "\n" + read(REPO / "SKILL.md")).lower()
    required = ["buyer", "outputs", "boundaries", "quick start", "maturity"]
    notes = [f"missing {term} language" for term in required if term not in text]
    return not notes, 100 - 15 * len(notes), notes


def check_source_pack() -> tuple[bool, int, list[str]]:
    missing = [rel for rel in SOURCE_PACK_FILES if not (REPO / rel).exists()]
    return not missing, 100 - 12 * len(missing), [f"missing {rel}" for rel in missing]


def check_research(today: date | None = None) -> tuple[bool, int, list[str], list[str]]:
    today = today or date.today()
    notes: list[str] = []
    critical: list[str] = []
    score = 100
    context = read(REPO / "references" / "product-spec.md") + "\n" + read(REPO / "README.md")
    requires_fresh = contains_any(context, HIGH_STAKES_TERMS) or contains_any(context, FAST_MOVING_TERMS)

    for rel in RESEARCH_FILES:
        path = REPO / rel
        if not path.exists():
            notes.append(f"missing {rel}")
            critical.append(f"missing research file: {rel}")
            score -= 25
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS):
            notes.append(f"placeholder research remains in {rel}")
            critical.append(f"placeholder research remains: {rel}")
            score -= 20
        if rel.endswith("current-requirements.md") and not re.search(r"\b20\d\d-\d\d-\d\d\b", text):
            notes.append(f"missing retrieval dates in {rel}")
            score -= 10

    ledger_ok, ledger_score, ledger_notes, ledger_critical = check_source_ledger(
        requires_fresh=requires_fresh, today=today
    )
    notes.extend(ledger_notes)
    critical.extend(ledger_critical)
    return not critical and ledger_ok, max(0, min(score, ledger_score)), notes, critical


def check_source_ledger(
    *, requires_fresh: bool, today: date | None = None
) -> tuple[bool, int, list[str], list[str]]:
    today = today or date.today()
    path = REPO / "references" / "source-ledger.json"
    notes: list[str] = []
    # Warning band entries are reported but never scored. A source approaching
    # its refresh date is information, not a defect, so it must not quietly
    # erode the score on the way to becoming a real failure.
    band_notes: list[str] = []
    critical: list[str] = []
    data, errors = load_json_object(path)
    if errors:
        critical.extend(f"invalid source-ledger.json: {error}" for error in errors)
        return False, 0, notes, critical
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        notes.append("source-ledger.json has no captured sources")
        critical.append("source-ledger has no captured official/primary sources")
        return False, 35, notes, critical

    official_count = 0
    for index, source in enumerate(sources, start=1):
        label = f"source-ledger source #{index}"
        if not isinstance(source, dict):
            critical.append(f"{label} must be an object")
            continue
        source_type = clean_string(source.get("source_type")).lower()
        retrieved = parse_iso_date(clean_string(source.get("retrieved")))
        refresh_due = parse_iso_date(clean_string(source.get("refresh_due")))
        claims = source.get("claims")
        if not clean_string(source.get("title")):
            critical.append(f"{label} missing title")
        if not is_valid_source_url(clean_string(source.get("url"))):
            critical.append(f"{label} has invalid or placeholder URL")
        if source_type in PRIMARY_SOURCE_TYPES:
            official_count += 1
        elif source_type not in {"market", "practitioner", "supporting", "fixture"}:
            critical.append(f"{label} has unsupported source_type")
        if retrieved is None:
            critical.append(f"{label} missing valid retrieved date")
        elif retrieved > today:
            critical.append(f"{label} has future retrieved date")
        if not isinstance(claims, list) or not any(clean_string(claim) for claim in claims):
            critical.append(f"{label} must list sourced claims")
        if requires_fresh:
            if refresh_due is None:
                critical.append(f"{label} missing valid refresh_due date")
            else:
                remaining = (refresh_due - today).days
                if remaining < -REFRESH_WARNING_DAYS:
                    critical.append(
                        f"{label} refresh_due is stale by {-remaining} days, past the "
                        f"{REFRESH_WARNING_DAYS} day warning band"
                    )
                elif remaining <= REFRESH_WARNING_DAYS:
                    band_notes.append(
                        f"{label} refresh_due {clean_string(source.get('refresh_due'))} is "
                        f"inside the {REFRESH_WARNING_DAYS} day warning band"
                    )

    minimum_official = 2 if requires_fresh else 1
    if official_count < minimum_official:
        critical.append(f"source-ledger needs at least {minimum_official} official/primary sources")
    score = max(0, 100 - 18 * len(critical) - 8 * len(notes))
    if band_notes:
        notes.append(
            f"{len(band_notes)} source(s) inside the {REFRESH_WARNING_DAYS} day "
            "refresh_due warning band; see refresh_window"
        )
    return not critical, score, notes, critical


def check_adapters() -> tuple[bool, int, list[str], list[str]]:
    notes: list[str] = []
    critical: list[str] = []
    data, errors = load_json_object(REPO / "references" / "adapter-manifest.json")
    if errors:
        critical.extend(f"invalid adapter-manifest.json: {error}" for error in errors)
        return False, 0, notes, critical
    if data.get("generic_only") is not False:
        notes.append("adapter-manifest declares generic_only=true")
        return False, 55, notes, critical

    required_sections = {
        "input_schemas": "input schema",
        "importers": "importer",
        "synthesis_modules": "synthesis module",
        "report_renderers": "report renderer",
        "fixtures": "fixture",
        "tests": "test",
    }
    for section, label in required_sections.items():
        entries = data.get(section)
        if not isinstance(entries, list) or not entries:
            critical.append(f"adapter-manifest missing {label} entries")
            continue
        for index, entry in enumerate(entries, start=1):
            entry_path = manifest_entry_path(entry)
            if not entry_path:
                critical.append(f"adapter-manifest {section} #{index} missing path")
            elif not (REPO / entry_path).exists():
                critical.append(f"adapter-manifest {section} path does not exist: {entry_path}")
    return not critical, max(0, 100 - 18 * len(critical) - 8 * len(notes)), notes, critical


def check_citations() -> tuple[bool, int, list[str], list[str]]:
    notes: list[str] = []
    critical: list[str] = []
    for folder in ["assets/template-brain/wiki/deliverables", "assets/template-brain/wiki/reports", "examples/sample-vault/wiki/deliverables", "examples/sample-vault/wiki/reports"]:
        root = REPO / folder
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            if "[[" not in text and ".raw/" not in text and "sha256" not in text.lower():
                rel = path.relative_to(REPO).as_posix()
                notes.append(f"missing source citation in {rel}")
                critical.append(f"unsourced deliverable/report: {rel}")
    return not critical, max(0, 100 - 15 * len(critical)), notes, critical


def check_packaging() -> tuple[bool, int, list[str]]:
    path = REPO / "scripts" / "package_release.py"
    if not path.exists():
        return False, 0, ["missing scripts/package_release.py"]
    text = path.read_text(encoding="utf-8", errors="replace")
    notes = [f"package script missing {term}" for term in ["SHA256SUMS", "RELEASE_MANIFEST", "release-type", "market-ready", "audit_brain.py"] if term not in text]
    return not notes, 100 - 20 * len(notes), notes


def check_paths(paths: list[str]) -> tuple[bool, int, list[str]]:
    missing = [rel for rel in paths if not (REPO / rel).exists()]
    return not missing, 100 - 12 * len(missing), [f"missing {rel}" for rel in missing]


def determine_status(categories: dict[str, dict[str, Any]], score: int, critical: list[str]) -> str:
    if not categories["current_research"]["ok"]:
        return "scaffolded"
    if not categories["domain_adapters"]["ok"]:
        return "researched"
    if not categories["demo_determinism"]["ok"] or not categories["tests"]["ok"]:
        return "domain-adapted"
    if critical or score < 90 or any(not categories[name]["ok"] for name in ["packaging", "installability", "docs", "source_citation", "obsidian_vault_quality"]):
        return "demo-verified"
    return "market-ready"


def load_json_object(path: Path) -> tuple[dict[str, Any], list[str]]:
    if not path.exists():
        return {}, [f"missing {path.relative_to(REPO).as_posix()}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return {}, [str(exc)]
    if not isinstance(data, dict):
        return {}, ["top-level value must be an object"]
    return data, []


def contains_any(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def clean_string(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def parse_iso_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def is_valid_source_url(value: str) -> bool:
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    return parsed.scheme in {"http", "https"} and bool(host) and host not in DISALLOWED_SOURCE_HOSTS and "TBD" not in value.upper()


def manifest_entry_path(entry: object) -> str:
    if isinstance(entry, str):
        return entry
    if not isinstance(entry, dict):
        return ""
    for key in ["path", "schema_path", "module", "fixture", "test"]:
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
