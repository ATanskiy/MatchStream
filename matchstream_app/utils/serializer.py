from dataclasses import asdict
from uuid import UUID
from datetime import datetime


def user_to_dict(user):
    d = asdict(user)

    # Ensure UUID and datetime are serializable
    d["user_id"] = str(d["user_id"])
    d["dob"] = d["dob"].isoformat()
    d["created_at"] = user.created_at.isoformat()

    return d