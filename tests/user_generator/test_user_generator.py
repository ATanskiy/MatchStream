import sys
from types import SimpleNamespace
from unittest.mock import MagicMock
# -----------------------------
# Fake config.settings
# -----------------------------
fake_settings = SimpleNamespace(
    US_CITIES_CSV_PATH="tests/fixtures/us_cities.csv",
    RANDOMUSER_URL="https://example.com",
)

sys.modules["config"] = SimpleNamespace(settings=fake_settings)
sys.modules["config.settings"] = fake_settings

# -----------------------------
# Fake generator.cities_loader
# -----------------------------
fake_cities_loader = SimpleNamespace(
    CitiesLoader=MagicMock()
)

# -----------------------------
# Fake generator.user_generator
# -----------------------------
fake_user_generator_module = SimpleNamespace(
    RANDOMUSER_URL="https://example.com",
    CitiesLoader=fake_cities_loader.CitiesLoader,
)

# -----------------------------
# Register fake package tree
# -----------------------------
sys.modules["generator"] = SimpleNamespace(
    cities_loader=fake_cities_loader,
    user_generator=fake_user_generator_module,
)

sys.modules["generator.cities_loader"] = fake_cities_loader
sys.modules["generator.user_generator"] = fake_user_generator_module

sys.modules["config"] = SimpleNamespace(settings=fake_settings)
sys.modules["config.settings"] = fake_settings

# ---- FORCE module existence ----
from matchstream_app.user_generator.generator.user_generator import UserGenerator

def test_generate_filters_underage(mocker):
    mocker.patch(
        "matchstream_app.user_generator.generator.user_generator.RANDOMUSER_URL",
        "http://fake-randomuser/?results="
    )

    mocker.patch(
        "matchstream_app.user_generator.generator.user_generator.CitiesLoader",
        return_value=MagicMock(
            get_random_city=lambda: {
                "city": "TestCity",
                "state": "TestState",
                "state_id": "TS",
                "postcode": "00000",
                "lat": 0.0,
                "lng": 0.0,
            }
        ),
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
                "picture": {
                    "large": "L",
                    "medium": "M",
                    "thumbnail": "T",
                },
            },
            {
                "gender": "female",
                "name": {"first": "Kid", "last": "Test"},
                "email": "kid@test.com",
                "dob": {"date": "2012-01-01T00:00:00Z", "age": 12},
                "phone": "3",
                "cell": "4",
                "picture": {
                    "large": "L",
                    "medium": "M",
                    "thumbnail": "T",
                },
            },
        ]
    }

    mock_resp = MagicMock()
    mock_resp.json.return_value = fake_api_response
    mock_resp.raise_for_status.return_value = None

    # 🔑 THIS IS THE FIX
    mocker.patch(
        "matchstream_app.user_generator.generator.user_generator.requests.get",
        return_value=mock_resp
    )

    generator = UserGenerator()
    users = generator.generate()

    assert len(users) == 1
    assert users[0].first_name == "John"