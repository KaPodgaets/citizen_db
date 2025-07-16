-- Idempotent DDL for stage schema (MS SQL)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'core')
    EXEC('CREATE SCHEMA core');
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'fake_citizen_ids' AND schema_id = SCHEMA_ID('core'))
BEGIN
    CREATE TABLE core.fake_citizen_ids
    (
        citizen_id       INT          NOT NULL,           -- real key
        fake_citizen_id  INT       NOT NULL,           -- surrogate
        created_at       DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
        CONSTRAINT PK_fake_citizen_id    PRIMARY KEY (citizen_id),
        CONSTRAINT UQ_fake_citizen_id    UNIQUE (fake_citizen_id)   -- avoids duplicates
    );
END
GO

/*------------------------------------------------------------
Create the surrogate-ID sequence  (once)
------------------------------------------------------------*/
IF NOT EXISTS (
        SELECT 1
        FROM   sys.sequences
        WHERE  name      = 'seq_fake_citizen_id'
        AND    SCHEMA_ID = SCHEMA_ID('core')
)
BEGIN
    CREATE SEQUENCE core.seq_fake_citizen_id
        AS INT
        START WITH 1
        INCREMENT BY 1;
END
GO
