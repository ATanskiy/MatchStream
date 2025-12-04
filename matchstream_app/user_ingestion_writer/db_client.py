# prod_ingestion/db_client.py

import psycopg2
from psycopg2.extensions import connection as PgConnection

from matchstream_app.user_ingestion_writer.settings import WRITER_DB_URL, WRITER_DB_USER, WRITER_DB_PASSWORD


class PostgresClient:
    """
    Thin wrapper around psycopg2 connection.
    Responsible only for connecting & closing.
    """

    def __init__(
        self,
        db_url: str = WRITER_DB_URL,
        user: str = WRITER_DB_USER,
        password: str = WRITER_DB_PASSWORD,
    ):
        self._db_url = db_url
        self._user = user
        self._password = password
        self._conn: PgConnection | None = None

    def connect(self) -> PgConnection:
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                self._db_url,
                user=self._user,
                password=self._password,
            )
            self._conn.autocommit = False
        return self._conn

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()
            self._conn = None
