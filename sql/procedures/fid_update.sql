/* -----------------------------------------------------------
   Up-sert new fake IDs for citizens that are current in core.av_bait
   • Inserts only those citizen_id values that don’t already exist
     in core.fake_citizen_id.
   • NEXT VALUE FOR retrieves the next surrogate from the sequence.
   • Uses an explicit transaction so you can roll back from Python
     if something goes wrong.
-----------------------------------------------------------*/

BEGIN TRANSACTION;                     -- ① start atomic section
SET NOCOUNT ON;                        -- ② suppress “rows affected”

INSERT INTO core.fake_citizen_id (citizen_id, fake_citizen_id)
SELECT  c.citizen_id,
        NEXT VALUE FOR core.seq_fake_citizen_id      -- ③ generate surrogate
FROM    core.av_bait     AS c
WHERE   c.is_current = 1                             -- ④ take only current rows
AND     NOT EXISTS (                                 -- ⑤ skip already-mapped IDs
        SELECT 1
        FROM   core.fake_citizen_id AS f
        WHERE  f.citizen_id = c.citizen_id
);

/* Optional: capture number of inserts for logging */
-- SELECT @@ROWCOUNT AS rows_inserted;

COMMIT TRANSACTION;                    -- ⑥ make it permanent
