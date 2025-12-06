from typing import Iterable, Mapping
from psycopg2.extras import execute_values
from db_client import PostgresClient


class UserRepository:
    """
    Handles persistence of users into Postgres.
    Knows the table schema and how to upsert.
    """

    def __init__(self, pg_client: PostgresClient, table_name: str = "matchstream.users"):
        self._pg_client = pg_client
        self._table_name = table_name

    def upsert_users(self, users: Iterable[Mapping]) -> int:
        """
        Insert users into DB.
        If user_id already exists -> ignore (idempotent).
        Returns number of attempted inserts.
        """
        users = list(users)
        if not users:
            return 0

        conn = self._pg_client.connect()
        cursor = conn.cursor()

        insert_sql = f"""
            INSERT INTO {self._table_name} (
                user_id,
                gender,
                first_name,
                last_name,
                email,
                password,
                dob,
                phone,
                cell,
                picture_large,
                picture_medium,
                picture_thumbnail,
                city,
                state,
                state_id,
                postcode,
                latitude,
                longitude,
                created_at
            )
            VALUES %s
            ON CONFLICT (user_id) DO NOTHING
        """

        values = [
            (
                u["user_id"],
                u["gender"],
                u["first_name"],
                u["last_name"],
                u["email"],
                u["password"],
                u["dob"],
                u["phone"],
                u["cell"],
                u["picture_large"],
                u["picture_medium"],
                u["picture_thumbnail"],
                u["city"],
                u["state"],
                u["state_id"],
                u["postcode"],
                float(u["latitude"]),
                float(u["longitude"]),
                u["created_at"],
            )
            for u in users
        ]

        execute_values(cursor, insert_sql, values)
        conn.commit()
        cursor.close()

        return len(values)
