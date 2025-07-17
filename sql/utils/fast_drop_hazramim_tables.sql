IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'hazramim' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.hazramim;
END
GO

IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'hazramim' AND s.name = 'core')
BEGIN
    drop table core.hazramim;
END
GO
