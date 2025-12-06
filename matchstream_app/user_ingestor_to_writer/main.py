import json
from kafka import KafkaConsumer

from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_USERS_TOPIC,
    KAFKA_GROUP_ID,
    POSTGRES_URL,
    BATCH_SIZE,
)

from db.db_client import PostgresClient
from repository.user_repository import UserRepository
from mappers.user_mapper import UserMapper
from services.user_db_writer_service import UserDbWriterService


def build_service():
    consumer = KafkaConsumer(
        KAFKA_USERS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    pg = PostgresClient(POSTGRES_URL)
    repo = UserRepository(pg)
    mapper = UserMapper()

    return UserDbWriterService(
        consumer=consumer,
        mapper=mapper,
        repository=repo,
        batch_size=BATCH_SIZE,
    )


def main():
    service = build_service()
    service.run()


if __name__ == "__main__":
    main()
