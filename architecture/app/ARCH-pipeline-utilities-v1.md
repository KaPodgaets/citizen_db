---
id: ARCH-pipeline-utilities
title: "Pipeline Core Utilities"
type: component
layer: infrastructure
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [python, utilities, config, logging, database, sqlalchemy]
depends_on: [ARCH-data-contract-validation-pydantic]
referenced_by: []
---
## Context
The pipeline relies on a set of robust utility modules to handle configuration, database access, and logging. These utilities ensure that the main pipeline scripts remain focused on business logic and are easy to maintain.

## Structure
The utilities are organized into separate modules within the `src/utils/` directory:
- `config.py`: Manages all application configuration.
- `db.py`: Manages database connections and execution.
- `logging_config.py`: Configures application-wide logging.
- `parsing.py`: Provides helper functions for complex parsing tasks.

## Behavior
- **`config.py`**: Uses `pydantic-settings` to load configuration from `.env` files, allowing for secure management of secrets and environment-specific settings.
- **`db.py`**: Initializes a singleton SQLAlchemy Engine, managing a connection pool for efficient database interaction. It provides helper functions for executing statements, especially for bulk operations using SQLAlchemy Core to ensure performance.
- **`logging_config.py`**: Sets up the root logger with two handlers: one for rich, readable console output, and a custom database handler that writes detailed log entries to the `meta.etl_audit` table. This provides robust, centralized auditing.
- **`parsing.py`**: Contains functions to handle specific data conversion and loading needs, such as:
  - Converting various date formats (Excel numeric, strings) into standard datetime objects.
  - Loading versioned column-mapping contracts from YAML files, validating their structure using Pydantic models from `src/models/contracts.py`.

## Evolution
### Historical
- v1: Initial design. 