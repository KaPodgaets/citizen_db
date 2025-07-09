---
id: TASK-2025-012
title: "Task 1.3: Implement Validate Script"
status: refactoring
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-validate]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (validate.py implemented)"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
---
## Description
Implement the `validate.py` script to perform the second layer of data quality checks. It reads data from the `raw` database schema, validates it against a Pandera schema, and loads the clean, correctly-typed data into the `stage` schema.

## Acceptance Criteria
The script takes a `file_id` as input, reads the data from the corresponding `raw` table, validates it against its Pandera schema, and on success, bulk-loads the clean DataFrame into the corresponding `stage` table. The result (pass or fail with errors) is logged to `meta.validation_log`. 