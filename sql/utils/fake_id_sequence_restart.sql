/* Restart the existing sequence at a new starting value */
ALTER SEQUENCE core.seq_fake_citizen_id
    RESTART WITH 1;          -- choose any bigint you need
GO


/* Optional IF EXISTS (SQL 2016+) */
DROP SEQUENCE IF EXISTS core.seq_fake_citizen_id;
GO

CREATE SEQUENCE core.seq_fake_citizen_id
    AS INT
    START WITH 1
    INCREMENT BY 1;
GO


