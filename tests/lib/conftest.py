"""Fixtures for the custom-code test tree (`src/fastvm/lib/`).

Tests are split into two subtrees:

* ``tests/lib/offline/`` — pure unit tests for the helpers (tar packing,
  shell-string wrap, polling error paths). These run on every PR.
* ``tests/lib/live/`` — workflow-style tests that hit the real API. Gated on
  ``FASTVM_API_KEY``; otherwise they skip. These run on ``workflow_dispatch``
  and nightly CI.
"""

from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:  # noqa: ARG001
    # Tests under ``tests/lib/live/`` are auto-marked ``live`` and auto-skipped
    # when ``FASTVM_API_KEY`` isn't set, so they don't run on the base PR CI.
    has_key = bool(os.environ.get("FASTVM_API_KEY"))
    for item in items:
        path = str(item.fspath)
        if "/tests/lib/live/" not in path.replace("\\", "/"):
            continue
        item.add_marker(pytest.mark.live)
        if not has_key:
            item.add_marker(pytest.mark.skip(reason="FASTVM_API_KEY not set; live tests skipped"))
