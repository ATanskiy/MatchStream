

WITH src AS (SELECT * FROM bronze.users_cdc)

SELECT
    user_id,
    CAST(created_at AS TIMESTAMP) AS created_at,
    password,
    ingested_at AS ingested_at_bronze
FROM src