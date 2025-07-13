
IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'citizens' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.citizens;
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

