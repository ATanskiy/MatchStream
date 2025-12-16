

WITH src AS (SELECT * FROM bronze.users_cdc)

SELECT
    user_id,
    picture_large,
    picture_medium,
    picture_thumbnail,
    ingested_at AS ingested_at_bronze
FROM src