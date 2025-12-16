{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['user1', 'user2'],
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

    FROM {{ source('bronze', 'matches_cdc') }}
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