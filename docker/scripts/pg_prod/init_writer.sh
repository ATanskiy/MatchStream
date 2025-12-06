#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    -- -------------------------------------
    -- Create replication user
    -- -------------------------------------
    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_roles WHERE rolname = 'replica_user'
        ) THEN
            CREATE ROLE replica_user WITH REPLICATION LOGIN PASSWORD 'replica_pass';
        END IF;
    END
    \$\$;


    -- -------------------------------------
    -- Create schema
    -- -------------------------------------
    CREATE SCHEMA IF NOT EXISTS matchstream;

    -- -------------------------------------
    -- Create users table
    -- -------------------------------------
    CREATE TABLE IF NOT EXISTS matchstream.users (
        id               BIGSERIAL PRIMARY KEY,  -- internal PK
        user_id          TEXT UNIQUE,            -- business key from stream
        gender           VARCHAR(20),
        first_name       VARCHAR(100),
        last_name        VARCHAR(100),
        email            VARCHAR(255),
        password         VARCHAR(255),
        dob              DATE,
        phone            VARCHAR(50),
        cell             VARCHAR(50),
        picture_large    TEXT,
        picture_medium   TEXT,
        picture_thumbnail TEXT,
        city             VARCHAR(150),
        state            VARCHAR(150),
        state_id         VARCHAR(10),
        postcode         VARCHAR(20),
        latitude         DOUBLE PRECISION,
        longitude        DOUBLE PRECISION,
        created_at       TIMESTAMPTZ
        );


    -- -------------------------------------
    -- GRANT permissions to replica_user
    -- -------------------------------------
    GRANT USAGE ON SCHEMA matchstream TO replica_user;
    GRANT SELECT ON ALL TABLES IN SCHEMA matchstream TO replica_user;

    -- Future tables also inherit permissions
    ALTER DEFAULT PRIVILEGES IN SCHEMA matchstream
        GRANT SELECT ON TABLES TO replica_user;


    -- -------------------------------------
    -- Setup publication
    -- -------------------------------------
    DROP PUBLICATION IF EXISTS matchstream_pub;
    CREATE PUBLICATION matchstream_pub FOR ALL TABLES;


    -- -------------------------------------
    -- Create replication slot
    -- -------------------------------------
    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_replication_slots WHERE slot_name = 'matchstream_slot'
        ) THEN
            PERFORM pg_create_logical_replication_slot('matchstream_slot', 'pgoutput');
        END IF;
    END
    \$\$;

EOSQL

echo "Writer database initialized successfully!"