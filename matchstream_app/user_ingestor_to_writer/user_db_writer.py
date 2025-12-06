# prod_ingestion/user_db_writer.py

import json
import signal
import sys
from typing import List

from kafka import KafkaConsumer

from settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_USERS_TOPIC
from db_client import PostgresClient
from user_repository import UserRepository


class UserDbWriterService:
    """
    Kafka consumer that reads user events and upserts them into Postgres.
    """

    def __init__(
        self,
        bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS,
        topic: str = KAFKA_USERS_TOPIC,
        group_id: str = "matchstream-users-db-writer",
        batch_size: int = 100,
    ):
        self._topic = topic
        self._batch_size = batch_size

        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False,  # we commit manually after DB write
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )

        pg_client = PostgresClient()
        self._user_repo = UserRepository(pg_client)

        self._running = True

    def _handle_sigint(self, *args):
        print("🛑 Stopping UserDbWriterService...")
        self._running = False

    def run_forever(self):
        signal.signal(signal.SIGINT, self._handle_sigint)
        signal.signal(signal.SIGTERM, self._handle_sigint)

        print(f"🚀 UserDbWriterService started. Consuming from topic '{self._topic}'")

        while self._running:
            batch: List[dict] = []
            msgs = self._consumer.poll(timeout_ms=1000, max_records=self._batch_size)

            for tp, records in msgs.items():
                for record in records:
                    batch.append(record.value)

            if not batch:
                continue

            inserted = self._user_repo.upsert_users(batch)
            print(f"✅ Upserted {inserted} users into Postgres")

            # commit Kafka offsets only after successful DB commit
            self._consumer.commit()

        print("Closing Kafka consumer...")
        self._consumer.close()


def main():
    service = UserDbWriterService()
    service.run_forever()


if __name__ == "__main__":
    main()
