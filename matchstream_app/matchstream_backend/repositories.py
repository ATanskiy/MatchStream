from matchstream_backend.database import get_writer, get_reader


class UserRepository:
    def create_user(self, user_id, email, password, first_name, last_name):
        conn = get_writer()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (user_id, email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, email, password, first_name, last_name))
        conn.commit()
        conn.close()

    def get_login(self, email):
        conn = get_reader()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, password
            FROM users
            WHERE email=%s
        """, (email,))
        row = cur.fetchone()
        conn.close()
        return row

    def discover(self, user_id, state, city):
        conn = get_reader()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                user_id,
                first_name,
                last_name,
                gender,
                email,
                COALESCE(phone, cell),
                city,
                state,
                picture_large,
                dob
            FROM users
            WHERE state=%s
            AND city=%s
            AND user_id != %s
            AND user_id NOT IN (
                SELECT target_id FROM actions WHERE user_id=%s
            )
            LIMIT 1
        """, (state, city, user_id, user_id))
        row = cur.fetchone()
        conn.close()
        return row

    def get_filters(self):
        conn = get_reader()
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT state FROM users WHERE state IS NOT NULL")
        states = sorted([r[0] for r in cur.fetchall()])

        cur.execute("""
            SELECT state, city
            FROM users
            WHERE state IS NOT NULL AND city IS NOT NULL
            GROUP BY state, city
        """)
        cities = {}
        for state, city in cur.fetchall():
            cities.setdefault(state, []).append(city)
        for s in cities:
            cities[s].sort()

        cur.execute("SELECT DISTINCT gender FROM users WHERE gender IS NOT NULL")
        genders = sorted([r[0] for r in cur.fetchall()])

        cur.execute("""
            SELECT
              MIN(EXTRACT(YEAR FROM AGE(dob)))::int,
              MAX(EXTRACT(YEAR FROM AGE(dob)))::int
            FROM users
            WHERE dob IS NOT NULL
        """)
        min_age, max_age = cur.fetchone()

        conn.close()

        return {
            "states": states,
            "cities": cities,
            "genders": genders,
            "age": {"min": min_age, "max": max_age},
        }


class SwipeRepository:
    def insert_swipe(self, user_id, target_id, action):
        conn = get_writer()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO actions (user_id, target_id, action)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, target_id) DO NOTHING
        """, (user_id, target_id, action))
        conn.commit()
        conn.close()

    def is_mutual_like(self, user_id, target_id):
        conn = get_reader()
        cur = conn.cursor()
        cur.execute("""
            SELECT 1
            FROM actions
            WHERE user_id=%s AND target_id=%s AND action='like'
        """, (target_id, user_id))
        found = cur.fetchone() is not None
        conn.close()
        return found

    def insert_match(self, user_id, target_id):
        conn = get_writer()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO matches (user1, user2)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (user_id, target_id))
        conn.commit()
        conn.close()

    def get_matches(self, user_id):
        conn = get_reader()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                u.user_id,
                u.first_name,
                u.last_name,
                u.city,
                u.state,
                u.picture_large
            FROM matches m
            JOIN users u
              ON (
                (m.user1 = %s AND u.user_id = m.user2)
                OR
                (m.user2 = %s AND u.user_id = m.user1)
              )
        """, (user_id, user_id))
        rows = cur.fetchall()
        conn.close()
        return rows