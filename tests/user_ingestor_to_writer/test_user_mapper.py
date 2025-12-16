from matchstream_app.user_ingestor_to_writer.mappers.user_mapper import UserMapper
from matchstream_app.user_ingestor_to_writer.models.user import User
from datetime import datetime


def test_from_event_maps_correctly():
    event = {
        "user_id": "u1",
        "gender": "male",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
        "password": "secret",
        "dob": "1990-01-01",
        "phone": "123",
        "cell": "456",
        "picture_large": "l",
        "picture_medium": "m",
        "picture_thumbnail": "t",
        "city": "NY",
        "state": "NY",
        "state_id": "NY",
        "postcode": "10001",
        "latitude": "40.7",
        "longitude": "-73.9",
        "created_at": datetime.utcnow(),
    }

    user = UserMapper.from_event(event)

    assert user.user_id == "u1"
    assert user.gender == "male"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.latitude == 40.7
    assert user.longitude == -73.9
