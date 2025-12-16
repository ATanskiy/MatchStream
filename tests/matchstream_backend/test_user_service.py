import pytest
from fastapi import HTTPException
from matchstream_app.matchstream_backend.services import UserService


class FakeUserRepo:
    def __init__(self, login_row=None, discover_row=None):
        self.login_row = login_row
        self.discover_row = discover_row

    def create_user(self, *args, **kwargs):
        pass

    def get_login(self, email):
        return self.login_row

    def discover(self, **kwargs):
        return self.discover_row

    def get_filters(self):
        return {"states": ["CA"]}


def test_login_success(monkeypatch):
    service = UserService()
    service.repo = FakeUserRepo(login_row=("user123", "pass"))

    token = service.login(type("Req", (), {"email": "a", "password": "pass"}))
    assert isinstance(token, str)


def test_login_failure_wrong_password(monkeypatch):
    service = UserService()
    service.repo = FakeUserRepo(login_row=("user123", "pass"))

    with pytest.raises(HTTPException):
        service.login(type("Req", (), {"email": "a", "password": "wrong"}))


def test_discover_formats_response():
    row = (
        "id1", "A", "B", "male", "a@b.com", "123",
        "SF", "CA", "pic", "1990-01-01"
    )
    service = UserService()
    service.repo = FakeUserRepo(discover_row=row)

    result = service.discover("me", "CA", "SF", "male", 18, 30)

    assert result["user_id"] == "id1"
    assert result["city"] == "SF"