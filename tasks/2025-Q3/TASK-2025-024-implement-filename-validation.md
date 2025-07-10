---
id: TASK-2025-024
title: "Task 1.4: Implement Source Filename Convention Validation"
status: backlog
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-ingest]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-07, user: "@AI-DocArchitect", action: "status: backlog -> done"}
---
## Description
Implement a strict validation check on the filenames of incoming source files to ensure they conform to the project's naming convention. This acts as a first, simple quality gate.

## Acceptance Criteria
The `ingest.py` script validates incoming filenames against a regular expression that enforces format, case, dataset prefix, date (`YYYY-MM`), and version (`v-XX`). Files with invalid names are rejected with a clear error message. 