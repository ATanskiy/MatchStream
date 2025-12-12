import signal
from base.logging_mixin import LoggingMixin
from configs.jobs.job_config import JobConfig
from base.spark_session_factory import SparkSessionFactory


class SparkApp(LoggingMixin):
    """Base class for Spark applications, handling session creation and graceful shutdown."""

    def __init__(self, app_name: str, config: JobConfig) -> None:
        self.config = config
        self.spark = SparkSessionFactory.build(config, app_name)
        self._setup_signals()

    def _setup_signals(self) -> None:
        def stop_app(signum: int, frame: object) -> None:
            self.log.warning("Stopping Spark job gracefully...")
            self.spark.stop()

        signal.signal(signal.SIGTERM, stop_app)
        signal.signal(signal.SIGINT, stop_app)

    def run(self) -> None:
        raise NotImplementedError("Subclasses must override run()")