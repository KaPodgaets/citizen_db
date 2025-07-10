---
id: TASK-2025-017
title: "Task 2.5: Implement run_pipeline.py Orchestrator"
status: done
priority: medium
type: feature
estimate: S
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: [TASK-2025-003]
children: []
arch_refs: [ARCH-pipeline-orchestration]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing orchestrator logic in run_pipeline.py"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
  - {date: 2025-07-10, user: "@AI-DocArchitect", action: "status: backlog -> done. Updated to reflect new pipeline steps."}
---
## Description
Create a smart runner script that automates the multi-step pipeline based on the current state recorded in the metadata tables.

## Acceptance Criteria
The run_pipeline.py script correctly queries the metadata tables to find files ready for the next step (validation, load-to-stage, transformation) and automatically triggers the appropriate script (validate.py, load_stage.py, transform.py) for them. 