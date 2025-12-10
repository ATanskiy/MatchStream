{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='user_id',
    table_type='iceberg',
    on_schema_change='append_new_columns'
) }}

WITH src AS (
    SELECT *
    FROM {{ source('bronze', 'users_cdc') }}
),

mapped AS (
    SELECT
        s.user_id,
        s.gender,
        s.first_name,
        s.last_name,
        st.state_id AS state_id,        -- surrogate
        ct.city_id AS city_id,          -- surrogate
        s.latitude,
        s.longitude,
        date_add('1970-01-01', s.dob_days) AS dob,
        s.created_at,
        s.ingested_at AS ingested_at_bronze
    FROM src s
    LEFT JOIN {{ ref('dim_states') }} st
        ON s.state_id = st.state_name_id
    LEFT JOIN {{ ref('dim_cities') }} ct
        ON s.city = ct.city_name
        AND st.state_id = ct.state_id
)

SELECT *
FROM mapped