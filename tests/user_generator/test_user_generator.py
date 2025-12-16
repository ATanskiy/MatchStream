from unittest.mock import MagicMock
from matchstream_app.user_generator.generator.user_generator import UserGenerator


def test_generate_filters_underage(mocker):
    mocker.patch(
        "matchstream_app.user_generator.generator.user_generator.RANDOMUSER_URL",
        "http://fake-randomuser/?results="
    )

    fake_api_response = {
        "results": [
            {
                "gender": "male",
                "name": {"first": "John", "last": "Doe"},
                "email": "john@test.com",
                "dob": {"date": "1990-01-01T00:00:00Z", "age": 30},
                "phone": "1",
                "cell": "2",
                "picture": {"large": "L", "medium": "M", "thumbnail": "T"},
            },
            {
                "gender": "female",
                "name": {"first": "Kid", "last": "Test"},
                "email": "kid@test.com",
                "dob": {"date": "2012-01-01T00:00:00Z", "age": 12},
                "phone": "3",
                "cell": "4",
                "picture": {"large": "L", "medium": "M", "thumbnail": "T"},
            },
        ]
    }

    mock_resp = MagicMock()
    mock_resp.json.return_value = fake_api_response
    mock_resp.raise_for_status.return_value = None

    mocker.patch(
        "matchstream_app.user_generator.generator.user_generator.requests.get",
        return_value=mock_resp,
    )

    generator = UserGenerator()
    users = list(generator.generate())

    assert len(users) == 1
    assert users[0].email == "john@test.com"
