# Refactoring/Design Plan: Implement Validated File-Based Staging with Period-Aware Loading

## 1. Executive Summary & Goals
This plan outlines a comprehensive refactoring of the data ingestion and staging pipeline. It incorporates robust upfront validation and implements a sophisticated, multi-tier staging architecture. A key refinement is the implementation of a period-aware loading strategy for the database `stage` layer, ensuring data for a given period is atomically replaced, while new periods are appended.

**Key Goals:**
1.  **Implement Strict Ingestion Gating:** Refactor `ingest.py` to perform strict filename and header validation on source files located in `data/landed/` *without* creating copies.
2.  **Establish a Parquet Staging Layer:** The `validate.py` script will consume raw files and produce cleaned, typed, and validated Parquet files in `data/stage/cleaned/`.
3.  **Implement Intelligent Database Staging:** A `load_stage.py` script will load the Parquet files into the `stage` database. This script will intelligently **replace** data for an existing period and **append** data for a new period within a single transaction.
4.  **Ensure Full Test Coverage:** Develop unit and integration tests for all new and modified components, with specific tests for the new loading logic.

## 2. Current Situation Analysis
The pipeline architecture is being formalized to create a clear, multi-step process prior to the core transformations. The user has specified a critical piece of business logic for loading the `stage` database tables: the process must be idempotent at the period level. This plan provides the definitive architecture to implement this requirement, removing the `raw` database schema and formalizing the use of both Parquet files and a `stage` database schema as distinct, purposeful layers.

## 3. Proposed Solution / Refactoring Strategy
### 3.1. High-Level Design / Architectural Overview
The proposed architecture establishes a clear, stateful, and auditable pipeline flow. The key innovation is the transactional "delete-then-append" logic in the `load_stage.py` script, which is enabled by adding a period tracking column to all `stage` tables.

**The New Pipeline Flow:**
1.  **Ingest (`ingest.py`):** Validates the name and headers of a source file in `data/landed/`. On success, logs metadata (including the parsed `period`) to `meta.ingestion_log`.
2.  **Validate (`validate.py`):** Consumes a source file from `data/landed/`, cleans and validates it, and produces a Parquet file in `data/stage/cleaned/`. Logs the outcome to `meta.validation_log`.
3.  **Load Stage DB (`load_stage.py`):** The orchestrator triggers this script for a validated file. It reads the Parquet file, and within a single database transaction, it **deletes** any existing data for that file's specific period from the target `stage` table and then **appends** the new data.
4.  **Transform & Publish (`transform.py` & `publish.py`):** These scripts consume data from the `stage` database layer to populate the `core` and `mart` layers, respectively. The orchestrator will instruct them which period to process.

```mermaid
graph TD
    subgraph "File System"
        A[data/landed/*.xlsx]
        B[data/stage/cleaned/*.parquet]
    end

    subgraph "Database"
        C[meta.* logs]
        D[stage.* tables<br>(with _data_period column)]
        E[core.* tables]
        F[mart.* tables]
    end

    subgraph "Application Scripts"
        G[ingest.py]
        H[validate.py]
        I[load_stage.py <br> (Transactional Upsert)]
        J[transform.py]
    end

    A -- "Reads from" --> G;
    G -- "Writes metadata to" --> C;
    A -- "Reads from" --> H;
    H -- "Writes to" --> B;
    H -- "Writes metadata to" --> C;
    B -- "Reads from" --> I;
    I -- "Deletes+Inserts in Tx to" --> D;
    D -- "Reads from" --> J;
    J -- "Writes data to" --> E;
```

### 3.2. Key Components / Modules
-   **`datasets_config.yml` (New File):** Defines dataset rules.
-   **`src/ingest.py` (Modified):** Validator and metadata logger.
-   **`src/validate.py` (Modified):** Creates validated Parquet files.
-   **`src/load_stage.py` (New Script):** Implements the transactional, period-aware loading logic.
-   **`src/transform.py` (Modified):** Adapted to process data for a specific period from the `stage` tables.
-   **Database Schemas (Modified):** `raw` schema removed. All `stage` tables get a new `_data_period` column.

### 3.3. Detailed Action Plan / Phases

---

#### **Phase 1: Foundation: Configuration, Utilities, and DB Schema**
-   **Objective(s):** Establish the core configuration, utility functions, and the updated database schema with period tracking.
-   **Priority:** High

-   **Task 1.1: Create `datasets_config.yml` & Core Utilities**
    -   **Rationale/Goal:** Centralize rules and create reusable validation functions.
    -   **Estimated Effort:** M
    -   **Deliverable/Criteria for Completion:** `datasets_config.yml` is created. `parse_and_validate_filename` and `validate_headers` functions are implemented in `src/utils/parsing.py`.

-   **Task 1.2: Update Database Schema with Period Tracking**
    -   **Rationale/Goal:** To modify the database to support the new period-aware loading logic.
    -   **Estimated Effort:** M
    -   **Deliverable/Criteria for Completion:** An SQL migration script is created that:
        1.  Adds the required metadata columns to `meta.ingestion_log` and `meta.validation_log`.
        2.  **Adds a `_data_period` `VARCHAR(7)` column to *every* table in the `stage` schema.**
        3.  **Adds an index on the `_data_period` column for each `stage` table to ensure efficient deletes.**
        4.  Drops the `raw` schema and all its tables.

---

