import os
import requests

BACKEND = os.getenv("MATCHSTREAM_BACKEND", "http://matchstream_backend:8010")

def login(email: str, password: str) -> dict:
    r = requests.post(
        f"{BACKEND}/login",
        json={"email": email, "password": password},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def register(email: str, password: str, first_name: str, last_name: str) -> dict:
    r = requests.post(
        f"{BACKEND}/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def discover(token: str, state: str, city: str, filters: dict | None = None) -> dict:
    params = {"token": token, "state": state, "city": city}
    if filters:
        params.update(filters)

    r = requests.get(f"{BACKEND}/discover", params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def swipe(token: str, target_id: str, action: str) -> None:
    r = requests.post(
        f"{BACKEND}/swipe",
        params={"token": token},
        json={"target_id": target_id, "action": action},
        timeout=15,
    )
    r.raise_for_status()

def matches(token: str) -> list[dict]:
    r = requests.get(f"{BACKEND}/matches", params={"token": token}, timeout=20)
    r.raise_for_status()
    return r.json()

def get_filters(token: str) -> dict:
    r = requests.get(
        f"{BACKEND}/filters",
        params={"token": token},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()
