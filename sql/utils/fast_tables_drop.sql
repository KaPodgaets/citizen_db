IF EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_audit' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table  meta.etl_audit;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ingestion_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table  meta.ingestion_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'validation_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.validation_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'dataset_version' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.dataset_version;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'core.citizens')
BEGIN
    drop table core.citizens;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'mart.citizens_fact')
BEGIN
    drop table mart.citizens_fact;
END
GO

