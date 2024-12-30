"""Starrocks target sink class, which handles writing streams."""

from __future__ import annotations

import functools
from typing import Any

import sqlalchemy as sa
from singer_sdk.connectors import SQLConnector
from singer_sdk.connectors.sql import JSONSchemaToSQL
from singer_sdk.sinks import SQLSink
from starrocks.datatype import JSON


class JSONSchemaToStarrocks(JSONSchemaToSQL):
    """Convert a JSON schema to a Starrocks-compatible SQL type."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the type converter."""
        super().__init__(*args, **kwargs)
        if self._max_varchar_length is None:
            msg = "max_varchar_length is required for Starrocks"
            raise ValueError(msg)

    def handle_raw_string(self, schema: dict) -> sa.types.TypeEngine:
        """Handle a raw string type."""
        max_length: int | None = schema.get("maxLength")

        if max_length and self._max_varchar_length:
            max_length = min(max_length, self._max_varchar_length)

        return sa.types.VARCHAR(length=max_length or self._max_varchar_length)


class StarrocksConnector(SQLConnector):
    """The connector for Starrocks.

    This class handles all DDL and type conversions.
    """

    allow_column_add: bool = True  # Whether ADD COLUMN is supported.
    allow_column_rename: bool = True  # Whether RENAME COLUMN is supported.
    allow_column_alter: bool = False  # Whether altering column types is supported.
    allow_merge_upsert: bool = False  # Whether MERGE UPSERT is supported.
    allow_overwrite: bool = False  # Whether overwrite load method is supported.
    allow_temp_tables: bool = True  # Whether temp tables are supported.

    #: The maximum VARCHAR length for this connector.
    #: https://docs.starrocks.io/docs/sql-reference/data-types/string-type/VARCHAR/
    #: TODO: Use the database version to determine if this should be 65533 (<2.1)
    #: or 1048576 (>=2.1).
    max_varchar_length: int = 65_533

    @functools.cached_property
    def jsonschema_to_sql(self) -> JSONSchemaToStarrocks:
        """The JSON-to-SQL type mapper object for this SQL connector."""
        to_sql = JSONSchemaToStarrocks(max_varchar_length=self.max_varchar_length)
        to_sql.register_type_handler("array", JSON)
        to_sql.register_type_handler("object", JSON)
        return to_sql

    def get_sqlalchemy_url(self, config: dict) -> str:
        """Generates a SQLAlchemy URL for Starrocks.

        Args:
            config: The configuration for the connector.
        """
        return super().get_sqlalchemy_url(config)


class StarrocksSink(SQLSink):
    """Starrocks target sink class."""

    connector_class = StarrocksConnector
