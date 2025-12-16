from pyspark.sql import DataFrame, functions as F
from typing import Callable
from base.spark_app import SparkApp
from config.job_config import JobConfig
from pyspark.sql.types import StructType


class StreamCDCBronze(SparkApp):
    """Generic streaming job to ingest CDC from Kafka to bronze tables."""

    def __init__(
        self,
        config: JobConfig,
        topic: str,
        schema_getter: Callable[[], StructType],
        transform_fn: Callable[[DataFrame], DataFrame],
        table_name: str,
        checkpoint_suffix: str,
    ) -> None:
        super().__init__(f"StreamCDC_{checkpoint_suffix}", config)
        self.topic = topic
        self.schema_getter = schema_getter
        self.transform_fn = transform_fn
        self.table_name = table_name
        self.checkpoint_location = (
            f"{self.config.checkpoint_base}/{checkpoint_suffix}"
        )

    def write_batch(self, df: DataFrame, batch_id: int) -> None:
        try:
            record_count = df.count()
            self.log.info(
                f"Writing batch {batch_id}: {record_count} records to {self.table_name}"
            )
            
            df.writeTo(self.table_name).append()
            
            self.log.info(f"Successfully wrote batch {batch_id}")
        except Exception as e:
            self.log.error(
                f"Failed to write batch {batch_id} to {self.table_name}: {e}",
                exc_info=True
            )
            raise

    def run(self) -> None:
        envelope_schema = self.schema_getter()

        raw_df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.config.kafka_bootstrap)
            .option("subscribe", self.topic)
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

        final_df = self.transform_fn(parsed_df)

        (
            final_df.writeStream
            .foreachBatch(self.write_batch)
            .option("checkpointLocation", self.checkpoint_location)
            .trigger(processingTime="30 seconds")
            .start()
            .awaitTermination()
        )