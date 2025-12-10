{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='user_id',
    table_type='iceberg',
    on_schema_change='sync_all_columns'
) }}

WITH src AS (SELECT * FROM {{ source('bronze', 'users_cdc') }})

SELECT
    user_id,
    CAST(created_at AS TIMESTAMP) AS created_at,
    password,
    ingested_at AS ingested_at_bronze
FROM src