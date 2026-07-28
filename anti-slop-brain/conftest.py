"""Pytest configuration for anti-slop-brain.

The suites under ``tests/`` are standalone scripts with their own runner and
their own assertion helpers. Their test functions take a positional ``tmp``
path, which pytest tries to satisfy as a fixture that does not exist, so a bare
``python3 -m pytest`` reports collection errors rather than real failures.
Nothing is broken when that happens: the suites pass when run the way CI runs
them.

    cd anti-slop-brain
    python3 tests/test_scanners.py     # 107 checks
    python3 tests/test_adapters.py     # 207 checks
    python3 tests/test_pipeline.py

This file stops pytest collecting those modules so the reflex command reports
nothing instead of a wall of errors. It sits at the root of this directory
rather than inside ``tests/`` so that it keeps working if this directory is
extracted and used on its own.
"""

collect_ignore_glob = ["tests/*.py"]


def pytest_report_header(config):
    """Point the reader at the command that actually runs the suites."""
    return (
        "anti-slop-brain: tests/ is deliberately not collected by pytest. "
        "Run them directly: python3 tests/test_scanners.py, "
        "python3 tests/test_adapters.py, python3 tests/test_pipeline.py"
    )
