{{ config(
    materialized='table',
    table_type='iceberg'
) }}

SELECT
    user_id,
    target_id,
    action,
    created_at AS action_at,
    DATE(created_at) AS action_date

FROM {{ ref('fct_actions') }}