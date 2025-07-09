IF EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_audit' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.etl_audit;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ingestion_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.ingestion_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'validation_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.validation_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'dataset_version' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.dataset_version;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'citizen_core')
BEGIN
    delete from meta.citizen_core;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'citizen_mart_fact')
BEGIN
    delete from meta.citizen_mart_fact;
END
GO

