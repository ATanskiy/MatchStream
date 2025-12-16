

WITH b AS (SELECT * FROM silver.users),
     c AS (SELECT * FROM silver.users_contact),
     p AS (SELECT * FROM silver.users_picture),
     m AS (SELECT * FROM silver.users_metadata),
     ci AS (SELECT * FROM silver.dim_cities),
     st AS (SELECT * FROM silver.dim_states)

SELECT
    b.user_id,
    b.gender,
    b.first_name,
    b.last_name,
    FLOOR(DATEDIFF(current_date, b.dob) / 365) AS age,

    -- Contact
    c.phone,
    c.cell,
    c.email,

    -- Pictures
    p.picture_large,
    p.picture_medium,
    p.picture_thumbnail,

    -- Geo (surrogate dimension values)
    ci.city_name,
    st.state_name,
    st.state_name_id,

    b.latitude,
    b.longitude,

    -- Metadata
    m.created_at,
    b.ingested_at_bronze
FROM b
LEFT JOIN c  ON b.user_id = c.user_id
LEFT JOIN p  ON b.user_id = p.user_id
LEFT JOIN m  ON b.user_id = m.user_id
LEFT JOIN ci ON b.city_id = ci.city_id
LEFT JOIN st ON b.state_id = st.state_id