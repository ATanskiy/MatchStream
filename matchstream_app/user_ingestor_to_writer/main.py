import json, logging
from kafka import KafkaConsumer
from services.user_db_writer_service import UserDbWriterService
from configs.logging_config import setup_logging
from db.db_client import PostgresClient
from repository.user_repository import UserRepository
from mappers.user_mapper import UserMapper
from configs.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_USERS_TOPIC,
    KAFKA_GROUP_ID,
    WRITER_DB_URL,
    BATCH_SIZE,
)


class UserIngestorApplication:

    def __init__(self):
        # Initialize global logging
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing UserIngestorApplication...")

    def build(self):
        self.logger.info("Building dependencies...")

        # Kafka
        consumer = KafkaConsumer(
            KAFKA_USERS_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_GROUP_ID,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        # DB + repository + mapper
        pg_client = PostgresClient(WRITER_DB_URL)
        repo = UserRepository(pg_client)
        mapper = UserMapper()

        service = UserDbWriterService(
            consumer=consumer,
            mapper=mapper,
            repository=repo,
            batch_size=BATCH_SIZE,
        )

        self.logger.info("Dependencies built successfully.")
        return service

    def run(self):
        self.logger.info("UserIngestorApplication starting...")
        service = self.build()
        service.run()


def main():
    app = UserIngestorApplication()
    app.run()


if __name__ == "__main__":
    main()