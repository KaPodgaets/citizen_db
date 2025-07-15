IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'new_immigrants' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.new_immigrants;
END
GO

IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'new_immigrants' AND s.name = 'core')
BEGIN
    drop table core.new_immigrants;
END
GO
