from pyspark.sql import DataFrame, functions as F
from base.spark_app import SparkApp
from configs.jobs.job_config import JobConfig
from schemas.cdc_actions import get_envelope_schema
from transformers.actions_cdc_transform import flatten_cdc


class StreamActionsCDCBronze(SparkApp):
    """Streaming job to ingest actions CDC from Kafka to bronze.actions_cdc."""

    def __init__(self, config: JobConfig) -> None:
        super().__init__("StreamActionsCdcBronze", config)
        self.checkpoint_location = (
            f"{self.config.checkpoint_base}/"
            f"{self.config.checkpoint_actions_cdc_bronze}"
        )

    def write_batch(self, df: DataFrame, batch_id: int) -> None:
        df.writeTo("matchstream.bronze.actions_cdc").append()

    def run(self) -> None:
        envelope_schema = get_envelope_schema()

        raw_df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.config.kafka_bootstrap)
            .option("subscribe", self.config.kafka_actions_cdc_topic)
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