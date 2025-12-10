WITH src AS (
    SELECT DISTINCT
        city AS city_name,
        state_id AS raw_state_id,
        CAST(latitude AS DOUBLE) AS latitude,
        CAST(longitude AS DOUBLE) AS longitude,
        ingested_at
    FROM {{ source('bronze', 'users_cdc') }}
    WHERE city IS NOT NULL
),

joined AS (
    SELECT
        s.city_name,
        st.state_id,               -- surrogate key from states
        s.raw_state_id,
        s.latitude,
        s.longitude,
        s.ingested_at
    FROM src s
    LEFT JOIN {{ ref('dim_states') }} st
        ON s.raw_state_id = st.state_name_id
),

with_ids AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['city_name', 'state_id']) }} AS city_id,
        city_name,
        state_id,
        latitude,
        longitude,
        MAX(ingested_at) AS last_ingested_at
    FROM joined
    GROUP BY city_name, state_id, latitude, longitude
)

SELECT *
FROM with_ids