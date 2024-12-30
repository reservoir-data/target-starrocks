"""Starrocks target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import SQLTarget

from target_starrocks.sinks import (
    StarrocksSink,
)


class TargetStarrocks(SQLTarget):
    """Sample target for Starrocks."""

    name = "target-starrocks"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "user",
            th.StringType,
            title="User",
            description="User for the Starrocks database",
        ),
        th.Property(
            "password",
            th.StringType,
            title="Username",
            description="Password for the Starrocks database",
            secret=True,
        ),
        th.Property(
            "host",
            th.StringType,
            title="Host",
            description="Host for the Starrocks database",
        ),
        th.Property(
            "port",
            th.IntegerType,
            title="Port",
            description="Port for the Starrocks database",
            default=9030,
        ),
        th.Property(
            "database",
            th.StringType,
            title="Database",
            description="Database name for the Starrocks database",
            required=True,
        ),
    ).to_dict()

    default_sink_class = StarrocksSink


if __name__ == "__main__":
    TargetStarrocks.cli()
