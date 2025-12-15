from fastapi import FastAPI
from matchstream_backend.schemas import RegisterRequest, LoginRequest, SwipeRequest
from matchstream_backend.auth import AuthService
from matchstream_backend.services import UserService, SwipeService
from matchstream_backend.repositories import SwipeRepository

app = FastAPI(title="MatchStream Backend API")

user_service = UserService()
swipe_repo = SwipeRepository()
swipe_service = SwipeService(swipe_repo)


@app.post("/register")
def register(req: RegisterRequest):
    return {"token": user_service.register(req)}


@app.post("/login")
def login(req: LoginRequest):
    return {"token": user_service.login(req)}


@app.get("/discover")
def discover(state: str, city: str, token: str):
    user_id = AuthService.get_user_id_from_token(token)
    user = user_service.discover(user_id, state, city)
    return user or {"message": "No more users"}


@app.post("/swipe")
def swipe(req: SwipeRequest, token: str):
    user_id = AuthService.get_user_id_from_token(token)
    swipe_service.swipe(user_id, req.target_id, req.action)
    return {"status": "ok"}


@app.get("/matches")
def matches(token: str):
    user_id = AuthService.get_user_id_from_token(token)
    return swipe_service.matches(user_id)


@app.get("/filters")
def filters(token: str | None = None):
    return user_service.filters()