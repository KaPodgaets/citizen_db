-- This script contains DDL changes for the v2 resilient pipeline.
-- It creates new logging tables and adds traceability columns to stage tables.
-- It is designed to be idempotent and can be run multiple times.

-- Create meta.stage_load_log table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'stage_load_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.stage_load_log (
        id INT IDENTITY(1,1) PRIMARY KEY,
        validation_log_id INT NOT NULL,
        status NVARCHAR(50) NOT NULL,
        load_timestamp DATETIME2 DEFAULT GETDATE(),
        error_message NVARCHAR(MAX),
        CONSTRAINT FK_stage_load_log_validation_log FOREIGN KEY (validation_log_id) REFERENCES meta.validation_log(id)
    );
END
GO

-- Create meta.transform_log table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'transform_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    CREATE TABLE meta.transform_log (
        id INT IDENTITY(1,1) PRIMARY KEY,
        dataset_name NVARCHAR(255) NOT NULL,
        period VARCHAR(7) NOT NULL,
        status NVARCHAR(50) NOT NULL, -- PENDING, PASS, FAIL
        retry_count INT DEFAULT 0,
        last_attempt_timestamp DATETIME2 DEFAULT GETDATE(),
        error_message NVARCHAR(MAX)
    );
END
GO

-- Generic procedure to add columns and index to a stage table
-- NOTE: This assumes your stage tables are named after the datasets in datasets_config.yml
DECLARE @tableName NVARCHAR(128);
DECLARE table_cursor CURSOR FOR
SELECT 'av_bait' UNION ALL
SELECT 'new_immigrants' UNION ALL
SELECT 'welfare_patients';

OPEN table_cursor;
FETCH NEXT FROM table_cursor INTO @tableName;

WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @sql NVARCHAR(MAX);

    -- Add columns if they don't exist
    SET @sql = 'IF EXISTS(SELECT * FROM sys.tables WHERE name = ''' + @tableName + ''' AND SCHEMA_ID(''stage'') = schema_id)
                BEGIN
                    IF NOT EXISTS (SELECT * FROM sys.columns WHERE Name = N''_source_parquet_path'' AND Object_ID = Object_ID(N''stage.' + @tableName + '''))
                        ALTER TABLE stage.' + @tableName + ' ADD _source_parquet_path NVARCHAR(1024);
                    IF NOT EXISTS (SELECT * FROM sys.columns WHERE Name = N''_data_period'' AND Object_ID = Object_ID(N''stage.' + @tableName + '''))
                        ALTER TABLE stage.' + @tableName + ' ADD _data_period VARCHAR(7);
                END';
    EXEC sp_executesql @sql;

    -- Add index if it doesn't exist
    SET @sql = 'IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = ''IX_' + @tableName + '_data_period'' AND object_id = OBJECT_ID(''stage.' + @tableName + '''))
                CREATE INDEX IX_' + @tableName + '_data_period ON stage.' + @tableName + '(_data_period);';
    EXEC sp_executesql @sql;

    FETCH NEXT FROM table_cursor INTO @tableName;
END

CLOSE table_cursor;
DEALLOCATE table_cursor;
GO