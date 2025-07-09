---
id: TASK-2025-019
title: "Task 3.2: Implement and Test Rollback Procedure"
status: done
priority: medium
type: feature
estimate: M
assignee: 
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-004]
children: []
arch_refs: [ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-Assistant", action: "marked done after implementing rollback procedure in transform.py"}
---
## Description
Provide a safe and reliable way to undo a faulty data load, reverting the database to its state before the load.

## Acceptance Criteria
A `--rollback` flag is added to `transform.py`. When used with a specific version identifier, it uses the metadata in the `meta.dataset_version` table to revert the corresponding data load from the `core` tables. 