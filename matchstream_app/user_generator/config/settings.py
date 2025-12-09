import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Producer Settings
US_CITIES_CSV_PATH = os.path.join(BASE_DIR, "us_cities", "uscities.csv")

KAFKA_BOOTSTRAP_SERVERS = "kafka_broker:9092"
KAFKA_USERS_TOPIC = "users"

RANDOMUSER_URL = "https://randomuser.me/api/?nat=us&results="