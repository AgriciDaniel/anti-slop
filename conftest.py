"""Pytest configuration for the anti-slop repository.

This repository has no pytest suite. The deterministic suites live in
``anti-slop-brain/tests/`` and are standalone scripts with their own runner,
so ``anti-slop-brain/conftest.py`` excludes them from collection.

This file exists so that a contributor running ``python3 -m pytest`` from the
repository root is told what to run instead. ``pytest_report_header`` only
fires for a conftest at the rootdir, which is why the hook is repeated here.
"""

_COMMANDS = (
    "cd anti-slop-brain && python3 tests/test_scanners.py "
    "&& python3 tests/test_adapters.py && python3 tests/test_pipeline.py"
)


def pytest_report_header(config):
    """Point the reader at the command that actually runs the suites."""
    return (
        "anti-slop: no pytest suite. The deterministic suites are standalone "
        "scripts and are not collected. Run them directly:\n  " + _COMMANDS
    )
