---
id: TASK-2025-011
title: "Task 1.2: Implement Ingest Script"
status: done
priority: high
type: feature
estimate: M
assignee:
created: 2025-07-09
updated: 2025-07-10
parents: [TASK-2025-002]
children: []
arch_refs: [ARCH-pipeline-step-ingest, ARCH-data-contract-yaml]
audit_log:
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "marked as done (ingest.py implemented)"}
  - {date: 2025-07-09, user: "@AI-DocArchitect", action: "description updated to reflect refactoring to DB-centric flow"}
  - {date: 2025-07-10, user: "@AI-DocArchitect", action: "status: refactoring -> done. Updated to reflect new in-place validation logic."}
---
## Description
Implement the ingest.py script to be the primary quality gate for source files. The script validates files in-place within the data/landed/ directory, ensuring they conform to project standards before being registered for further processing. It does not load data into the database.

## Acceptance Criteria
The script takes a --file-path to a file in data/landed/. It validates the filename structure and content against datasets_config.yml. It validates that all required headers (from the relevant YAML contract) are present in the source file. It performs a hash-based idempotency check. It does NOT move or copy the file. On success, it logs the file's metadata (name, hash, dataset, period, version) to meta.ingestion_log and exits. 