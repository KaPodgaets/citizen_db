IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'citizen' AND s.name = 'mart')
BEGIN
    DROP TABLE mart.citizen;
END
GO


IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'citizens' AND s.name = 'mart')
BEGIN
    DROP TABLE mart.citizens;
END
GO