from matchstream_app.user_ingestor_to_writer.repository.user_repository import UserRepository
from matchstream_app.user_ingestor_to_writer.models.user import User
from datetime import datetime


def test_upsert_calls_execute_many(mocker):
    mock_client = mocker.Mock()

    repo = UserRepository(mock_client)

    users = [
        User(
            user_id="u1",
            gender="male",
            first_name="A",
            last_name="B",
            email="a@test.com",
            password="x",
            dob="1990",
            phone="1",
            cell="2",
            picture_large="l",
            picture_medium="m",
            picture_thumbnail="t",
            city="c",
            state="s",
            state_id="s",
            postcode="p",
            latitude=1.0,
            longitude=2.0,
            created_at=datetime.utcnow(),
        )
    ]

    inserted = repo.upsert(users)

    mock_client.execute_many.assert_called_once()
    assert inserted == 1
