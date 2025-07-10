---
id: ARCH-pipeline-orchestration
title: "Pipeline Orchestration"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-10
tags: [python, orchestration, etl]
depends_on: [ARCH-pipeline-step-validate, ARCH-pipeline-step-load-stage, ARCH-pipeline-step-transform, ARCH-pipeline-step-publish, ARCH-database-schemas]
referenced_by: []
---
## Context
The orchestrator coordinates the execution of pipeline steps, ensuring that each file is processed in the correct order and only once.

## Structure
Implemented as a Python script (`run_pipeline.py`) that uses SQLAlchemy and utility modules for database access and logging.

## Behavior
The orchestrator script queries the `meta` tables to drive the pipeline forward. The typical flow for a new file is:
1.  Queries `meta.ingestion_log` to find files ready for validation and triggers `validate.py`.
2.  Queries `meta.validation_log` to find successfully created Parquet files and triggers `load_stage.py`.
3.  Queries the stage load logs to find periods ready for transformation and triggers `transform.py`.
4.  Finally, it triggers `publish.py` to update the data marts.

This stateful, metadata-driven approach makes the pipeline resumable and idempotent at a process level.
## Evolution
### Historical
- v1: Initial design. 