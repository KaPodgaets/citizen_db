---
id: ARCH-pipeline-orchestration
title: "Pipeline Orchestration"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, orchestration, etl]
depends_on: [ARCH-pipeline-step-transform, ARCH-pipeline-step-publish, ARCH-database-schemas]
referenced_by: []
---
## Context
This component is the main entry point for running the data transformation and publishing workflow in an automated fashion. It is responsible for orchestrating the execution of subsequent pipeline steps based on the current state of the data, as tracked in the metadata database.

## Structure
The core of this component is the `run_pipeline.py` script. It relies on the metadata schema to determine its course of action.

## Behavior
The orchestrator script queries the `meta` tables to identify files that have been successfully validated but not yet transformed and published. For each new valid dataset, it triggers the `transform.py` script, followed by the `publish.py` script to complete the end-to-end data processing for that dataset. This ensures a stateful and smart execution flow.

## Evolution
### Planned
- Initial implementation as described.

### Historical
- v1: Initial design. 