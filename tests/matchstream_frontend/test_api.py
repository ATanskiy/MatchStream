import pytest
import requests_mock
import matchstream_app.matchstream_frontend.app.utils.api as api


@pytest.fixture
def mock_backend(monkeypatch):
    monkeypatch.setattr(api, "BACKEND", "http://test-backend")


def test_login(mock_backend):
    with requests_mock.Mocker() as m:
        m.post("http://test-backend/login", json={"token": "abc123"}, status_code=200)

        result = api.login("test@email.com", "pass")
        assert result["token"] == "abc123"

    # Error case
    with requests_mock.Mocker() as m:
        m.post("http://test-backend/login", status_code=401)

        with pytest.raises(Exception):
            api.login("bad@email.com", "wrong")


def test_discover(mock_backend):
    with requests_mock.Mocker() as m:
        m.get(
            "http://test-backend/discover",
            json={"user_id": 1, "first_name": "Test"},
            status_code=200,
        )

        result = api.discover("token", "CA", "SF", "male", 18, 30)
        assert result["user_id"] == 1


def test_swipe(mock_backend):
    with requests_mock.Mocker() as m:
        m.post("http://test-backend/swipe", status_code=200)

        api.swipe("token", "target123", "like")  # just ensure no exception