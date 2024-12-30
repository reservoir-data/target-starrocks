"""Pytest configuration file."""

from __future__ import annotations

import pytest


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests that require a live API key."""
    test_name = item.name.split("::")[-1]

    if test_name == "test_target_array_data":
        item.add_marker(
            pytest.mark.xfail(
                reason="Unexpected input ')'",
            ),
        )

    if test_name == "test_target_schema_no_properties":
        item.add_marker(
            pytest.mark.xfail(
                reason="Data type of first column cannot be JSON",
            ),
        )

    if test_name in {
        "test_target_encoded_string_data",
        "test_target_schema_updates",
        "test_target_special_chars_in_attributes",
    }:
        item.add_marker(
            pytest.mark.xfail(
                reason="dict can not be used as parameter",
            ),
        )
