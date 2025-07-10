---
id: ARCH-pipeline-step-load-stage
title: "Pipeline Step: Load Stage DB"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-10
updated: 2025-07-10
tags: [python, etl, parquet, mssql, transaction]
depends_on: [ARCH-database-schemas, ARCH-pipeline-utilities, ARCH-pipeline-step-validate]
referenced_by: []
---
## Context
This component acts as the bridge between the file-based staging layer (validated Parquet files) and the database staging layer (`stage` schema). Its primary purpose is to load clean, structured data into the database in a transactional and idempotent manner, preparing it for the final transformations into the `core` layer.

## Structure
This component is implemented as a new Python script, `src/load_stage.py`. It is triggered by the orchestrator after a Parquet file has been successfully created by the validation step.

## Behavior
The script implements a period-aware, transactional "upsert" (delete-then-append) logic:
1.  It accepts a Parquet file path, the data period (e.g., '2025-06'), and the dataset name as arguments.
2.  It reads the Parquet file from `data/stage/cleaned/` into a pandas DataFrame.
3.  It adds a `_data_period` column to the DataFrame, populated with the period argument.
4.  Within a single database transaction, it first executes a `DELETE` statement against the target `stage` table, removing all rows matching the given `_data_period`.
5.  It then appends the new DataFrame to the same table.
6.  If both operations succeed, the transaction is committed. If any error occurs, the transaction is rolled back, leaving the database in its original state.

## Evolution
### Historical
- v1: Initial design, created to support the new file-based-to-DB staging architecture. 