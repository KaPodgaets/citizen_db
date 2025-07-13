IF EXISTS (SELECT * FROM sys.tables t 
           INNER JOIN sys.schemas s ON t.schema_id = s.schema_id 
           WHERE t.name = 'av_bait' AND s.name = 'stage')
BEGIN
    DROP TABLE stage.av_bait;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'core.av_bait')
BEGIN
    drop table core.av_bait;
END
GO

IF EXISTS (SELECT * FROM sys.tables WHERE name = 'mart.av_bait_fact')
BEGIN
    drop table mart.av_bait;
END
GO

