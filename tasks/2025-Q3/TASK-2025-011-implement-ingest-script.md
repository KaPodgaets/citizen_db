---
id: TASK-2025-011
title: "Task 1.2: Implement ingest.py"
status: done
priority: high
type: feature
estimate: M
assignee: 
created: 2025-07-09
updated: 2025-09-07
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-ingest]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (ingest.py implemented)"}
---
## Description
Implement the `ingest.py` script to automate the landing and registration of a new source file. The process must be idempotent to prevent duplicate processing.

## Acceptance Criteria
The script correctly copies a source file to `data/land/`, calculates its SHA256 hash, and inserts a record into `meta.ingestion_log` only if the hash is unique in that table. 