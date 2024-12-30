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
            "sqlalchemy_url",
            th.StringType,
            secret=True,  # Flag config as protected.
            title="SQLAlchemy URL",
            description="SQLAlchemy connection string",
        ),
    ).to_dict()

    default_sink_class = StarrocksSink


if __name__ == "__main__":
    TargetStarrocks.cli()
