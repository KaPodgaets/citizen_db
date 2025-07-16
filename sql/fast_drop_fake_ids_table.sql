IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'fake_citizen_ids' AND s.name = 'core')
BEGIN
    DROP TABLE core.fake_citizen_ids;
END
GO