import json, logging
from kafka import KafkaProducer
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_USERS_TOPIC

logger = logging.getLogger(__name__)

class UserKafkaProducer:
    def __init__(self, servers=KAFKA_BOOTSTRAP_SERVERS, topic=KAFKA_USERS_TOPIC):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        logger.info(f"Kafka Producer connected to {servers}, topic='{topic}'")

    def send(self, data: dict):
        self.producer.send(self.topic, value=data)

    def flush(self):
        self.producer.flush()
        logger.info("Flushed Kafka producer")