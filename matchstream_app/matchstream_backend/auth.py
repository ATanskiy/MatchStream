from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from fastapi import HTTPException

JWT_SECRET = os.getenv("JWT_SECRET", "MATCHSTREAM_SECRET_KEY")
JWT_ALGO = "HS256"


class AuthService:
    @staticmethod
    def create_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
