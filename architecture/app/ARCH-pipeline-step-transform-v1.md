---
id: ARCH-pipeline-step-transform
title: "Pipeline Step: Transform"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-13
tags: [python, transform, etl, scd2]
depends_on: [ARCH-database-schemas, ARCH-transform-rules, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The transform step applies business logic and data cleansing rules to the validated data in the `stage` schema, transforming it into the historized `core` schema using Slowly Changing Dimension (SCD) Type 2 patterns.

## Structure
This component is implemented in `transform.py`. It imports and uses cleansing functions from modules in the `src/transformations/` directory.

## Behavior
The script is triggered by the orchestrator for a specific dataset and period, based on work identified in the `meta.transform_log` table. It reads the latest available data for that period from the `stage` schema tables. It then applies various data cleansing and standardization rules defined in `src/transformations/`. Using pandas, it compares the incoming data against the current data in the `core.*` tables to identify new, unchanged, and changed records. For changed records, it expires the old version and inserts a new one. It then uses SQLAlchemy Core for efficient bulk INSERT and UPDATE operations against the database to apply these changes. On success or failure, it updates its status in `meta.transform_log`.

## Evolution
### Planned
- **Resilient Execution**: The script's execution will be governed by the orchestrator and the `meta.transform_log` table. If the script fails due to a transient error, the orchestrator will be able to re-trigger it once by checking the `retry_count` in the log table. This prevents temporary issues from halting the entire pipeline.

### Historical
- **2025-07-10**: Adapted to be period-aware, processing data from the `stage` layer for a specific period passed as an argument. 