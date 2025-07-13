IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'welfare_patients' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.welfare_patients;
END
GO

IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'welfare_patients' AND s.name = 'core')
BEGIN
    drop table core.welfare_patients;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'mart.welfare_patients')
BEGIN
    drop table mart.welfare_patients;
END
GO

