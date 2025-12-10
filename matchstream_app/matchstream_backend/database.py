import os

print("DEBUG READER USER:", os.getenv("REPLICA_DB_USER"))
print("DEBUG READER PASS:", os.getenv("REPLICA_DB_PASSWORD"))
print("DEBUG REPLICA URL:", os.getenv("PG_REPLICA_URL"))

import psycopg
from dotenv import load_dotenv

load_dotenv()

PG_WRITER_URL = os.getenv("PG_WRITER_URL")
PG_REPLICA_URL = os.getenv("PG_REPLICA_URL")


def get_writer():
    return psycopg.connect(PG_WRITER_URL)


def get_reader():
    return psycopg.connect(PG_REPLICA_URL)