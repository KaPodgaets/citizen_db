---
id: TASK-2025-035
title: "Phase 2: Create Directory and Template for Modular Transform Scripts"
status: done
priority: high
type: feature
estimate: M
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
  - {date: 2025-07-13, user: "@AI-Roboticist", action: "marked as done"}
---
## Description
Establish the new structure for modular transform scripts by creating a dedicated directory and providing a starting template for each dataset.

## Acceptance Criteria
- A new directory, `src/transformations/scripts/`, is created.
- The existing `src/transform.py` is copied into this new directory for each dataset defined in `datasets_config.yml` (e.g., `transform_av_bait.py`, `transform_new_immigrants.py`).
- The original `src/transform.py` is marked as deprecated in its docstring. 