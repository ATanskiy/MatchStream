from pyspark.sql import functions as F
from pyspark.sql import DataFrame

from base.constants import CHECKPOINT_BASE
from base.spark_app import SparkApp
from configs.jobs.job_config import JobConfig
from schemas.cdc_users import get_envelope_schema
from transformers.users_cdc_transform import flatten_cdc


class StreamUsersCDCBronze(SparkApp):
    """Streaming job to ingest users CDC from Kafka to bronze.users_cdc."""

    def __init__(self, config: JobConfig) -> None:
        super().__init__("StreamUsersCdcBronze", config)
        self.checkpoint_location = f"{CHECKPOINT_BASE}/users_cdc_bronze"

    def write_batch(self, df: DataFrame, batch_id: int) -> None:
        df.writeTo("matchstream.bronze.users_cdc").append()

    def run(self) -> None:
        envelope_schema = get_envelope_schema()

        raw_df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.config.kafka_bootstrap)
            .option("subscribe", self.config.kafka_users_topic)
            .load()
        )

        parsed_df = (
            raw_df
            .select(
                "topic",
                "partition",
                "offset",
                F.col("timestamp").alias("kafka_timestamp"),
                F.col("value").cast("string").alias("json_str"),
            )
            .select(
                "*",
                F.from_json("json_str", envelope_schema).alias("root"),
            )
        )

        final_df = flatten_cdc(parsed_df)

        (
            final_df.writeStream
            .foreachBatch(self.write_batch)
            .option("checkpointLocation", self.checkpoint_location)
            .trigger(processingTime="30 seconds")
            .start()
            .awaitTermination()
        )