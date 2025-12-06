import signal
import json
from kafka import KafkaConsumer

class UserDbWriterService:

    def __init__(self, consumer, mapper, repository, batch_size: int):
        self.consumer = consumer
        self.mapper = mapper
        self.repository = repository
        self.batch_size = batch_size
        self._running = True

    def _stop(self, *_):
        print("🛑 Stopping service...")
        self._running = False

    def _setup_signals(self):
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def run(self):
        self._setup_signals()
        print("🚀 UserDbWriterService started...")

        while self._running:
            polled = self.consumer.poll(timeout_ms=1000, max_records=self.batch_size)

            events = [record.value for _, recs in polled.items() for record in recs]
            if not events:
                continue

            users = [self.mapper.from_event(e) for e in events]
            inserted = self.repository.upsert(users)

            print(f"✅ Inserted {inserted} users")
            self.consumer.commit()

        print("Closing Kafka consumer...")
        self.consumer.close()
