---
id: TASK-2025-017
title: "Task 2.5: Implement run_pipeline.py Orchestrator"
status: backlog
priority: medium
type: feature
estimate: S
assignee: 
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-003]
children: []
arch_refs: [ARCH-pipeline-orchestration]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing orchestrator logic in run_pipeline.py"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
---
## Description
Create a smart runner script that automates the standard transform-then-publish workflow based on the pipeline's current state.

## Acceptance Criteria
The `run_pipeline.py` script correctly queries the `meta.ingestion_log` and `meta.validation_log` tables to find files ready for the next step (validation, transformation) and automatically triggers the appropriate script for them. 