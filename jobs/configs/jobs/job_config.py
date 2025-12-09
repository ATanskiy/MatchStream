import os

class JobConfig:
    def __init__(self):
        self.aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_endpoint = os.getenv("S3_ENDPOINT_URL")
        self.hive_metastore = os.getenv("THRIFT_HIVE_METASTORE")
        self.catalog_type = os.getenv("CATALOG_TYPE")

        self.kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        self.kafka_users_topic = os.getenv("KAFKA_USERS_TOPIC")