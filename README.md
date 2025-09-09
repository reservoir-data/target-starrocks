# target-starrocks

`target-starrocks` is a Singer target for [StarRocks].

Build with the [Meltano Target SDK][Singer SDK].

## Installation

Install from PyPI:

```bash
uv tool install target-starrocks
```

Install from GitHub:

```bash
uv tool install git+https://github.com/reservoir-data/target-starrocks.git@main
```

## Supported Python Versions

* 3.13
* 3.14

## Configuration

### Accepted Config Options

| Setting                           | Required | Default                       | Description                                                                                                                                                                                                                                                                                      |
| :-------------------------------- | :------- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| user                              | False    | None                          | User for the StarRocks database                                                                                                                                                                                                                                                                  |
| password                          | False    | None                          | Password for the StarRocks database                                                                                                                                                                                                                                                              |
| host                              | False    | None                          | Host for the StarRocks database                                                                                                                                                                                                                                                                  |
| port                              | False    | 9030                          | Port for the StarRocks database                                                                                                                                                                                                                                                                  |
| database                          | True     | None                          | Database name for the StarRocks database                                                                                                                                                                                                                                                         |

#### Additional Config Options

The following built-in configuration options are also supported:

| Setting                           | Required | Default                       | Description                                                                                                                                                                                                                                                                                      |
| :-------------------------------- | :------- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| default_target_schema             | False    | None                          | The default target database schema name to use for all streams.                                                                                                                                                                                                                                  |
| hard_delete                       | False    | 0                             | Hard delete records.                                                                                                                                                                                                                                                                             |
| add_record_metadata               | False    | None                          | Whether to add metadata fields to records.                                                                                                                                                                                                                                                       |
| load_method                       | False    | TargetLoadMethods.APPEND_ONLY | The method to use when loading data into the destination. `append-only` will always write all input records whether that records already exists or not. `upsert` will update existing records and insert new records. `overwrite` will delete all existing records and insert all input records. |
| batch_size_rows                   | False    | None                          | Maximum number of rows in each batch.                                                                                                                                                                                                                                                            |
| process_activate_version_messages | False    | 1                             | Whether to process `ACTIVATE_VERSION` messages.                                                                                                                                                                                                                                                  |
| validate_records                  | False    | 1                             | Whether to validate the schema of the incoming streams.                                                                                                                                                                                                                                          |
| stream_maps                       | False    | None                          | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                                                                      |
| stream_map_config                 | False    | None                          | User-defined config values to be used within map expressions.                                                                                                                                                                                                                                    |
| faker_config                      | False    | None                          | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly).                                         |
| faker_config.seed                 | False    | None                          | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                                                        |
| faker_config.locale               | False    | None                          | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                                                            |
| flattening_enabled                | False    | None                          | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                                                                   |
| flattening_max_depth              | False    | None                          | The max depth to flatten schemas.                                                                                                                                                                                                                                                                |

A full list of supported settings and capabilities is available by running: `target-starrocks --about`

### Configure using environment variables

This Singer target will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Authentication and Authorization

## Usage

You can easily run `target-starrocks` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-starrocks --version
target-starrocks --help
# Test using the "Smoke Test" tap:
tap-smoke-test | target-starrocks --config /path/to/target-starrocks-config.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # or see https://docs.astral.sh/uv/getting-started/installation/
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
uv run pytest
```

You can also test the `target-starrocks` CLI interface directly using `uv run`:

```bash
uv run target-starrocks --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
uv tool install meltano
meltano config meltano set venv.backend uv

# Initialize meltano within this directory
cd target-starrocks
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-starrocks --version

# OR run a test EL pipeline with the Smoke Test sample tap:
meltano run tap-smoke-test target-starrocks
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano Singer SDK to
develop your own Singer taps and targets.

[StarRocks]: https://starrocks.io
[Singer SDK]: https://sdk.meltano.com
