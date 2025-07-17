IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'hamal' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.hamal;
END
GO

IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'hamal' AND s.name = 'core')
BEGIN
    drop table core.hamal;
END
GO
