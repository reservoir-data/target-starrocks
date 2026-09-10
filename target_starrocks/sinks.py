"""StarRocks target sink class, which handles writing streams.

Copyright (c) 2026 Edgar-Ramírez Mondragón
"""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, override

import sqlalchemy as sa
from singer_sdk.sql.connector import FullyQualifiedName, JSONSchemaToSQL, SQLConnector
from singer_sdk.sql.sink import SQLSink
from sqlalchemy.sql import ddl
from sqlalchemy.util import immutabledict
from starrocks.datatype import ARRAY, JSON

if TYPE_CHECKING:
    from collections.abc import Mapping


class JSONSchemaToStarRocks(JSONSchemaToSQL):
    """Convert a JSON schema to a StarRocks-compatible SQL type."""

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the type converter."""
        super().__init__(*args, **kwargs)
        if self._max_varchar_length is None:
            msg = "max_varchar_length is required for StarRocks"
            raise ValueError(msg)

    @override
    def handle_raw_string(self, schema: dict[str, Any]) -> sa.types.VARCHAR:
        """Handle a raw string type."""
        max_length: int | None = schema.get("maxLength")

        if max_length and self._max_varchar_length:
            max_length = min(max_length, self._max_varchar_length)

        return sa.types.VARCHAR(length=max_length or self._max_varchar_length)

    def convert_array_schema(self, schema: dict[str, Any]) -> sa.types.TypeEngine[Any]:
        """Convert array schema to ARRAY type."""
        if items := schema.get("items"):
            return ARRAY(self.to_sql_type(items))
        return sa.types.VARCHAR()


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

    @override
    @functools.cached_property
    def jsonschema_to_sql(self) -> JSONSchemaToStarRocks:
        """The JSON-to-SQL type mapper object for this SQL connector."""
        to_sql = JSONSchemaToStarRocks(max_varchar_length=self.max_varchar_length)
        to_sql.register_format_handler("time", sa.types.VARCHAR)
        to_sql.register_format_handler("uuid", lambda _: sa.types.CHAR(36))
        to_sql.register_type_handler("array", to_sql.convert_array_schema)
        to_sql.register_type_handler("object", JSON)
        return to_sql

    @override
    def get_column_add_ddl(
        self,
        table_name: str | FullyQualifiedName,
        column_name: str,
        column_type: sa.types.TypeEngine[Any],
    ) -> sa.DDL:
        """Get the ADD COLUMN DDL statement.

        Overrides the base implementation to work around a bug in the starrocks
        library where ``column.table`` can be ``None`` when compiling a standalone
        ``CreateColumn`` clause, causing an ``AttributeError`` in
        ``StarRocksDDLCompiler._get_table_agg_info``.

        By attaching the column to a temporary dummy table before compilation, the
        dialect can safely inspect ``column.table.info`` without raising.
        """
        column = sa.Column(column_name, column_type)
        dummy_table = sa.Table("_dummy", sa.MetaData())
        dummy_table.append_column(column)
        create_column_clause = ddl.CreateColumn(column)
        compiled = create_column_clause.compile(self._engine).string
        return sa.DDL(  # type: ignore[no-untyped-call]
            "ALTER TABLE %(table_name)s ADD COLUMN %(create_column_clause)s",
            {
                "table_name": table_name,
                "create_column_clause": compiled,
            },
        )

    @override
    def get_sqlalchemy_url(self, config: Mapping[str, Any]) -> str:
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
            query=immutabledict(),
        ).render_as_string(hide_password=False)


class StarRocksSink(SQLSink[StarRocksConnector]):
    """StarRocks target sink class."""

    connector_class = StarRocksConnector
