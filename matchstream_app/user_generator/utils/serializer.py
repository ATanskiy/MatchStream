from dataclasses import asdict
from datetime import datetime
from uuid import UUID

def user_to_dict(user):
    data = asdict(user)

    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
        elif isinstance(value, UUID):
            data[key] = str(value)

    return data