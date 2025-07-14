/* -------------------------------------------
CLEANING META TABLES
------------------------------------------- */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_audit' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.etl_audit;
END
GO


IF EXISTS (SELECT * FROM sys.tables WHERE name = 'stage_load_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.stage_load_log;
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

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'transform_log' AND schema_id = SCHEMA_ID('meta'))
BEGIN
    delete from meta.transform_log;
END
GO
/* -------------------------------------------
CLEANING data TABLES
------------------------------------------- */
/* av_bait */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'av_bait' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    delete from stage.av_bait;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'av_bait' AND schema_id = SCHEMA_ID('core'))
BEGIN
    delete from core.av_bait;
END
GO
/* welfare_patients */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'welfare_patients' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    delete from stage.welfare_patients;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'welfare_patients' AND schema_id = SCHEMA_ID('core'))
BEGIN
    delete from core.welfare_patients;
END
GO

/* meser */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'meser' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    delete from stage.meser;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'meser' AND schema_id = SCHEMA_ID('core'))
BEGIN
    delete from core.meser;
END
GO

/* hazramim */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'hazramim' AND schema_id = SCHEMA_ID('stage'))
BEGIN
    delete from stage.hazramim;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'hazramim' AND schema_id = SCHEMA_ID('core'))
BEGIN
    delete from core.hazramim;
END
GO

/* phone_numbers */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'phone_numbers' AND schema_id = SCHEMA_ID('core'))
BEGIN
    delete from core.phone_numbers;
END
GO
/* -------------------------------------------
CLEANING MART LAYER
------------------------------------------- */
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'citizens' AND schema_id = SCHEMA_ID('mart'))
BEGIN
    delete from mart.citizens;
END
GO