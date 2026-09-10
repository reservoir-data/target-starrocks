"""Pytest configuration file.

Copyright (c) 2026 Edgar-Ramírez Mondragón
"""

from __future__ import annotations

import pytest


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests that require a live API key."""
    test_name = item.name.split("::")[-1]

    if test_name == "test_target_schema_no_properties":
        item.add_marker(
            pytest.mark.xfail(
                reason="Data type of first column cannot be JSON",
            ),
        )
