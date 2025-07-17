---
id: TASK-2025-008
title: "Task 0.4: Implement Core Utilities (logging, db)"
status: done
priority: high
type: feature
estimate: M
assignee: 
created: 2025-07-09
updated: 2025-07-09
parents: [TASK-2025-001]
children: []
arch_refs: [ARCH-pipeline-utilities]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (db.py and logging file exist)"}
---
## Description
Create shared, robust modules for centralized logging and database interaction to be used by all pipeline scripts.

## Acceptance Criteria
- `src/utils/db.py` is created and initializes a singleton SQLAlchemy Engine.
- `src/utils/logging_config.py` is created. It configures the root logger with a console handler for clear output and a custom database handler to write log entries to the `meta.etl_audit` table. 