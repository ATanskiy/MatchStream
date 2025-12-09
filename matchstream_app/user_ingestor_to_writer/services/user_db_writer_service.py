import signal, logging

class UserDbWriterService:

    def __init__(self, consumer, mapper, repository, batch_size: int):
        self.consumer = consumer
        self.mapper = mapper
        self.repository = repository
        self.batch_size = batch_size
        self._running = True
        self.logger = logging.getLogger(self.__class__.__name__)

    def _stop(self, *_):
        self.logger.info("Received stop signal. Shutting down...")
        self._running = False

    def _setup_signals(self):
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def run(self):
        self._setup_signals()
        self.logger.info("Service started.")

        while self._running:
            polled = self.consumer.poll(timeout_ms=1000, max_records=self.batch_size)
            events = [rec.value for _, recs in polled.items() for rec in recs]

            if not events:
                continue

            users = [self.mapper.from_event(e) for e in events]
            inserted = self.repository.upsert(users)

            self.logger.info("Inserted %s users", inserted)
            self.consumer.commit()

        self.logger.info("Closing Kafka consumer.")
        self.consumer.close()