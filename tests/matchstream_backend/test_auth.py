import pytest
from fastapi import HTTPException
from matchstream_app.matchstream_backend.auth import AuthService


def test_create_and_decode_token():
    token = AuthService.create_token("user123")
    user_id = AuthService.get_user_id_from_token(token)
    assert user_id == "user123"


def test_invalid_token():
    with pytest.raises(HTTPException):
        AuthService.get_user_id_from_token("invalid.token.here")
