IF EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_audit' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table  meta.etl_audit;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'stage_load_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.stage_load_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'validation_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.validation_log;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ingestion_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table  meta.ingestion_log;
END
GO


IF EXISTS (SELECT * FROM sys.tables WHERE name = 'dataset_version' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.dataset_version;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'transform_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    drop table meta.transform_log;
END
GO