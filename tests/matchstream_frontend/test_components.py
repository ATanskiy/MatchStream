from datetime import datetime
from matchstream_app.matchstream_frontend.app.utils.components import (
    calculate_age,
    profile_card_html,
)


def test_calculate_age_valid_date():
    year = datetime.today().year
    expected = str(year - 1990)
    assert calculate_age("1990-01-01") in {expected, str(int(expected) - 1)}


def test_calculate_age_today():
    today = datetime.today().strftime("%Y-%m-%d")
    assert calculate_age(today) == "0"


def test_calculate_age_invalid():
    assert calculate_age("invalid") == ""
    assert calculate_age("") == ""


def test_profile_card_html_full_profile():
    profile = {
        "picture": "http://test.com/img.jpg",
        "dob": "1990-01-01",
        "gender": "male",
        "city": "SF",
        "state": "CA",
        "email": "test@email.com",
        "phone": "123-456",
    }

    html = profile_card_html(profile, photo_size_px=350)

    assert 'src="http://test.com/img.jpg"' in html
    assert "👤 Male" in html
    assert "🎂" in html
    assert "years old" in html
    assert "📅 Born on 1990-01-01" in html
    assert "📍 SF, CA" in html
    assert "✉️ test@email.com" in html
    assert "📞 123-456" in html


def test_profile_card_html_empty_profile():
    html = profile_card_html({})

    assert "https://via.placeholder.com" in html
    assert "About Me:" in html
    assert "👤" not in html
    assert "🎂" not in html
    assert "📍" not in html
