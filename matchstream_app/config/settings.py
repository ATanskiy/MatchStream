import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Producer Settings
US_CITIES_CSV_PATH = os.path.join(
    BASE_DIR,
    "matchstream_app",
    "us_cities_csv",
    "uscities.csv"
)

KAFKA_BOOTSTRAP_SERVERS = "kafka_broker:9092"
KAFKA_USERS_TOPIC = "users"