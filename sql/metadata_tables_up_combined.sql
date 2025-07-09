/*----------------------------------------------------------
meta schema (keeps operational tables separate from business data)
----------------------------------------------------------*/
IF SCHEMA_ID('meta') IS NULL
    EXEC('CREATE SCHEMA meta');
GO

/*----------------------------------------------------------
1) meta.ingestion_log
   – One row per physical file that entered the pipeline
----------------------------------------------------------*/
CREATE TABLE meta.ingestion_log
(
    file_id        INT            IDENTITY(1,1) PRIMARY KEY,
    file_name      NVARCHAR(260)  NOT NULL,             -- original name
    sha256_hash    CHAR(64)       NOT NULL,
    file_size_mb   DECIMAL(18,2)  NOT NULL,
    rows_loaded    INT            NULL,                 -- filled after load
    load_ts        DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
    loaded_by      NVARCHAR(128)  NOT NULL              -- login() or AD user
);
/* Prevent duplicate loads of the *same* file */
CREATE UNIQUE INDEX IX_ingestion_sha256
    ON meta.ingestion_log(sha256_hash);

/*-----------------------------------------------------------
2) meta.validation_log
   – Data-quality results tied back to the file
-----------------------------------------------------------*/
CREATE TABLE meta.validation_log
(
    validation_id  INT           IDENTITY(1,1) PRIMARY KEY,
    file_id        INT           NOT NULL
                 REFERENCES meta.ingestion_log(file_id),
    status         VARCHAR(10)   NOT NULL           -- PASS / FAIL
                 CHECK (status IN ('PASS','FAIL')),
    issues_json    NVARCHAR(MAX) NULL,              -- row/column errors
    validated_at   DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);
CREATE INDEX IX_validation_file
    ON meta.validation_log(file_id);

/* -----------------------------------------------------------
3) meta.dataset_version
   – Logical snapshots of the *transformed* dataset
----------------------------------------------------------- */
CREATE TABLE meta.dataset_version
(
    dataset        VARCHAR(64)   NOT NULL,          -- e.g. 'citizens'
    version_id     CHAR(7)       NOT NULL,          -- 'YYYY-MM'
    is_current     BIT           NOT NULL,
    applied_at     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
    applied_by     NVARCHAR(128) NOT NULL,
    CONSTRAINT PK_dataset_version
        PRIMARY KEY (dataset, version_id)
);
/* Fast lookup of the active version */
CREATE UNIQUE INDEX IX_version_current
    ON meta.dataset_version(dataset)
    WHERE is_current = 1;

/* -----------------------------------------------------------
4) meta.etl_audit
   – Execution heartbeat for every CLI / step
----------------------------------------------------------- */
CREATE TABLE meta.etl_audit
(
    run_id         BIGINT        IDENTITY(1,1) PRIMARY KEY,
    step_name      VARCHAR(32)   NOT NULL,          -- ingest / validate / transform
    status         VARCHAR(10)   NOT NULL
                 CHECK (status IN ('START','OK','FAIL')),
    duration_ms    INT           NULL,              -- filled on END
    note           NVARCHAR(4000) NULL,             -- error msg or free-text
    started_at     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
    ended_at       DATETIME2     NULL,              -- set when run finishes
    file_id        INT NULL
                 REFERENCES meta.ingestion_log(file_id)
);
CREATE INDEX IX_audit_step_time
    ON meta.etl_audit(step_name, started_at DESC);
GO
