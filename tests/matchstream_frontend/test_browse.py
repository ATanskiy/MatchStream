from datetime import datetime
from matchstream_app.matchstream_frontend.app.utils.components import profile_card_html, calculate_age  # Adjust import path if needed

def test_profile_card_html():
    profile = {
        'picture': 'http://test.com/img.jpg',
        'dob': '1990-01-01',
        'gender': 'male',
        'city': 'SF',
        'state': 'CA',
        'email': 'test@email.com',
        'phone': '123-456'
    }

    html = profile_card_html(profile, photo_size_px=350)  # Matches browse.py usage

    # Core checks
    assert 'src="http://test.com/img.jpg"' in html
    assert '👤 Male' in html
    assert '🎂 35 years old' in html  # Correct for current date (Dec 2025)
    assert '📅 Born on 1990-01-01' in html
    assert '📍 SF, CA' in html
    assert '✉️ test@email.com' in html
    assert '📞 123-456' in html

    # Bonus: Test edge cases
    empty_profile = {}
    html_empty = profile_card_html(empty_profile)
    assert 'https://via.placeholder.com' in html_empty  # Default photo
    assert 'About Me:' in html_empty
    # No personal info should appear
    assert '👤' not in html_empty
    assert '🎂' not in html_empty
    assert '📍' not in html_empty


# Optional: Test calculate_age directly for more precision
def test_calculate_age():
    assert calculate_age('1990-01-01') == '35'  # As of Dec 16, 2025
    assert calculate_age('2000-12-17') == '24'  # Birthday tomorrow → still 24
    assert calculate_age('2000-12-16') == '25'  # Birthday today → 25
    assert calculate_age('invalid') == ''     # Graceful fallback