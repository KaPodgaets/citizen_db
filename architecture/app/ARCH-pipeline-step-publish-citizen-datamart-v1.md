---
id: ARCH-pipeline-step-publish-citizen-datamart
title: "Pipeline Step: Publish Citizen Datamart"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-13
updated: 2025-07-13
tags: [python, publish, etl, datamart]
depends_on: [ARCH-datamart-citizen, ARCH-pipeline-step-transform, ARCH-pipeline-orchestration]
referenced_by: []
---
## Context
This component is a specialized publishing script responsible for creating and populating the `mart.citizen_datamart` table. It consolidates information from multiple `core` tables into a single, denormalized, analytics-ready view.

## Structure
This component is implemented as a standalone Python script, `src/publish_citizen_mart.py`. It uses the shared `src/utils/db.py` utility to connect to the database. The core logic is contained within a complex SQL query embedded in the script.

## Behavior
The script is triggered by the `run_pipeline.py` orchestrator after the `transform` step has successfully populated the `core` tables.

The process is a full `TRUNCATE` and `INSERT`, ensuring the datamart is always a fresh reflection of the current state of the core data. The main SQL query performs the following key operations:
- Uses `core.av_bait` as the base table.
- Left joins to `core.welfare_patients` to determine the `is_welfare_patient` flag.
- Uses a Common Table Expression (CTE) with `ROW_NUMBER()` to rank and pivot up to three phone numbers per citizen from `core.phone_numbers`, prioritizing the 'mobile' type.
- Calculates boolean flags like `has_phone` and `has_mobile_phone`.

## Evolution
### Historical
- v1: Initial implementation for the citizen datamart. 