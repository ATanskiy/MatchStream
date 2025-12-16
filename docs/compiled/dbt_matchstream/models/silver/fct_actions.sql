

WITH max_loaded AS (

    
        SELECT MAX(cdc_ts_ms) AS max_cdc_ts
        FROM silver.fct_actions
    

),

ranked AS (

    SELECT
        event_id,
        user_id,
        target_id,
        action,
        created_at,
        ingested_at AS ingested_at_bronze,
        cdc_ts_ms,

        ROW_NUMBER() OVER (
            PARTITION BY user_id, target_id
            ORDER BY cdc_ts_ms DESC
        ) AS rn

    FROM bronze.actions_cdc
    CROSS JOIN max_loaded

    WHERE op != 'd'
      AND cdc_ts_ms > max_loaded.max_cdc_ts
)

SELECT
    event_id,
    user_id,
    target_id,
    action,
    created_at,
    ingested_at_bronze,
    cdc_ts_ms

FROM ranked
WHERE rn = 1