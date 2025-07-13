---
id: TASK-2025-036
title: "Phase 2: Modify Orchestrator to Use Dynamic Transform Scripts"
status: backlog
priority: high
type: feature
estimate: M
assignee: 
created: 2025-07-13
updated: 2025-07-13
parents: [TASK-2025-031]
children: []
arch_refs: [ARCH-pipeline-orchestration, ARCH-pipeline-step-transform]
audit_log:
  - {date: 2025-07-13, user: "@AI-DocArchitect", action: "created with status backlog"}
---
## Description
Refactor the orchestrator to use the new configuration in `datasets_config.yml` to run the correct, dataset-specific transform script.

## Acceptance Criteria
- The `trigger_transforms` function in `src/run_pipeline.py` is refactored.
- Instead of calling a hardcoded `src/transform.py`, it now loads `datasets_config.yml`.
- For each task, it looks up the `dataset_name` in the config, retrieves the path from the `transform_script` key, and executes that script via `subprocess.run`.
- The function raises a clear error if the `transform_script` key is missing for a dataset. 