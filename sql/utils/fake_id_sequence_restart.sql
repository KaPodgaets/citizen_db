/* Restart the existing sequence at a new starting value */
ALTER SEQUENCE core.seq_fake_citizen_id
    RESTART WITH 1000000;          -- choose any bigint you need
GO


/* Optional IF EXISTS (SQL 2016+) */
DROP SEQUENCE IF EXISTS core.seq_fake_citizen_id;
GO

CREATE SEQUENCE core.seq_fake_citizen_id
    AS BIGINT
    START WITH 1000000
    INCREMENT BY 1;
GO
