#!/usr/bin/env python3
"""Shared helpers for the Anti-Slop domain adapters.

Two adapter lanes live in this repository and both import from here.

Lane 1, the review run: `ingest_review_input.py`, `synthesize_findings.py`,
`render_findings_report.py`. It turns an artifact under review, plus the
output of the Layer 0 scanners, plus the artifacts produced by the Layer 1
structural procedures, into a findings report.

Lane 2, the marker cohort refresh: `ingest_marker_cohort.py`,
`synthesize_cohort_diff.py`, `render_cohort_report.py`. Marker lists rot, so
two dated snapshots are diffed and every source whose `refresh_due` has
passed is flagged.

Firewall rules carried by this module, from PLAN.md section 3:

1. No adapter output object carries an authorship verdict key of any kind.
   The scanners in `scan_common.py` emit an explicit `authorship_verdict:
   null`; the adapters go further and never name the concept as a field, so
   that no consumer can read a value out of one.
2. A Tier 2 or Tier 3 marker never produces a finding on its own. It
   produces a routed procedure suggestion. Only a structural procedure that
   convicted a span, or a deterministic Layer 0 scanner, produces a finding.
3. Severity is impact and confidence is certainty. They are computed by two
   separate functions and stored in two separate fields.
4. A finding with no evidence span is refused rather than emitted.

Determinism. Nothing here reads the clock, seeds a random source, or lets
set iteration order reach the output. Every collection is sorted before it
is serialized. Dates arrive through `--reference-date`.

Validation. `validate_instance` implements the subset of JSON Schema draft
2020-12 that the four schemas in `schemas/` actually use: `$ref` into
`$defs`, `type`, `enum`, `const`, `required`, `properties`,
`additionalProperties`, `items`, `minItems`, `minLength`, `maxLength`,
`pattern`, `minimum`, `maximum`, `uniqueItems` and `format`. Draft 2020-12
treats `format` as an annotation by default; this validator asserts it,
because a date that does not parse and a URL that is not http are exactly
the defects these adapters exist to refuse.

Standard library only. No network access anywhere in this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_common import EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE  # noqa: E402

ENVELOPE_VERSION = 1

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"

ADAPTER_DISCLAIMER = (
    "Structural findings report only. Every finding here was convicted by a named "
    "structural procedure or by a deterministic Layer 0 scanner, and every finding "
    "carries its own evidence span. It does not judge authorship and it is not "
    "evidence about who or what wrote the text."
)

SEVERITY_ORDER = ("HIGH", "MEDIUM", "LOW")
CONFIDENCE_ORDER = ("high", "medium", "low")
PROCEDURES = ("deletion", "inversion", "stranger", "attribution", "load-bearing")
TIERS = (1, 2, 3)

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TYPE_MAP: dict[str, tuple[type, ...]] = {
    "object": (dict,),
    "array": (list,),
    "string": (str,),
    "number": (int, float),
    "integer": (int,),
    "boolean": (bool,),
    "null": (type(None),),
}


class AdapterError(Exception):
    """Raised for any input the adapter refuses. Never escapes as a traceback."""

    def __init__(self, code: str, message: str, errors: list[dict] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.errors = errors or []


def escape_pointer_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def join_pointer(pointer: str, token: object) -> str:
    return f"{pointer}/{escape_pointer_token(str(token))}"


def resolve_ref(ref: str, root_schema: dict) -> dict:
    """Resolve a local `#/$defs/Name` reference. Remote refs are refused."""
    if not ref.startswith("#/"):
        raise AdapterError("unsupported_ref", f"only local $ref is supported, got {ref}")
    node: Any = root_schema
    for raw in ref[2:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or token not in node:
            raise AdapterError("unresolved_ref", f"cannot resolve $ref {ref}")
        node = node[token]
    if not isinstance(node, dict):
        raise AdapterError("unresolved_ref", f"$ref {ref} does not point at a schema")
    return node


def is_type(value: object, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, TYPE_MAP.get(name, ()))


def check_format(value: str, fmt: str) -> str:
    """Return an error message for a bad format value, or an empty string."""
    if fmt == "date":
        if not ISO_DATE_RE.match(value):
            return f"is not an ISO 8601 calendar date in YYYY-MM-DD form: {value!r}"
        try:
            date.fromisoformat(value)
        except ValueError:
            return f"is not a real calendar date: {value!r}"
        return ""
    if fmt == "uri":
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"}:
            return (
                "must be an http or https URL; this adapter refuses every other "
                f"scheme, got {value!r}"
            )
        if not parsed.netloc:
            return f"is a URL with no host: {value!r}"
        return ""
    return ""


def validate_instance(
    instance: object,
    schema: dict,
    root_schema: dict | None = None,
    pointer: str = "",
) -> list[dict]:
    """Validate one instance and return a sorted list of error records."""
    root = root_schema if root_schema is not None else schema
    errors: list[dict] = []

    if "$ref" in schema:
        merged = dict(resolve_ref(schema["$ref"], root))
        for key, value in schema.items():
            if key != "$ref":
                merged[key] = value
        return validate_instance(instance, merged, root, pointer)

    declared = schema.get("type")
    if declared is not None:
        names = declared if isinstance(declared, list) else [declared]
        if not any(is_type(instance, name) for name in names):
            errors.append(
                {
                    "pointer": pointer or "/",
                    "keyword": "type",
                    "message": f"expected type {' or '.join(names)}, got {type(instance).__name__}",
                }
            )
            return sorted_errors(errors)

    if "const" in schema and instance != schema["const"]:
        errors.append(
            {
                "pointer": pointer or "/",
                "keyword": "const",
                "message": f"must equal {schema['const']!r}",
            }
        )

    if "enum" in schema and instance not in schema["enum"]:
        allowed = ", ".join(repr(item) for item in schema["enum"])
        errors.append(
            {
                "pointer": pointer or "/",
                "keyword": "enum",
                "message": f"{instance!r} is not one of: {allowed}",
            }
        )

    if isinstance(instance, str):
        errors.extend(_validate_string(instance, schema, pointer))
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        errors.extend(_validate_number(instance, schema, pointer))
    if isinstance(instance, list):
        errors.extend(_validate_array(instance, schema, root, pointer))
    if isinstance(instance, dict):
        errors.extend(_validate_object(instance, schema, root, pointer))

    return sorted_errors(errors)


def _validate_string(instance: str, schema: dict, pointer: str) -> list[dict]:
    errors: list[dict] = []
    where = pointer or "/"
    minimum = schema.get("minLength")
    if isinstance(minimum, int) and len(instance) < minimum:
        errors.append(
            {"pointer": where, "keyword": "minLength", "message": f"needs at least {minimum} characters"}
        )
    maximum = schema.get("maxLength")
    if isinstance(maximum, int) and len(instance) > maximum:
        errors.append(
            {"pointer": where, "keyword": "maxLength", "message": f"allows at most {maximum} characters"}
        )
    pattern = schema.get("pattern")
    if isinstance(pattern, str) and not re.search(pattern, instance):
        errors.append(
            {"pointer": where, "keyword": "pattern", "message": f"does not match {pattern}"}
        )
    fmt = schema.get("format")
    if isinstance(fmt, str):
        problem = check_format(instance, fmt)
        if problem:
            errors.append({"pointer": where, "keyword": "format", "message": problem})
    return errors


def _validate_number(instance: float, schema: dict, pointer: str) -> list[dict]:
    errors: list[dict] = []
    where = pointer or "/"
    minimum = schema.get("minimum")
    if isinstance(minimum, (int, float)) and instance < minimum:
        errors.append({"pointer": where, "keyword": "minimum", "message": f"must be at least {minimum}"})
    maximum = schema.get("maximum")
    if isinstance(maximum, (int, float)) and instance > maximum:
        errors.append({"pointer": where, "keyword": "maximum", "message": f"must be at most {maximum}"})
    return errors


def _validate_array(instance: list, schema: dict, root: dict, pointer: str) -> list[dict]:
    errors: list[dict] = []
    where = pointer or "/"
    minimum = schema.get("minItems")
    if isinstance(minimum, int) and len(instance) < minimum:
        errors.append({"pointer": where, "keyword": "minItems", "message": f"needs at least {minimum} items"})
    maximum = schema.get("maxItems")
    if isinstance(maximum, int) and len(instance) > maximum:
        errors.append({"pointer": where, "keyword": "maxItems", "message": f"allows at most {maximum} items"})
    if schema.get("uniqueItems") is True:
        seen: list[str] = []
        for item in instance:
            key = json.dumps(item, sort_keys=True, default=str)
            if key in seen:
                errors.append({"pointer": where, "keyword": "uniqueItems", "message": "contains a duplicate item"})
                break
            seen.append(key)
    item_schema = schema.get("items")
    if isinstance(item_schema, dict):
        for index, item in enumerate(instance):
            errors.extend(validate_instance(item, item_schema, root, join_pointer(pointer, index)))
    return errors


def _validate_object(instance: dict, schema: dict, root: dict, pointer: str) -> list[dict]:
    errors: list[dict] = []
    properties = schema.get("properties")
    properties = properties if isinstance(properties, dict) else {}
    for name in schema.get("required", []):
        if name not in instance:
            errors.append(
                {"pointer": join_pointer(pointer, name), "keyword": "required", "message": "is required and missing"}
            )
    for name in sorted(instance):
        if name in properties:
            errors.extend(
                validate_instance(instance[name], properties[name], root, join_pointer(pointer, name))
            )
    if schema.get("additionalProperties") is False:
        for name in sorted(instance):
            if name not in properties:
                errors.append(
                    {
                        "pointer": join_pointer(pointer, name),
                        "keyword": "additionalProperties",
                        "message": f"{name!r} is not a declared property of this object",
                    }
                )
    return errors


def sorted_errors(errors: list[dict]) -> list[dict]:
    unique: dict[tuple[str, str, str], dict] = {}
    for error in errors:
        key = (error["pointer"], error["keyword"], error["message"])
        unique.setdefault(key, error)
    return [unique[key] for key in sorted(unique)]


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    if not path.exists():
        raise AdapterError("missing_schema", f"no such schema file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise AdapterError("invalid_schema", f"schema {name} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise AdapterError("invalid_schema", f"schema {name} must be a JSON object")
    return data


def read_json_input(raw_path: str, label: str = "input") -> dict:
    """Read one JSON object from a path, or from stdin when the path is '-'."""
    if raw_path == "-":
        text = sys.stdin.read()
        origin = "<stdin>"
    else:
        path = Path(raw_path)
        if not path.exists():
            raise AdapterError("missing_input", f"no such {label} file: {raw_path}")
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise AdapterError("unreadable_input", f"cannot read {raw_path}: {exc}") from exc
        origin = raw_path
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise AdapterError(
            "invalid_json",
            f"{label} is not valid JSON",
            [{"pointer": "/", "keyword": "json", "message": f"{origin}: {exc}"}],
        ) from exc
    if not isinstance(data, dict):
        raise AdapterError(
            "invalid_json",
            f"{label} must be a JSON object",
            [{"pointer": "/", "keyword": "type", "message": f"{origin}: top level value is not an object"}],
        )
    return data


def validate_or_refuse(instance: dict, schema_name: str, label: str) -> None:
    schema = load_schema(schema_name)
    errors = validate_instance(instance, schema, schema)
    if errors:
        raise AdapterError(
            "schema_violation",
            f"{label} does not satisfy {schema_name}",
            errors,
        )


def parse_reference_date(value: str | None, fallback: str | None = None) -> str:
    """Return a validated ISO date string. Never reads the system clock."""
    chosen = value if value else fallback
    if not chosen:
        raise AdapterError(
            "missing_reference_date",
            "a reference date is required; pass --reference-date YYYY-MM-DD",
        )
    problem = check_format(chosen, "date")
    if problem:
        raise AdapterError(
            "invalid_reference_date",
            f"reference date {problem}",
            [{"pointer": "/reference_date", "keyword": "format", "message": problem}],
        )
    return chosen


def date_value(value: str, pointer: str) -> date:
    problem = check_format(value, "date")
    if problem:
        raise AdapterError(
            "invalid_date",
            f"date at {pointer} {problem}",
            [{"pointer": pointer, "keyword": "format", "message": problem}],
        )
    return date.fromisoformat(value)


def stable_id(prefix: str, parts: list[str]) -> str:
    """Deterministic short identifier built from the finding's own content."""
    payload = "".join(parts).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=6).hexdigest()
    return f"{prefix}-{digest}"


