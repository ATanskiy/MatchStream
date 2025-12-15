import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

PG_WRITER_URL = os.getenv("PG_WRITER_URL")
PG_REPLICA_URL = os.getenv("PG_REPLICA_URL")


def get_writer():
    conn = psycopg.connect(PG_WRITER_URL)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO matchstream")
    return conn


def get_reader():
    conn = psycopg.connect(PG_REPLICA_URL)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO matchstream")
    return conn
