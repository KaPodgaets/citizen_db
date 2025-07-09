---
id: ARCH-pipeline-step-transform
title: "Pipeline Step: Transformation (SCD-2 Core)"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, transform, etl, scd2]
depends_on: [ARCH-database-schemas, ARCH-transform-rules, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The Transformation step is the heart of the ELT process. It takes clean, staged data and applies business logic to produce a historized, high-quality `core` data layer using a Slowly Changing Dimension (SCD) Type 2 pattern.

## Structure
This component is implemented in `transform.py`. It imports and uses cleansing functions from modules in the `src/transformations/` directory.

## Behavior
The script reads a clean Parquet file from the `data/stage/` directory. It applies various data cleansing and standardization rules defined in `src/transformations/`. Using pandas, it compares the incoming data against the current data in the `core.*` tables to identify new records, unchanged records, and changed records. For changed records, it expires the old version and inserts a new one. It then uses SQLAlchemy Core for efficient bulk INSERT and UPDATE operations against the database to apply these changes. It will also support a `--rollback` feature, which uses the `meta.dataset_version` table, to revert a specific data load.

## Evolution
### Planned
- Initial implementation of SCD-2 logic.
- Add a `--rollback` flag that uses `meta.dataset_version` to revert a specific data load version.

### Historical
- v1: Initial design. 