"""Tests standard target features using the built-in SDK tests library."""

from __future__ import annotations

import pytest
from singer_sdk.testing import get_target_test_class

from target_starrocks.target import TargetStarRocks

# Run standard built-in target tests from the SDK:
StandardTargetTests = get_target_test_class(target_class=TargetStarRocks, config={})


class TestTargetStarRocks(StandardTargetTests):  # type: ignore[misc, valid-type]
    """Standard Target Tests."""

    @pytest.fixture(scope="class")
    def resource(self):  # noqa: ANN201
        """Generic external resource.

        This fixture is useful for setup and teardown of external resources,
        such output folders, tables, buckets etc. for use during testing.

        Example usage can be found in the SDK samples test suite:
        https://github.com/meltano/sdk/tree/main/tests/samples
        """
        return "resource"
