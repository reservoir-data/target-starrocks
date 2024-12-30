"""StarRocks target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import SQLTarget

from target_starrocks.sinks import (
    StarRocksSink,
)


class TargetStarRocks(SQLTarget):
    """Sample target for StarRocks."""

    name = "target-starrocks"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "user",
            th.StringType,
            title="User",
            description="User for the StarRocks database",
        ),
        th.Property(
            "password",
            th.StringType,
            title="Username",
            description="Password for the StarRocks database",
            secret=True,
        ),
        th.Property(
            "host",
            th.StringType,
            title="Host",
            description="Host for the StarRocks database",
        ),
        th.Property(
            "port",
            th.IntegerType,
            title="Port",
            description="Port for the StarRocks database",
            default=9030,
        ),
        th.Property(
            "database",
            th.StringType,
            title="Database",
            description="Database name for the StarRocks database",
            required=True,
        ),
    ).to_dict()

    default_sink_class = StarRocksSink


if __name__ == "__main__":
    TargetStarRocks.cli()