#### **Phase 2: Script Implementation and Refactoring**
-   **Objective(s):** Implement the logic for each step of the new pipeline, focusing on the new loading strategy.
-   **Priority:** High (Depends on Phase 1)

-   **Task 2.1: Refactor `ingest.py` and `validate.py`**
    -   **Rationale/Goal:** To align the first two steps of the pipeline with the new design.
    -   **Estimated Effort:** M
    -   **Deliverable/Criteria for Completion:** `ingest.py` performs in-place validation. `validate.py` creates Parquet files. Both scripts function as described in the high-level design.

-   **Task 2.2: Create `load_stage.py` with Transactional Logic**
    -   **Rationale/Goal:** To implement the core requirement of period-based replacement.
    -   **Estimated Effort:** L
    -   **Deliverable/Criteria for Completion:** A new `src/load_stage.py` script is created. It:
        1.  Accepts `--parquet-path`, `--period`, and `--dataset` as arguments.
        2.  Reads the Parquet file.
        3.  Adds a `_data_period` column to the DataFrame with the value from the `--period` argument.
        4.  Determines the target table name (e.g., `stage.citizens`) from the `--dataset` argument.
        5.  Opens a database transaction.
        6.  Executes `DELETE FROM stage.<table> WHERE _data_period = :period;`.
        7.  Appends the DataFrame to the table using `df.to_sql(..., if_exists='append', index=False)`.
        8.  Commits the transaction. Errors cause a rollback.

-   **Task 2.3: Adapt `transform.py`**
    -   **Rationale/Goal:** To ensure the transform step processes only the intended dataset from the `stage` layer.
    -   **Estimated Effort:** S
    -   **Deliverable/Criteria for Completion:** `transform.py` is modified to accept a `--period` argument. Its SQL `SELECT` query from the stage table will now include a `WHERE _data_period = :period` clause.

---

#### **Phase 3: Testing and Documentation**
-   **Objective(s):** Ensure the new pipeline is robust, especially the transactional loading logic.
-   **Priority:** High

-   **Task 3.1: Implement Comprehensive Tests**
    -   **Rationale/Goal:** To validate all new and modified functionality.
    -   **Estimated Effort:** L
    -   **Deliverable/Criteria for Completion:**
        1.  Unit tests for utilities.
        2.  Integration tests for `ingest.py` and `validate.py`.
        3.  **Specific integration tests for `load_stage.py` that:**
            -   Verify a first-time load for a period works correctly.
            -   Verify that re-loading for the same period correctly replaces the old data without affecting other periods.
            -   Verify that a failed load correctly rolls back the transaction, leaving the old data intact.

### 3.4. Data Model Changes
-   **Schema `raw`:**
    -   **Action:** REMOVE.
-   **Schema `stage`:**
    -   **Action:** MODIFY. Every table within this schema must be altered.
    -   **Example (`stage.citizens`):**
        | Column Name      | Type         | Attributes |
        |------------------|--------------|------------|
        | `citizen_id`     | INT          |            |
        | `first_name`     | VARCHAR      |            |
        | ... (other data columns) ... |              |
        | **`_data_period`** | **VARCHAR(7)** | **NOT NULL, INDEXED** |

### 3.5. API Design / Interface Changes
-   **`ingest.py`:** `python src/ingest.py --file-path <path_in_landed>`
-   **`validate.py`:** `python src/validate.py --file-id <id>`
-   **`load_stage.py`:** `python src/load_stage.py --parquet-path <path> --period YYYY-MM --dataset <name>`
-   **`transform.py`:** `python src/transform.py --period YYYY-MM --dataset <name>`

## 4. Key Considerations & Risk Mitigation
### 4.1. Technical Risks & Challenges
-   **Risk:** Performance of the `DELETE` operation on large `stage` tables.
    -   **Mitigation:** This is critically mitigated by **adding a database index** on the `_data_period` column in every `stage` table. This is a mandatory part of the plan (Task 1.2).
-   **Risk:** A failure between the `DELETE` and `INSERT` could lead to data loss if not handled correctly.
    -   **Mitigation:** The entire delete-and-append operation **must** be wrapped in a single database transaction. The `load_stage.py` script will use a `try...except...finally` block with `connection.begin()` context manager to ensure that any failure results in a `rollback`, preserving the original state.

### 4.2. Dependencies
-   The orchestrator must be updated to pass the new `--period` and `--dataset` arguments to `load_stage.py` and `transform.py`. This information can be retrieved from the `meta.ingestion_log` record.

### 4.3. Non-Functional Requirements (NFRs) Addressed
-   **Idempotency:** The new loading logic makes the `stage` layer idempotent at the period level, which is a significant improvement in reliability and re-runnability.
-   **Data Integrity:** The use of transactions guarantees atomicity for the replace/append operation, preventing partially loaded or corrupted states in the `stage` tables.

## 5. Success Metrics / Validation Criteria
-   All previous metrics hold true.
-   **Additional Metric:** Executing `load_stage.py` for a period '2025-06' successfully loads the data. Executing it again for '2025-06' with different data results in only the new data being present for that period, while data for '2025-05' remains untouched.
-   A failed run of `load_stage.py` (e.g., due to a data type mismatch on insert) leaves the data in the target `stage` table in its pre-run state.

## 6. Assumptions Made
-   All tables in the `stage` schema are targetable by a dataset name and can be modified to include the `_data_period` column.
-   The orchestrator can be adapted to manage the new script arguments and execution flow.