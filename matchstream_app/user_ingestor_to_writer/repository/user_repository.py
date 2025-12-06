from models.user import User
from db.db_client import PostgresClient

class UserRepository:
    def __init__(self, client: PostgresClient, table: str = "matchstream.users"):
        self.client = client
        self.table = table

    def upsert(self, users: list[User]) -> int:
        if not users:
            return 0

        sql = f"""
            INSERT INTO {self.table} (
                user_id, gender, first_name, last_name, email,
                password, dob, phone, cell,
                picture_large, picture_medium, picture_thumbnail,
                city, state, state_id, postcode,
                latitude, longitude, created_at
            )
            VALUES %s
            ON CONFLICT (user_id) DO NOTHING
        """

        values = [
            (
                u.user_id, u.gender, u.first_name, u.last_name, u.email,
                u.password, u.dob, u.phone, u.cell,
                u.picture_large, u.picture_medium, u.picture_thumbnail,
                u.city, u.state, u.state_id, u.postcode,
                u.latitude, u.longitude, u.created_at,
            )
            for u in users
        ]

        self.client.execute_many(sql, values)
        return len(values)
