#!/bin/sh
set -e

echo "Waiting for pg_writer..."

until pg_isready -h pg_writer -p 5432 -U replica_user; do
  >&2 echo "pg_writer is unavailable - sleeping"
  sleep 2
done

echo "pg_writer is UP."

# Run inside replica container
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    -- Create schema if not exists
    CREATE SCHEMA IF NOT EXISTS matchstream;

    -- Create the same table as writer
    CREATE TABLE IF NOT EXISTS matchstream.users (
        id               BIGSERIAL PRIMARY KEY,  -- internal PK
        user_id          UUID UNIQUE NOT NULL,   -- business key from stream
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

    CREATE TABLE IF NOT EXISTS matchstream.actions (
        user_id    UUID NOT NULL,
        target_id  UUID NOT NULL,
        action     TEXT NOT NULL CHECK (action IN ('like', 'dislike')),
        created_at TIMESTAMPTZ DEFAULT NOW(),
        PRIMARY KEY (user_id, target_id)
    );

    CREATE TABLE IF NOT EXISTS matchstream.matches (
        user1      UUID NOT NULL,
        user2      UUID NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        PRIMARY KEY (user1, user2)
    );

    -- Drop subscription if already exists (safe redraw)
    DO \$\$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_subscription WHERE subname = 'matchstream_sub') THEN
            EXECUTE 'DROP SUBSCRIPTION matchstream_sub';
        END IF;
    END
    \$\$;

    -- Create subscription to writer
    CREATE SUBSCRIPTION matchstream_sub
    CONNECTION 'host=pg_writer port=5432 user=replica_user password=replica_pass dbname=matchstream'
    PUBLICATION matchstream_pub
    WITH (copy_data = true);

EOSQL

echo "Replica initialized successfully!"