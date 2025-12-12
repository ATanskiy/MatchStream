import os
from typing import Optional


class JobConfig:
    """Configuration class loaded from environment variables."""

    def __init__(self) -> None:
        self.aws_key: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_endpoint: Optional[str] = os.getenv("S3_ENDPOINT_URL")
        self.hive_metastore: Optional[str] = os.getenv("THRIFT_HIVE_METASTORE")
        self.catalog_type: Optional[str] = os.getenv("CATALOG_TYPE")
        self.kafka_bootstrap: Optional[str] = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        self.kafka_users_topic: Optional[str] = os.getenv("KAFKA_USERS_TOPIC")

        self._validate()

    def _validate(self) -> None:
        """Validate required config values."""
        required = [
            self.aws_key, self.aws_secret, self.s3_endpoint,
            self.hive_metastore, self.catalog_type, self.kafka_bootstrap
        ]
        if any(v is None for v in required):
            raise ValueError("Missing required environment variables for JobConfig")