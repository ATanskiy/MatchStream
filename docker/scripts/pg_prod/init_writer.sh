#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE replica_user WITH REPLICATION LOGIN PASSWORD 'replica_pass';

    CREATE PUBLICATION matchstream_pub FOR ALL TABLES;

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
