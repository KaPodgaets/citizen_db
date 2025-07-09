# Design Plan: Python & MS SQL Data Integration Pipeline (Revision 2)

## 1. Executive Summary & Goals
This document provides a detailed architectural and implementation plan for the "Citizen Data Integration Project". It incorporates user feedback to create a robust, maintainable, and scalable data pipeline using Python with SQLAlchemy and MS SQL Server.

The primary objective is to establish an end-to-end ELT (Extract-Load-Transform) process that moves data from source Excel files into an analytics-ready MS SQL data mart, ready for consumption by Power BI.

**Key Goals:**
1.  **Robustness & Auditability:** Build a pipeline where every step is logged to the database, is auditable, and is restartable, ensuring data integrity and operational transparency.
2.  **Maintainability & Scalability:** Create a modular Python codebase with clear separation of concerns, managed dependencies, and a design that can be extended to new data sources and eventually automated.
3.  **Actionable Data Delivery:** Produce a clean, historized, and well-structured star schema that empowers analysts and delivers reliable insights through Power BI.

## 2. Current Situation Analysis
The project starts with a well-conceived conceptual brief (`autogen_readme.md`). This brief establishes a solid foundation by defining:
*   A logical four-layer data architecture (Raw, Stage, Core, Mart).
*   A clear separation of pipeline steps into distinct, single-responsibility scripts.
*   A comprehensive metadata-driven approach for auditing and control.
*   A high-level testing and security strategy.

This plan solidifies the conceptual brief into a concrete, actionable implementation roadmap, addressing previous ambiguities in tooling, configuration, and operational procedures.

## 3. Proposed Solution / Refactoring Strategy
### 3.1. High-Level Design / Architectural Overview
The proposed architecture is an ELT pipeline orchestrated by Python scripts, using MS SQL Server for storage and transformation, and leveraging local file systems for raw and staged data. A central `meta` schema in the database will track every action, enabling idempotency and advanced operational control.

```mermaid
graph TD
    subgraph "On-Prem File System"
        A[Monthly XLSX Files] --> B{data/land/};
        B --> C[ingest.py];
        D[validate.py] --> E(data/stage/clean/*.parquet);
    end

    subgraph "Python ETL Application"
        C -- "Log File Info" --> F;
        C -- "File Path" --> D;
        D -- "Log Validation" --> F;
        E -- "Parquet Path" --> G[transform.py];
        G -- "Log Transform" --> F;
        G -- "Update Version" --> F;
        H[publish.py] -- "Log Publish" --> F;
        I[run_pipeline.py] -- "Orchestrates G & H" --> G & H;
    end

    subgraph "MS SQL Server"
        F[meta.* Schemas];
        G --> J[core.* Schemas (SCD-2)];
        J --> H;
        H --> K[mart.* Schemas (Star)];
    end

    subgraph "BI Layer"
        K --> L((Power BI));
    end

    F -- "Provides State" --> I;
```

### 3.2. Key Components / Modules
The project will follow the proposed folder structure with added detail for maintainability.

*   **`src/` - Core Application Logic:**
    *   `ingest.py`, `validate.py`, `transform.py`, `publish.py`, `run_pipeline.py`: Single-responsibility scripts as defined previously.
*   **`src/utils/` - Shared Utilities:**
    *   `config.py`: Manages environment-aware configuration (dev, test, prod) using `pydantic-settings` to load from `.env` files.
    *   `db.py`: Manages a **SQLAlchemy Engine** and connection pool. Provides helper functions for executing statements and performing bulk operations.
    *   `logging_config.py`: Centralized logging setup. Configures a handler for rich, readable console output and another for detailed logging to the `meta.etl_audit` table.
*   **`src/transformations/` - Business Logic for Cleansing:**
    *   **Purpose:** To isolate complex data cleansing rules from the main transformation orchestration logic.
    *   `citizen_rules.py`: Contains functions for cleansing citizen data (e.g., name parsing, address standardization).
    *   `phone_rules.py`: Contains functions for phone number validation and formatting.
*   **`schemas/` - Data Contracts:**
    *   Pandera schemas, one module per data source (e.g., `citizens_schema.py`).
