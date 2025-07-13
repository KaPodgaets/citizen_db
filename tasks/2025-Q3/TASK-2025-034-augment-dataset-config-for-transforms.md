---
id: TASK-2025-034
title: "Phase 2: Augment Dataset Configuration for Transform Scripts"
status: backlog
priority: high
type: feature
estimate: S
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Extend the central `datasets_config.yml` file to define the specific transformation script for each dataset, enabling a configuration-driven approach.

## Acceptance Criteria
The `datasets_config.yml` file is updated. Each dataset entry receives a new key, `transform_script`, with a value pointing to its corresponding script location (e.g., 'src/transformations/scripts/transform_av_bait.py'). 