def normalize_span(span: object) -> dict | None:
    """Return the canonical evidence span, or None when there is no usable one."""
    if not isinstance(span, dict):
        return None
    text = span.get("text")
    if not isinstance(text, str) or not text.strip():
        return None
    path = span.get("path")
    start_line = span.get("start_line")
    if not isinstance(path, str) or not path.strip():
        return None
    if not isinstance(start_line, int) or isinstance(start_line, bool) or start_line < 1:
        return None
    start_column = span.get("start_column")
    start_column = start_column if isinstance(start_column, int) and start_column >= 1 else 1
    end_line = span.get("end_line")
    end_line = end_line if isinstance(end_line, int) and end_line >= start_line else start_line
    end_column = span.get("end_column")
    end_column = end_column if isinstance(end_column, int) and end_column >= 1 else start_column
    return {
        "end_column": end_column,
        "end_line": end_line,
        "path": path.strip(),
        "start_column": start_column,
        "start_line": start_line,
        "text": collapse(text),
    }


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def spans_overlap(left: dict, right: dict) -> bool:
    if left["path"] != right["path"]:
        return False
    return left["start_line"] <= right["end_line"] and right["start_line"] <= left["end_line"]


def severity_rank(value: str) -> int:
    return SEVERITY_ORDER.index(value) if value in SEVERITY_ORDER else len(SEVERITY_ORDER)


