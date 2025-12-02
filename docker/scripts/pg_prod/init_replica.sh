#!/bin/sh
set -e

echo "Waiting for pg_writer..."

until pg_isready -h pg_writer -p 5432 -U replica_user; do
  >&2 echo "pg_writer is unavailable - sleeping"
  sleep 2
done

echo "pg_writer is up!"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SUBSCRIPTION matchstream_sub
    CONNECTION 'host=pg_writer port=5432 user=replica_user password=replica_pass dbname=matchstream'
    PUBLICATION matchstream_pub;
EOSQL

echo "Replica initialized successfully!"
