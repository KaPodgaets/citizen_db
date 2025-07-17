---
id: TASK-2025-027
title: "Implement Staging Layer Update and Core Rebuild Logic (v2)"
status: done
priority: high
type: feature
estimate: XL
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: []
children: [TASK-2025-028, TASK-2025-029, TASK-2025-030]
arch_refs: [ARCH-pipeline-step-load-stage, ARCH-pipeline-orchestration, ARCH-database-schemas, ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-13, user: "@AI-Roboticist", action: "marked as done"}
---
## Description
This epic covers the implementation of a robust, auditable staging load process and enhances the core rebuild orchestration with a resilient, single-retry mechanism for transformations. This work addresses key requirements for data traceability and pipeline reliability.

## Acceptance Criteria
- A new `load_stage.py` script transactionally loads validated Parquet files into the stage database, logging its actions.
- The database schema is augmented with new log tables (`meta.stage_load_log`, `meta.transform_log`) and traceability columns in `stage` tables.
- The `run_pipeline.py` orchestrator is enhanced to use the new log tables to manage the pipeline flow and automatically retry a failed transformation step once. 