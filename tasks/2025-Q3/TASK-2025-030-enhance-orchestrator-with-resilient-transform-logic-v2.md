---
id: TASK-2025-030
title: "Task 2.1: Enhance Orchestrator with Resilient Transform Logic (v2)"
status: done
priority: high
type: feature
estimate: L
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-027]
children: []
arch_refs: [ARCH-pipeline-orchestration, ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-13, user: "@AI-Roboticist", action: "marked as done"}
---
## Description
Refactor the `run_pipeline.py` script to create a fully automated and resilient flow from validation to core layer population. This includes integrating the new staging step and implementing a "rebuild core" logic with a single-retry mechanism for the transformation step.

## Acceptance Criteria
- The orchestrator triggers `load_stage.py` for newly validated files found in `meta.validation_log`.
- The orchestrator identifies new work for transformation by querying `meta.stage_load_log` and creates 'PENDING' records in `meta.transform_log`.
- The orchestrator processes 'PENDING' records by triggering `transform.py`.
- On failure, the orchestrator updates the `meta.transform_log` record to 'FAIL' and increments `retry_count`.
- The orchestrator re-triggers `transform.py` for records with `status` = 'FAIL' and `retry_count` < 1.
- A transform that fails twice is not triggered a third time. 