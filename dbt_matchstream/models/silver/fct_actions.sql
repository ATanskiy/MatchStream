{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['user_id', 'target_id'],
    table_type='iceberg',
    on_schema_change='sync_all_columns'
) }}

WITH max_loaded AS (

    {% if is_incremental() %}
        SELECT MAX(cdc_ts_ms) AS max_cdc_ts
        FROM {{ this }}
    {% else %}
        SELECT CAST(0 AS BIGINT) AS max_cdc_ts
    {% endif %}

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

    FROM {{ source('bronze', 'actions_cdc') }}
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