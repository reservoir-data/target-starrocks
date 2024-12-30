"""StarRocks target sink class, which handles writing streams."""

from __future__ import annotations

import functools
from typing import Any

import sqlalchemy as sa
from singer_sdk.connectors import SQLConnector
from singer_sdk.connectors.sql import JSONSchemaToSQL
from singer_sdk.sinks import SQLSink
from starrocks.datatype import JSON


class JSONSchemaToStarRocks(JSONSchemaToSQL):
    """Convert a JSON schema to a StarRocks-compatible SQL type."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the type converter."""
        super().__init__(*args, **kwargs)
        if self._max_varchar_length is None:
            msg = "max_varchar_length is required for StarRocks"
            raise ValueError(msg)

    def handle_raw_string(self, schema: dict) -> sa.types.TypeEngine:
        """Handle a raw string type."""
        max_length: int | None = schema.get("maxLength")

        if max_length and self._max_varchar_length:
            max_length = min(max_length, self._max_varchar_length)

        return sa.types.VARCHAR(length=max_length or self._max_varchar_length)


class StarRocksConnector(SQLConnector):
    """The connector for StarRocks.

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
    def jsonschema_to_sql(self) -> JSONSchemaToStarRocks:
        """The JSON-to-SQL type mapper object for this SQL connector."""
        to_sql = JSONSchemaToStarRocks(max_varchar_length=self.max_varchar_length)
        to_sql.register_type_handler("array", JSON)
        to_sql.register_type_handler("object", JSON)
        return to_sql

    def get_sqlalchemy_url(self, config: dict) -> str:
        """Generates a SQLAlchemy URL for StarRocks.

        Args:
            config: The configuration for the connector.
        """
        return sa.URL(
            drivername="starrocks",
            username=config.get("user"),
            password=config.get("password"),
            host=config.get("host"),
            port=config.get("port"),
            database=config["database"],
            query={},
        ).render_as_string(hide_password=False)


class StarRocksSink(SQLSink):
    """StarRocks target sink class."""

    connector_class = StarRocksConnector
