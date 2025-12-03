import json
from kafka import KafkaProducer

from matchstream_app.config.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_USERS_TOPIC
)


class UserKafkaProducer:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, topic=KAFKA_USERS_TOPIC):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send_user_event(self, user_dict: dict):
        """Send single user as Kafka event"""
        self.producer.send(self.topic, value=user_dict)

    def flush(self):
        self.producer.flush()