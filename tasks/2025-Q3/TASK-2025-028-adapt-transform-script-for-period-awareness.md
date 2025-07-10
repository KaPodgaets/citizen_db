---
id: TASK-2025-028
title: "Adapt transform.py for Period-Aware Processing"
status: backlog
priority: medium
type: feature
estimate: S
assignee:
created: 2025-07-10
updated: 2025-07-10
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-step-transform]
audit_log:

{date: 2025-07-10, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Adapt the transform.py script to ensure it processes only the intended dataset from the stage layer for a specific period.

## Acceptance Criteria
- transform.py is modified to accept a --period argument.
- Its SQL SELECT query from the stage table(s) will include a WHERE _data_period = :period clause to correctly filter the source data. 