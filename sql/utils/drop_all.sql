-- Run in the target database
SET NOCOUNT ON;

DECLARE @sql NVARCHAR(MAX);

-------------------------------------------------------------------------------
-- 0) Safety: make sure we're not touching system schemas
-------------------------------------------------------------------------------
-- We'll always exclude: sys, INFORMATION_SCHEMA, guest, dbo (for schemas step)

-------------------------------------------------------------------------------
-- 1) Drop all VIEWS first (they may depend on tables)
-------------------------------------------------------------------------------
SET @sql = N'';
SELECT @sql = @sql + N'DROP VIEW ' + QUOTENAME(s.name) + N'.' + QUOTENAME(v.name) + N';' + CHAR(13)
FROM sys.views AS v
JOIN sys.schemas AS s ON s.schema_id = v.schema_id
WHERE s.name NOT IN (N'sys', N'INFORMATION_SCHEMA');

IF LEN(@sql) > 0 EXEC sys.sp_executesql @sql;

-------------------------------------------------------------------------------
-- 2) DROP all FOREIGN KEYS (so tables can be dropped regardless of dependencies)
-------------------------------------------------------------------------------
SET @sql = N'';
SELECT @sql = @sql + N'ALTER TABLE ' + QUOTENAME(s.name) + N'.' + QUOTENAME(t.name)
             + N' DROP CONSTRAINT ' + QUOTENAME(fk.name) + N';' + CHAR(13)
FROM sys.foreign_keys AS fk
JOIN sys.tables       AS t  ON t.object_id  = fk.parent_object_id
JOIN sys.schemas      AS s  ON s.schema_id  = t.schema_id
WHERE s.name NOT IN (N'sys', N'INFORMATION_SCHEMA');

IF LEN(@sql) > 0 EXEC sys.sp_executesql @sql;

-------------------------------------------------------------------------------
-- 3) Drop all TABLES
-- (PK/UK/CK/DF constraints are dropped implicitly with the table)
-- NOTE: If you have system-versioned temporal tables, disable system_versioning first.
-------------------------------------------------------------------------------
SET @sql = N'';
SELECT @sql = @sql + N'DROP TABLE ' + QUOTENAME(s.name) + N'.' + QUOTENAME(t.name) + N';' + CHAR(13)
FROM sys.tables AS t
JOIN sys.schemas AS s ON s.schema_id = t.schema_id
WHERE s.name NOT IN (N'sys', N'INFORMATION_SCHEMA');

IF LEN(@sql) > 0 EXEC sys.sp_executesql @sql;

-------------------------------------------------------------------------------
-- 4) Drop all SEQUENCES
-------------------------------------------------------------------------------
SET @sql = N'';
SELECT @sql = @sql + N'DROP SEQUENCE ' + QUOTENAME(s.name) + N'.' + QUOTENAME(seq.name) + N';' + CHAR(13)
FROM sys.sequences AS seq
JOIN sys.schemas   AS s   ON s.schema_id = seq.schema_id
WHERE s.name NOT IN (N'sys', N'INFORMATION_SCHEMA');

IF LEN(@sql) > 0 EXEC sys.sp_executesql @sql;

-------------------------------------------------------------------------------
-- 5) Drop all user SCHEMAS (except dbo and system ones)
-------------------------------------------------------------------------------
SET @sql = N'';
SELECT @sql = @sql + N'DROP SCHEMA ' + QUOTENAME(s.name) + N';' + CHAR(13)
FROM sys.schemas AS s
WHERE s.name NOT IN (N'dbo', N'guest', N'sys', N'INFORMATION_SCHEMA');

IF LEN(@sql) > 0 EXEC sys.sp_executesql @sql;
