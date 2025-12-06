from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    user_id: str
    gender: str
    first_name: str
    last_name: str
    email: str
    password: str
    dob: str
    phone: str
    cell: str
    picture_large: str
    picture_medium: str
    picture_thumbnail: str
    city: str
    state: str
    state_id: str
    postcode: str
    latitude: float
    longitude: float
    created_at: datetime
