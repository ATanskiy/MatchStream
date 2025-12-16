

-- 1. Берём уникальные штаты
WITH base AS (
    SELECT DISTINCT
        state AS state_name,
        state_id AS state_name_id,
        ingested_at
    FROM bronze.users_cdc
    WHERE state IS NOT NULL
),

-- 2. Делаем детерминированный список штатов
ordered AS (
    SELECT
        state_name,
        state_name_id,
        MAX(ingested_at) AS last_ingested_at
    FROM base
    GROUP BY state_name, state_name_id
),

-- 3. Назначаем serial-like ID
with_ids AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY state_name_id) AS state_id,
        state_name,
        state_name_id,
        last_ingested_at
    FROM ordered
)

SELECT *
FROM with_ids