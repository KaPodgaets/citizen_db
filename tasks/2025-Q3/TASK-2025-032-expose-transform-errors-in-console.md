---
id: TASK-2025-032
title: "Phase 1: Expose Transformation Errors in the Console"
status: backlog
priority: high
type: feature
estimate: S
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-orchestration]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
To provide immediate visibility into transformation failures and speed up debugging, modify the orchestrator to print errors to the console.

## Acceptance Criteria
The `trigger_transforms` function in `src/run_pipeline.py` is modified. In the failure block (when a subprocess returns a non-zero exit code), the captured `stderr` from the process is printed to the console in addition to being logged to the database. 