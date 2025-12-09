from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

@dataclass
class User:
    user_id: UUID
    gender: str
    first_name: str
    last_name: str
    email: str
    password: str
    dob: datetime
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
    created_at: datetime = field(default_factory=datetime.utcnow)
