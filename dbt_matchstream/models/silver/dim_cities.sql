{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='city_id',
    table_type='iceberg',
    on_schema_change='sync_all_columns'
) }}

WITH base AS (
    SELECT DISTINCT
        city AS city_name,
        state_id AS state_name_id,   -- old code passed original ID
        CAST(latitude AS DOUBLE) AS latitude,
        CAST(longitude AS DOUBLE) AS longitude,
        ingested_at
    FROM {{ source('bronze', 'users_cdc') }}
    WHERE city IS NOT NULL
),

joined AS (
    SELECT
        b.city_name,
        st.state_id,        -- THE FIX (surrogate key)
        b.latitude,
        b.longitude,
        b.ingested_at
    FROM base b
    LEFT JOIN {{ ref('dim_states') }} st
        ON b.state_name_id = st.state_name_id
),

ordered AS (
    SELECT
        city_name,
        state_id,
        MAX(ingested_at) AS last_ingested_at
    FROM joined
    GROUP BY city_name, state_id
),

with_ids AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY state_id, city_name) AS city_id,
        city_name,
        state_id,
        last_ingested_at
    FROM ordered
)

SELECT *
FROM with_ids