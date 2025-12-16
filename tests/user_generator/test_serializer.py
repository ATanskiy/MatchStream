from datetime import datetime
from uuid import uuid4
from matchstream_app.user_generator.utils.user import User
from matchstream_app.user_generator.utils.serializer import user_to_dict


def test_serialize_user():
    user = User(
        user_id=uuid4(),
        gender="male",
        first_name="John",
        last_name="Doe",
        email="a@b.com",
        password="pwd",
        dob=datetime(1990, 1, 1),
        phone="1",
        cell="2",
        picture_large="L",
        picture_medium="M",
        picture_thumbnail="T",
        city="NY",
        state="NY",
        state_id="NY",
        postcode="10001",
        latitude=1.0,
        longitude=2.0,
    )

    data = user_to_dict(user)

    assert data["first_name"] == "John"
    assert isinstance(data["dob"], str)
