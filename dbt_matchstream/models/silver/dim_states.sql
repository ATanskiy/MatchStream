{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='state_id',
    table_type='iceberg',
    on_schema_change='append_new_columns'
) }}

WITH src AS (
    SELECT DISTINCT
        state AS state_name,
        state_id AS state_name_id,
        ingested_at      -- FIXED HERE
    FROM {{ source('bronze', 'users_cdc') }}
    WHERE state IS NOT NULL
),

with_ids AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['state_name_id']) }} AS state_id,
        state_name,
        state_name_id,
        MAX(ingested_at) AS last_ingested_at
    FROM src
    GROUP BY state_name, state_name_id
)

SELECT *
FROM with_ids