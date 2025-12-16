from fastapi.testclient import TestClient
from fastapi import HTTPException

import matchstream_app.matchstream_backend.main as main


class FakeUserService:
    def filters(self):
        return {"states": ["CA"], "cities": ["SF"]}

    def login(self, req):
        raise HTTPException(status_code=400, detail="Invalid credentials")


# 🔥 Monkeypatch the GLOBAL service used by routes
main.user_service = FakeUserService()

client = TestClient(main.app)


def test_filters_endpoint():
    r = client.get("/filters")
    assert r.status_code == 200
    assert "states" in r.json()


def test_login_invalid():
    r = client.post("/login", json={"email": "x", "password": "y"})
    assert r.status_code == 400