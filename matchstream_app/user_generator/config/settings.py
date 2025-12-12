import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Producer Settings
US_CITIES_CSV_PATH = os.path.join(BASE_DIR, "us_cities", "uscities.csv")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERS_TOPIC = os.getenv("KAFKA_USERS_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

RANDOMUSER_URL = os.getenv("RANDOMUSER_URL")