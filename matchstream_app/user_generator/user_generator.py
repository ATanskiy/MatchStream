import requests, string, secrets
from uuid import uuid4
from datetime import datetime

from matchstream_app.data_models.user import User
from matchstream_app.user_generator.cities_loader import CitiesLoader
from matchstream_app.config.settings import US_CITIES_CSV_PATH

import random


class UserGenerator:
    def __init__(self):
        self.cities = CitiesLoader(US_CITIES_CSV_PATH)

    def fetch_random_users(self, count: int):
        url = f"https://randomuser.me/api/?nat=us&results={count}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["results"]
    
    def generate_password(self, length=12):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def generate_users(self, min_users=2, max_users=15):
        num = random.randint(min_users, max_users)
        raw_users = self.fetch_random_users(num)

        users = []

        for ru in raw_users:
            # Skip minors
            if ru["dob"]["age"] < 18:
                continue

            city = self.cities.get_random_city()

            user = User(
                user_id=uuid4(),
                gender=ru["gender"],
                first_name=ru["name"]["first"],
                last_name=ru["name"]["last"],
                email=ru["email"],
                password=self.generate_password(), 

                dob=datetime.fromisoformat(ru["dob"]["date"].replace("Z", "+00:00")),

                phone=ru["phone"],
                cell=ru["cell"],

                picture_large=ru["picture"]["large"],
                picture_medium=ru["picture"]["medium"],
                picture_thumbnail=ru["picture"]["thumbnail"] ,

                city=city["city"],
                state=city["state"],
                state_id=city["state_id"],
                postcode=city["postcode"],
                latitude=city["lat"],
                longitude=city["lng"],
            )

            users.append(user)

        return users