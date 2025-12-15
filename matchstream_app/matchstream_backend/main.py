from fastapi import FastAPI, HTTPException
from matchstream_backend.database import get_writer, get_reader
from matchstream_backend.auth import create_token
from matchstream_backend.schemas import RegisterRequest, LoginRequest, SwipeRequest
import uuid
from matchstream_backend.auth import get_user_id_from_token

app = FastAPI(title="MatchStream Backend API")


@app.post("/register")
def register(req: RegisterRequest):
    conn = get_writer()
    cur = conn.cursor()

    user_id = str(uuid.uuid4())

    try:
        cur.execute("""
            INSERT INTO users (user_id, email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, req.email, req.password, req.first_name, req.last_name))
    except Exception:
        raise HTTPException(400, "Email already registered")

    conn.commit()
    conn.close()

    return {"token": create_token(user_id)}


@app.post("/login")
def login(req: LoginRequest):
    conn = get_reader()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, password
        FROM users
        WHERE email=%s
    """, (req.email,))
    row = cur.fetchone()

    if not row:
        raise HTTPException(400, "Invalid login")

    user_id, stored_password = row

    if stored_password is None or req.password != stored_password:
        raise HTTPException(400, "Invalid login")

    return {"token": create_token(str(user_id))}


@app.get("/discover")
def discover(state: str, city: str, token: str):
    user_id = get_user_id_from_token(token)

    conn = get_reader()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            user_id,
            first_name,
            last_name,
            gender,
            email,
            COALESCE(phone, cell) AS phone,
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

    user = cur.fetchone()
    if not user:
        return {"message": "No more users"}

    return {
        "user_id": str(user[0]),
        "first_name": user[1],
        "last_name": user[2],
        "gender": user[3],
        "email": user[4],
        "phone": user[5],
        "city": user[6],
        "state": user[7],
        "picture": user[8],
        "dob": user[9],
    }


@app.post("/swipe")
def swipe(req: SwipeRequest, token: str):
    user_id = get_user_id_from_token(token)

    conn = get_writer()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO actions (user_id, target_id, action)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, target_id) DO NOTHING
    """, (user_id, req.target_id, req.decision))

    if req.decision == "like":
        cur.execute("""
            SELECT 1
            FROM actions
            WHERE user_id = %s
            AND target_id = %s
            AND action = 'like'
        """, (req.target_id, user_id))

        if cur.fetchone():
            cur.execute("""
                INSERT INTO matches (user1, user2)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (user_id, req.target_id))

    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.get("/matches")
def get_matches(token: str):
    user_id = get_user_id_from_token(token)

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

    return [
        {
            "user_id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "city": r[3],
            "state": r[4],
            "picture": r[5],
        }
        for r in rows
    ]

@app.get("/filters")
def get_filters(token: str | None = None):
    conn = get_reader()
    cur = conn.cursor()

    # States
    cur.execute("SELECT DISTINCT state FROM users WHERE state IS NOT NULL")
    states = sorted([r[0] for r in cur.fetchall()])

    # Cities per state
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

    # Genders
    cur.execute("SELECT DISTINCT gender FROM users WHERE gender IS NOT NULL")
    genders = sorted([r[0] for r in cur.fetchall()])

    # Age range
    cur.execute("""
        SELECT
          MIN(EXTRACT(YEAR FROM AGE(dob)))::int,
          MAX(EXTRACT(YEAR FROM AGE(dob)))::int
        FROM users
        WHERE dob IS NOT NULL
    """)
    min_age, max_age = cur.fetchone()

    cur.close()
    conn.close()

    result = {
        "states": states,
        "cities": cities,
        "genders": genders,
        "age": {
            "min": min_age,
            "max": max_age
        }
    }

    print("DEBUG /filters response:", result)

    return {
        "states": states,
        "cities": cities,
        "genders": genders,
        "age": {
            "min": min_age,
            "max": max_age
        }
    }