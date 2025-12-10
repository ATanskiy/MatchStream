CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    city TEXT,
    state TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_SWIPES_TABLE = """
CREATE TABLE IF NOT EXISTS swipes (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    target_id UUID NOT NULL,
    decision TEXT CHECK (decision IN ('like', 'dislike')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, target_id)
);
"""

CREATE_MATCHES_TABLE = """
CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    user1 UUID NOT NULL,
    user2 UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user1, user2)
);
"""