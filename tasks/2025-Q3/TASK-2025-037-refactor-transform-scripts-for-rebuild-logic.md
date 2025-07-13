---
id: TASK-2025-037
title: "Phase 3: Refactor Transform Scripts with Metadata-Driven Rebuild Logic"
status: backlog
priority: medium
type: feature
estimate: L
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-step-transform, ARCH-data-model-core]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Implement the new, simpler core data loading strategy within each dataset-specific transform script, using the `meta.dataset_version` table for state management.

## Acceptance Criteria
- Each script in `src/transformations/scripts/` is refactored.
- The main logic is replaced with a single transaction that:
  1. Finds any previous `dataset_version_ids` for the same dataset and period.
  2. Creates a new record in `meta.dataset_version`, getting back the new `dataset_version_id`.
  3. If previous versions were found, it deletes the old data from the `core` table based on the old IDs.
  4. Reads data from the `stage` table, adds the new `dataset_version_id`, and bulk inserts it into the `core` table. 