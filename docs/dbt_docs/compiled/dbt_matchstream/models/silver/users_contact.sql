

WITH src AS (SELECT * FROM bronze.users_cdc)

SELECT
    user_id,
    email,
    phone,
    cell,
    ingested_at AS ingested_at_bronze
FROM src