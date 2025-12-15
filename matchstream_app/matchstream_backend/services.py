import uuid
from fastapi import HTTPException
from matchstream_backend.repositories import UserRepository, SwipeRepository
from matchstream_backend.auth import AuthService


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, req):
        user_id = str(uuid.uuid4())
        try:
            self.repo.create_user(
                user_id,
                req.email,
                req.password,
                req.first_name,
                req.last_name
            )
        except Exception:
            raise HTTPException(400, "Email already registered")

        return AuthService.create_token(user_id)

    def login(self, req):
        row = self.repo.get_login(req.email)
        if not row:
            raise HTTPException(400, "Invalid login")

        user_id, stored_password = row
        if stored_password is None or req.password != stored_password:
            raise HTTPException(400, "Invalid login")

        return AuthService.create_token(str(user_id))

    def discover(self, user_id, state, city):
        row = self.repo.discover(user_id, state, city)
        if not row:
            return None

        return {
            "user_id": str(row[0]),
            "first_name": row[1],
            "last_name": row[2],
            "gender": row[3],
            "email": row[4],
            "phone": row[5],
            "city": row[6],
            "state": row[7],
            "picture": row[8],
            "dob": row[9],
        }

    def filters(self):
        return self.repo.get_filters()


class SwipeService:
    def __init__(self, repo):
        self.repo = repo

    def swipe(self, user_id: str, target_id: str, action: str):
        self.repo.insert_swipe(user_id, target_id, action)

        if action == "like" and self.repo.is_mutual_like(user_id, target_id):
            self.repo.insert_match(user_id, target_id)