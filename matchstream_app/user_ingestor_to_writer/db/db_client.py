import psycopg2
from psycopg2.extras import execute_values

class PostgresClient:
    def __init__(self, url: str):
        self._url = url
        self._conn = None

    def connect(self):
        if not self._conn or self._conn.closed:
            self._conn = psycopg2.connect(self._url)
            self._conn.autocommit = False
        return self._conn

    def execute_many(self, sql: str, values: list[tuple]):
        conn = self.connect()
        with conn.cursor() as cur:
            execute_values(cur, sql, values)
        conn.commit()

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()