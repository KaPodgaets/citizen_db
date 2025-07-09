---
id: ARCH-pipeline-orchestration
title: "Pipeline Orchestration"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-09
tags: [python, orchestration, etl]
depends_on: [ARCH-pipeline-step-transform, ARCH-pipeline-step-publish, ARCH-database-schemas]
referenced_by: []
---
## Context
The orchestrator coordinates the execution of pipeline steps, ensuring that each file is processed in the correct order and only once.

## Structure
Implemented as a Python script (`run_pipeline.py`) that uses SQLAlchemy and utility modules for database access and logging.

## Behavior
The orchestrator script queries the `meta` tables to identify files that have been successfully validated but not yet transformed and published. For each new valid dataset, it triggers the `transform.py` script, followed by the `publish.py` script to complete the end-to-end data processing for that dataset. This ensures a stateful and smart execution flow.

The script checks the `meta.ingestion_log` and `meta.validation_log` to determine the next action for each file, making the pipeline resumable and idempotent at a process level.
## Evolution
### Historical
- v1: Initial design. 