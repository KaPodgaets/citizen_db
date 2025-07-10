---
id: ARCH-pipeline-step-transform
title: "Pipeline Step: Transformation (SCD-2 Core)"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [python, transform, etl, scd2]
depends_on: [ARCH-database-schemas, ARCH-transform-rules, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
This component is implemented in `transform.py`. It imports and uses cleansing functions from modules in the `src/transformations/` directory.

## Behavior
The script reads clean, validated data for a specific period (e.g., '2025-06') from the `stage` schema tables in the database, using a `WHERE _data_period = ?` clause. It applies various data cleansing and standardization rules defined in `src/transformations/`. Using pandas, it compares the incoming data against the current data in the `core.*` tables to identify new, unchanged, and changed records. For changed records, it expires the old version and inserts a new one. It then uses SQLAlchemy Core for efficient bulk INSERT and UPDATE operations against the database to apply these changes. It will also support a `--rollback` feature, which uses the `meta.dataset_version` table, to revert a specific data load.

## Evolution
### Historical
- v1: Initial design. 