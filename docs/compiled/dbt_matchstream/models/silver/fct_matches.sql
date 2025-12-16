

WITH max_loaded AS (

    
        SELECT MAX(cdc_ts_ms) AS max_cdc_ts
        FROM silver.fct_matches
    

),

normalized AS (

    SELECT
        event_id,
        LEAST(user1, user2)    AS user1,
        GREATEST(user1, user2) AS user2,
        created_at,
        ingested_at AS ingested_at_bronze,
        cdc_ts_ms,

        ROW_NUMBER() OVER (
            PARTITION BY
                LEAST(user1, user2),
                GREATEST(user1, user2)
            ORDER BY cdc_ts_ms DESC
        ) AS rn

    FROM bronze.matches_cdc
    CROSS JOIN max_loaded

    WHERE op != 'd'
      AND cdc_ts_ms > max_loaded.max_cdc_ts
)

SELECT
    user1,
    user2,
    created_at,
    ingested_at_bronze,
    cdc_ts_ms

FROM normalized
WHERE rn = 1