def confidence_rank(value: str) -> int:
    return CONFIDENCE_ORDER.index(value) if value in CONFIDENCE_ORDER else len(CONFIDENCE_ORDER)


def add_output_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output",
        default="-",
        help="Where to write the result. Use - for stdout, which is the default.",
    )


def write_output(text: str, destination: str) -> None:
    if destination == "-":
        sys.stdout.write(text)
        return
    path = Path(destination)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump_json(payload: dict, destination: str) -> None:
    write_output(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", destination)


def error_envelope(tool: str, exc: AdapterError) -> dict:
    """The structured refusal every adapter emits instead of a traceback."""
    return {
        "envelope_version": ENVELOPE_VERSION,
        "error": {"code": exc.code, "message": exc.message},
        "errors": exc.errors,
        "note": ADAPTER_DISCLAIMER,
        "ok": False,
        "tool": tool,
    }


def run_adapter(main_function, tool: str, argv: list[str] | None = None) -> int:
    """Run an adapter main and map AdapterError to a structured refusal."""
    try:
        return main_function(argv)
    except AdapterError as exc:
        sys.stdout.write(json.dumps(error_envelope(tool, exc), indent=2, sort_keys=True) + "\n")
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_CLEAN


__all__ = [
    "ADAPTER_DISCLAIMER",
    "AdapterError",
    "CONFIDENCE_ORDER",
    "ENVELOPE_VERSION",
    "EXIT_CLEAN",
    "EXIT_FINDINGS",
    "EXIT_USAGE",
    "PROCEDURES",
    "SEVERITY_ORDER",
    "TIERS",
    "add_output_argument",
    "check_format",
    "collapse",
    "confidence_rank",
    "date_value",
    "dump_json",
    "error_envelope",
    "load_schema",
    "normalize_span",
    "parse_reference_date",
    "read_json_input",
    "run_adapter",
    "severity_rank",
    "spans_overlap",
    "stable_id",
    "validate_instance",
    "validate_or_refuse",
    "write_output",
]
