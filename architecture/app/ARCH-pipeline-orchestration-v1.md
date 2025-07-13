---
id: ARCH-pipeline-orchestration
title: "Pipeline Orchestration"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-13
tags: [python, orchestration, etl]
depends_on: [ARCH-pipeline-step-validate, ARCH-pipeline-step-load-stage, ARCH-pipeline-step-transform, ARCH-pipeline-step-publish, ARCH-database-schemas]
referenced_by: []
---
## Context
The pipeline orchestrator (`run_pipeline.py`) is the central coordinator that manages the flow of data through the entire ETL pipeline. It uses the metadata tables in the `meta` schema to track the state of each file and data period, ensuring idempotent and resumable execution.

## Structure
This component is implemented as a Python script that queries the `meta` tables to determine what work needs to be done and then triggers the appropriate pipeline steps.

## Behavior
The orchestrator script queries the `meta` tables to drive the pipeline forward. The typical flow for a new file is:
1.  Queries `meta.ingestion_log` to find files ready for validation and triggers `validate.py`.
2.  Queries `meta.validation_log` for new 'PASS' records not yet logged in `meta.stage_load_log` and triggers `load_stage.py` for each.
3.  Identifies new work for the transform step by finding successful loads in `meta.stage_load_log` that do not have a 'PASS' record in `meta.transform_log`. It creates 'PENDING' records in `meta.transform_log`.
4.  Triggers `transform.py` for any 'PENDING' records in `meta.transform_log`.
5.  If a transform fails, it updates the log status to 'FAIL' and increments a `retry_count`. It will re-trigger the transform once if `retry_count` is less than 1.
6.  Finally, it triggers `publish.py` to update the data marts.

This stateful, metadata-driven approach makes the pipeline resumable and idempotent at a process level.
## Evolution
### Planned
- **Resilient Transformation**: The orchestration logic will be enhanced to support a single-retry mechanism for the `transform.py` step. This will be governed by a new `meta.transform_log` table, which tracks the status (`PENDING`, `PASS`, `FAIL`) and `retry_count` for each transformation task. This makes the pipeline more resilient to transient failures.

### Historical
- v1: Initial design. 