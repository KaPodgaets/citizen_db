---
id: ARCH-pipeline-step-publish
title: "Pipeline Step: Publish (Mart)"
type: component
layer: application
owner: "@team-data"
version: v1
status: planned
created: 2025-07-09
updated: 2025-07-09
tags: [python, publish, etl, star-schema]
depends_on: [ARCH-database-schemas, ARCH-pipeline-utilities]
referenced_by: []
---
## Context
The Publish step is responsible for creating the final, denormalized star schema in the data mart. This schema is optimized for consumption by BI tools like Power BI, providing analysts with a simple and performant data model.

## Structure
This component is implemented as a single-responsibility script: `publish.py`.

## Behavior
The script connects to the MS SQL database using utilities from `src/utils/db.py`. It executes pre-defined SQL scripts or stored procedures that truncate the `mart.*` tables and reload them with fresh data from the historized `core.*` layer. This ensures the mart always reflects the latest state of the core data.

## Evolution
### Planned
- Initial implementation as described.

### Historical
- v1: Initial design. 