{{ config(
    materialized='table',
    table_type='iceberg'
) }}

SELECT
    user1,
    user2,
    created_at AS matched_at,
    DATE(created_at) AS matched_date

FROM {{ ref('fct_matches') }}