---
id: ARCH-pipeline-utilities
title: "Pipeline Core Utilities"
type: component
layer: infrastructure
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, utilities, config, logging, database, sqlalchemy]
depends_on: []
referenced_by: []
---
## Context
This component provides a set of shared, reusable modules that support the core pipeline scripts. It centralizes common functionalities like configuration management, database connectivity, and logging to promote consistency and maintainability across the application.

## Structure
The utilities are organized into separate modules within the `src/utils/` directory:
- `config.py`: Manages all application configuration.
- `db.py`: Manages database connections and execution.
- `logging_config.py`: Configures application-wide logging.

## Behavior
- **`config.py`**: Uses `pydantic-settings` to load configuration from `.env` files, allowing for secure management of secrets and environment-specific settings.
- **`db.py`**: Initializes a singleton SQLAlchemy Engine, managing a connection pool for efficient database interaction. It provides helper functions for executing statements, especially for bulk operations using SQLAlchemy Core to ensure performance.
- **`logging_config.py`**: Sets up the root logger with two handlers: one for rich, readable console output, and a custom database handler that writes detailed log entries to the `meta.etl_audit` table. This provides robust, centralized auditing.

## Evolution
### Planned
- Initial implementation of the three utility modules.

### Historical
- v1: Initial design. 