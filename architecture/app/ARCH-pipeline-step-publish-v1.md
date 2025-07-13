---
id: ARCH-pipeline-step-publish
title: "Pipeline Step: Publish (Mart)"
type: component
layer: application
owner: "@team-data"
version: v1
status: current
created: 2025-07-09
updated: 2025-07-13
tags: [python, publish, etl, star-schema]
depends_on: [ARCH-database-schemas, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The Publish step is responsible for making analytics-ready data available to BI tools and downstream consumers. This document describes the generic concept, where a simple script (`publish.py`) can be used for simple mart updates.

## Structure
Implemented as a Python script (`publish.py`) that uses SQLAlchemy and utility modules for database access and logging.

## Behavior
The script connects to the MS SQL database using utilities from `src/utils/db.py`. It executes pre-defined SQL scripts or stored procedures that truncate the `mart.*` tables and reload them with fresh data from the historized `core.*` layer. This ensures the mart always reflects the latest state of the core data.

## Evolution
### Historical
- v1: Initial design. 
### Planned
- For complex data marts requiring specific logic, dedicated scripts will be created (e.g., `publish_citizen_mart.py`). See `ARCH-pipeline-step-publish-citizen-datamart`. 