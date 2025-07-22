IF EXISTS (
    SELECT 1
    FROM sys.views v
    INNER JOIN sys.schemas s ON v.schema_id = s.schema_id
    WHERE v.name = 'vw_citizens_anon' AND s.name = 'mart'
)
DROP VIEW mart.vw_citizens_anon;
