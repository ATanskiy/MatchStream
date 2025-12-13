from fastapi import FastAPI, HTTPException
from matchstream_backend.database import get_writer, get_reader
from matchstream_backend.auth import create_token
from matchstream_backend.schemas import RegisterRequest, LoginRequest, SwipeRequest
import uuid

app = FastAPI(title="MatchStream Backend API")


@app.post("/register")
def register(req: RegisterRequest):
    conn = get_writer()
    cur = conn.cursor()

    user_id = str(uuid.uuid4())

    try:
        cur.execute("""
            INSERT INTO users (id, email, password, first_name, last_name)
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

    cur.execute("SELECT id, password FROM users WHERE email=%s", (req.email,))
    row = cur.fetchone()

    if not row:
        raise HTTPException(400, "Invalid login")

    user_id, stored_password = row

    if stored_password is None:
        raise HTTPException(400, "Invalid login")

    if req.password != stored_password:
        raise HTTPException(400, "Invalid login")

    return {"token": create_token(str(user_id))}


@app.get("/discover")
def discover(state: str, city: str, user_id: str):
    conn = get_reader()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, first_name, last_name, city, state
        FROM users
        WHERE state=%s
        AND city=%s
        AND id != %s
        AND id NOT IN (SELECT target_id FROM swipes WHERE user_id=%s)
        LIMIT 1
    """, (state, city, user_id, user_id))

    user = cur.fetchone()
    if not user:
        return {"message": "No more users"}

    return {
        "id": str(user[0]),
        "first_name": user[1],
        "last_name": user[2],
        "city": user[3],
        "state": user[4]
    }


@app.post("/swipe")
def swipe(user_id: str, req: SwipeRequest):
    conn = get_writer()
    cur = conn.cursor()

    # Save swipe
    cur.execute("""
        INSERT INTO swipes (user_id, target_id, decision)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, target_id) DO NOTHING
    """, (user_id, req.target_id, req.decision))

    # Check match
    if req.decision == "like":
        cur.execute("""
            SELECT 1 FROM swipes
            WHERE user_id=%s AND target_id=%s AND decision='like'
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