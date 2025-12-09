import signal
from base.logging_mixin import LoggingMixin
from jobs.configs.jobs.job_config import JobConfig
from base.spark_session_factory import SparkSessionFactory

class SparkApp(LoggingMixin):

    def __init__(self, app_name):
        super().__init__()
        self.config = JobConfig()
        self.spark = SparkSessionFactory.build(self.config, app_name)
        self._running = True
        self._setup_signals()

    def _setup_signals(self):
        def stop_app(*_):
            self.log.warning("Stopping Spark job gracefully...")
            self._running = False
            self.spark.stop()

        signal.signal(signal.SIGTERM, stop_app)
        signal.signal(signal.SIGINT, stop_app)

    def run(self):
        raise NotImplementedError("Subclasses must override run()")