*   **`sql/` - Database Definitions:**
    *   `ddl/`: Idempotent DDL scripts for `meta`, `core`, and `mart` schemas.

### 3.3. Detailed Action Plan / Phases

#### Phase 0: Project Foundation & Setup
*   **Objective(s):** Establish a stable, reproducible development environment and core utilities.
*   **Priority:** High
*   **Task 0.1:** Initialize Git Repository & Folder Structure
    *   **Rationale/Goal:** Create the baseline project structure, including the new `src/transformations` directory.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:** Git repository created with the documented folder tree and a comprehensive `.gitignore` file.
*   **Task 0.2:** Implement Dependency Management
    *   **Rationale/Goal:** Ensure reproducible builds.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:** A `pyproject.toml` file with `pandas`, `pandera`, **`sqlalchemy`**, `pyodbc`, `pydantic-settings`, `openpyxl`.
*   **Task 0.3:** Implement Configuration Management (`src/utils/config.py`)
    *   **Rationale/Goal:** Securely manage secrets and environment-specific settings.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** A `config.py` module loads settings from a `.env` file. A `.env.example` file is committed.
*   **Task 0.4:** Implement Core Utilities (`src/utils/logging_config.py`, `src/utils/db.py`)
    *   **Rationale/Goal:** Create shared, robust modules for logging and database interaction.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:**
        *   `db.py`: Initializes a singleton SQLAlchemy Engine.
        *   `logging_config.py`: Configures the root logger with a custom formatter for clear console output (e.g., `[%(asctime)s] - %(levelname)s - %(message)s`) and a custom handler to write log entries to `meta.etl_audit`.
*   **Task 0.5:** Implement SQL DDL for `meta` Schema
    *   **Rationale/Goal:** Create the foundational tables for pipeline auditing and control.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:** Idempotent DDL script in `sql/ddl/meta_schema.sql` is created and run.

---
#### Phase 1: Ingestion and Validation
*   **Objective(s):** Reliably land source files and validate them against defined data contracts.
*   **Priority:** High
*   **Task 1.1:** Develop Pandera Schemas for Source Files
    *   **Rationale/Goal:** Define data quality rules and structure for incoming data.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** Pandera schema files are created in `schemas/`.
*   **Task 1.2:** Implement `ingest.py`
    *   **Rationale/Goal:** Automate landing a new file and registering it. Idempotency is achieved by checking for an existing SHA256 hash in `meta.ingestion_log` before processing.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** Script correctly copies a file, calculates its hash, and inserts a record into `meta.ingestion_log` only if the hash is unique.
*   **Task 1.3:** Implement `validate.py`
    *   **Rationale/Goal:** Validate a landed file against its schema and produce a clean Parquet file.
    *   **Estimated Effort (Optional):** L
    *   **Deliverable/Criteria for Completion:** Script takes a `file_id`, validates data, writes a Parquet file on success, and logs the result to `meta.validation_log`.

---
#### Phase 2: Data Transformation (Core & Mart)
*   **Objective(s):** Implement the business logic to create the historized `core` layer and the analytics-ready `mart` layer.
*   **Priority:** Medium
*   **Task 2.1:** Implement SQL DDL for `core` and `mart` Schemas
    *   **Rationale/Goal:** Create the target tables for transformation.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** Idempotent DDL scripts in `sql/ddl/core_schema.sql` and `sql/ddl/mart_schema.sql` are created and run.
*   **Task 2.2:** Implement Data Cleansing Functions
    *   **Rationale/Goal:** Isolate business logic for better testing and maintenance.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** Cleansing functions are created in `src/transformations/` as pure, testable Python functions (e.g., `clean_phone_number(series) -> series`).
*   **Task 2.3:** Implement SCD-2 Logic in `transform.py`
    *   **Rationale/Goal:** Correctly identify new, changed, and unchanged records to build the historized `core` layer.
    *   **Estimated Effort (Optional):** L
    *   **Deliverable/Criteria for Completion:** The script imports and applies functions from `src/transformations`. It reads from `stage`, uses pandas to determine changes, and then uses SQLAlchemy Core to execute efficient bulk INSERT/UPDATE operations against the database.
