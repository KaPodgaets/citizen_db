IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'phone_numbers' AND s.name = 'core')
BEGIN
    drop table core.phone_numbers;
END
GO
