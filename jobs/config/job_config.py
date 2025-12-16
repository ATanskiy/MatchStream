import os
from typing import Optional


class JobConfig:
    """Configuration class loaded from environment variables."""

    def __init__(self) -> None:
        self.aws_key: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_endpoint: Optional[str] = os.getenv("S3_ENDPOINT_URL")
        self.spark_warehouse_dir: Optional[str] = os.getenv("SPARK_WAREHOUSE_DIR")
        self.hive_metastore: Optional[str] = os.getenv("THRIFT_HIVE_METASTORE")
        self.catalog_type: Optional[str] = os.getenv("CATALOG_TYPE")
        self.kafka_bootstrap: Optional[str] = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        self.kafka_users_cdc_topic: Optional[str] = os.getenv("KAFKA_USERS_CDC_TOPIC")
        self.kafka_actions_cdc_topic: Optional[str] = os.getenv("KAFKA_ACTIONS_CDC_TOPIC")
        self.kafka_matches_cdc_topic: Optional[str] = os.getenv("KAFKA_MATCHES_CDC_TOPIC")
        self.checkpoint_base: Optional[str] = os.getenv("CHECKPOINT_BASE")
        self.checkpoint_users_cdc_bronze: Optional[str] = os.getenv("CHECKPOINT_USERS_CDC_BRONZE")
        self.checkpoint_actions_cdc_bronze: Optional[str] = os.getenv("CHECKPOINT_ACTIONS_CDC_BRONZE")
        self.checkpoint_matches_cdc_bronze: Optional[str] = os.getenv("CHECKPOINT_MATCHES_CDC_BRONZE")

        self._validate()

    def _validate(self) -> None:
        """Validate required config values."""
        required = {
            "AWS_ACCESS_KEY_ID": self.aws_key,
            "AWS_SECRET_ACCESS_KEY": self.aws_secret,
            "S3_ENDPOINT_URL": self.s3_endpoint,
            "SPARK_WAREHOUSE_DIR": self.spark_warehouse_dir,
            "THRIFT_HIVE_METASTORE": self.hive_metastore,
            "CATALOG_TYPE": self.catalog_type,
            "KAFKA_BOOTSTRAP_SERVERS": self.kafka_bootstrap,
            "KAFKA_USERS_CDC_TOPIC": self.kafka_users_cdc_topic,
            "KAFKA_ACTIONS_CDC_TOPIC": self.kafka_actions_cdc_topic,
            "KAFKA_MATCHES_CDC_TOPIC": self.kafka_matches_cdc_topic,
            "CHECKPOINT_BASE": self.checkpoint_base,
            "CHECKPOINT_USERS_CDC_BRONZE": self.checkpoint_users_cdc_bronze,
            "CHECKPOINT_ACTIONS_CDC_BRONZE": self.checkpoint_actions_cdc_bronze,
            "CHECKPOINT_MATCHES_CDC_BRONZE": self.checkpoint_matches_cdc_bronze,
        }
        
        missing = [name for name, value in required.items() if value is None]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )