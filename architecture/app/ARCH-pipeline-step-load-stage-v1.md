---
id: ARCH-pipeline-step-load-stage
title: "Pipeline Step: Load Stage"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-10
updated: 2025-07-13
tags: [python, etl, parquet, mssql, transaction]
depends_on: [ARCH-database-schemas, ARCH-pipeline-utilities, ARCH-pipeline-step-validate]
referenced_by: []
---
## Context
This component acts as the bridge between the file-based staging layer (validated Parquet files) and the database staging layer (`stage` schema). Its primary purpose is to load clean, structured data into the database in a transactional and idempotent manner, preparing it for the final transformations into the `core` layer.

## Structure
This component is implemented as a Python script, `src/load_stage.py`. It is triggered by the orchestrator for each successfully validated Parquet file, identified via `meta.validation_log`. It logs its own execution results to `meta.stage_load_log`.

## Behavior
The script implements a period-aware, transactional "upsert" (delete-then-append) logic:
1.  It accepts a `--validation-log-id` to retrieve the source Parquet file path, period, and dataset from the metadata tables.
2.  It reads the Parquet file from `data/stage/cleaned/` into a pandas DataFrame.
3.  It enriches the DataFrame with metadata columns: `_data_period` (from the log) and `_source_parquet_path` (the path of the file being loaded).
4.  Within a single database transaction, it first executes a `DELETE` statement against the target `stage` table, removing all rows matching the given `_data_period`.
5.  It then appends the new, enriched DataFrame to the same table.
6.  On success or failure, it inserts a corresponding record into the `meta.stage_load_log` table, linking back to the `validation_log_id`.
7.  If any database operation fails, the entire transaction is rolled back, leaving the `stage` table in its original state for that period.

## Evolution
### Historical
- v1: Initial design. Status changed from `planned` to `current` as part of the resilient core rebuild initiative. Behavior updated to include enhanced auditing via `meta.stage_load_log` and additional source traceability columns. 