*   **Task 2.4:** Implement Mart Population in `publish.py`
    *   **Rationale/Goal:** Create the denormalized star schema for BI consumption.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** The script uses SQLAlchemy to execute stored procedures or SQL scripts that truncate and reload the `mart` tables from `core`.
*   **Task 2.5:** Implement `run_pipeline.py` Orchestrator
    *   **Rationale/Goal:** Create a smart runner that automates the standard transform-then-publish workflow.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:** Script queries `meta` tables to find new validated files and triggers the subsequent steps.

---
#### Phase 3: Operational Hardening
*   **Objective(s):** Make the pipeline robust, easy to operate, and failure-resistant.
*   **Priority:** Medium
*   **Task 3.1:** Implement Global Error Handling and Auditing
    *   **Rationale/Goal:** Ensure failures are caught, logged centrally, and visible to operators.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** All main scripts use a decorator or context manager that wraps their main logic in a `try...except` block. All exceptions are caught and logged to both the console (via the rich logger) and the `meta.etl_audit` table with a 'FAIL' status and error details.
*   **Task 3.2:** Implement and Test Rollback Procedure
    *   **Rationale/Goal:** Provide a safe and reliable way to undo a faulty data load.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:** A `--rollback` flag is added to `transform.py` that uses the `meta.dataset_version` table to revert a specific data load.

### 3.4. Data Model Changes
The data models for the `meta` schema are confirmed as proposed previously. They are designed to support the audit and control requirements of the pipeline.

## 4. Key Considerations & Risk Mitigation
### 4.1. Technical Risks & Challenges
*   **Schema Integrity:** There is a risk that malformed data could corrupt the database.
    *   **Mitigation:** This is prevented by a multi-layered defense. **1) DDL Separation:** Database schemas are defined and managed by separate, version-controlled `.sql` scripts, not by the Python application. The ETL service account will not have DDL modification rights. **2) Pandera Validation:** The `validate.py` step acts as a gatekeeper. No data that fails schema or content validation ever reaches the transformation step or the `core` database tables.
*   **Idempotency:** Re-running a script could cause duplicate data.
    *   **Mitigation:** Each script will perform a "pre-flight check" against the `meta` tables. `ingest.py` checks the SHA256 hash. `transform.py` checks if a `dataset_version` for that input data already exists. This ensures that operations are not repeated.
*   **Performance with SQLAlchemy:** The ORM layer can sometimes be slow for bulk operations.
    *   **Mitigation:** The plan specifies using **SQLAlchemy Core** (`engine.execute()`, `connection.execute()`) for all bulk data operations, not the ORM. This provides performance near that of raw database drivers while retaining the benefits of connection management and SQL expression building.

### 4.2. Dependencies
*   **Internal:** The phases are sequential. The successful completion of `validate.py` is a strict prerequisite for `transform.py`.
*   **External:** Stable network access to MS SQL Server; consistent source file delivery; permissions for the ETL service account.

### 4.3. Non-Functional Requirements (NFRs) Addressed
*   **Maintainability:** Addressed by modular code (`src/utils`, `src/transformations`), single-responsibility scripts, and clear configuration management.
*   **Reliability & Auditability:** Addressed by the comprehensive `meta` schema and the robust logging to both the console and the database.
*   **Security:** Addressed by using `.env` files for secrets and defining limited-permission SQL roles.

## 5. Success Metrics / Validation Criteria
*   **Pipeline Reliability:** >99% of runs complete successfully.
*   **Data Quality:** Failures are caught at the `validate` step, with zero malformed data reaching the `core` schema.
*   **Performance:** End-to-end processing time for a standard 50MB file is under the 10-minute target.
*   **Operational Transparency:** An operator can determine the status of any file load by querying the `meta` tables and viewing the console logs.

## 6. Assumptions Made
*   The project has access to a dedicated service account with the necessary permissions.
*   Business logic for transformations will be clearly defined.
*   **Historical Data Loading:** Historical files will be manually placed and processed in chronological order using the pipeline to ensure correct SCD-2 historization. No special backfill script is required.
*   **Raw Data Archival:** The policy for long-term archival of raw files in `data/land/` is deferred and out of scope for this initial implementation.

## 7. Open Questions / Areas for Further Investigation
*All previously open questions have been resolved by user feedback and incorporated into this definitive plan.*