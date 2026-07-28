#!/usr/bin/env python3
"""Reproducible date resolution for the vault build scripts.

A generated artifact that stamps `date.today()` is not reproducible. The
same inputs produce a different tree tomorrow, so a drift check that
rebuilds a committed artifact and diffs it turns red on the calendar rather
than on a real change. Every script that stamps a date into generated
output resolves it through this module instead of reading the clock.

Resolution order, highest priority first:

1. `--reference-date YYYY-MM-DD` on the command line.
2. `SOURCE_DATE_EPOCH`, the reproducible-builds convention: an integer
   number of seconds since the Unix epoch, interpreted in UTC.
3. The caller's fallback. That is `date.today()` for the general purpose
   scripts, which are meant to stamp the real day, and a pinned constant
   for `build_demo_vault.py`, whose output is committed to this repository.

Standard library only. No network access anywhere in this module.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import os

SOURCE_DATE_EPOCH = "SOURCE_DATE_EPOCH"


class ReferenceDateError(ValueError):
    """Raised when a pinned date cannot be parsed. Callers exit 2 on this."""


def parse_iso_date(value: str, origin: str) -> date:
    """Parse an ISO 8601 calendar date, naming the origin in the error."""
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise ReferenceDateError(
            f"{origin} must be an ISO calendar date in YYYY-MM-DD form: {value!r}"
        ) from exc


def date_from_source_date_epoch(raw: str) -> date:
    """Convert a SOURCE_DATE_EPOCH value to a UTC calendar date.

    UTC is not a detail. The reproducible-builds convention fixes the
    instant, so reading it in local time would put two contributors in
    different timezones on different days from the same pin.
    """
    try:
        seconds = int(raw.strip())
    except ValueError as exc:
        raise ReferenceDateError(
            f"{SOURCE_DATE_EPOCH} must be an integer number of seconds since the "
            f"Unix epoch: {raw!r}"
        ) from exc
    try:
        return datetime.fromtimestamp(seconds, timezone.utc).date()
    except (OverflowError, OSError, ValueError) as exc:
        raise ReferenceDateError(
            f"{SOURCE_DATE_EPOCH} is out of range: {raw!r}"
        ) from exc


def resolve_reference_date(
    explicit: str | None = None,
    *,
    fallback: date | None = None,
    env: dict[str, str] | None = None,
) -> date:
    """Return the calendar date this run stamps into generated output.

    The clock is read at most once, here, and only when neither the caller
    nor the environment pinned a date and no fallback was supplied.
    """
    environment = os.environ if env is None else env
    if explicit:
        return parse_iso_date(explicit, "--reference-date")
    raw = environment.get(SOURCE_DATE_EPOCH)
    if raw and raw.strip():
        return date_from_source_date_epoch(raw)
    if fallback is not None:
        return fallback
    return date.today()


def add_reference_date_argument(parser: argparse.ArgumentParser) -> None:
    """Attach the shared date pin option."""
    parser.add_argument(
        "--reference-date",
        default=None,
        metavar="YYYY-MM-DD",
        help="Pin every generated date stamp to this calendar date. Falls back to "
             "the SOURCE_DATE_EPOCH environment variable, then to today.",
    )
