import requests, random, secrets, string, logging
from uuid import uuid4
from datetime import datetime
from generator.cities_loader import CitiesLoader
from utils.user import User
from config.settings import US_CITIES_CSV_PATH, RANDOMUSER_URL

logger = logging.getLogger(__name__)

class UserGenerator:

    def __init__(self):
        self.cities = CitiesLoader(US_CITIES_CSV_PATH)
        self.RANDOMUSER_URL = RANDOMUSER_URL

    def _fetch_users(self, count):
        logger.info(f"Fetching {count} users from RandomUser API")
        response = requests.get(self.RANDOMUSER_URL + str(count))
        response.raise_for_status()
        return response.json().get("results", [])

    def _generate_password(self, length=12):
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def generate(self, min_users=5, max_users=35):
        count = random.randint(min_users, max_users)
        raw_users = self._fetch_users(count)

        users = []

        for ru in raw_users:
            if ru["dob"]["age"] < 18:
                continue

            city = self.cities.get_random_city()
            dob = datetime.fromisoformat(ru["dob"]["date"].replace("Z", "+00:00"))

            user = User(
                user_id=uuid4(),
                gender=ru["gender"],
                first_name=ru["name"]["first"],
                last_name=ru["name"]["last"],
                email=ru["email"],
                password=self._generate_password(),
                dob=dob,
                phone=ru["phone"],
                cell=ru["cell"],
                picture_large=ru["picture"]["large"],
                picture_medium=ru["picture"]["medium"],
                picture_thumbnail=ru["picture"]["thumbnail"],
                city=city["city"],
                state=city["state"],
                state_id=city["state_id"],
                postcode=city["postcode"],
                latitude=city["lat"],
                longitude=city["lng"],
            )

            users.append(user)

        logger.info(f"Generated {len(users)} adult users")
        return users