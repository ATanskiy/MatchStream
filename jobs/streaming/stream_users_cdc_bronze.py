from base.spark_app import SparkApp
from pyspark.sql import functions as F
from schemas.cdc_users import get_envelope_schema
from transformers.users_cdc_transform import flatten_cdc


class StreamUsersCDCBronze(SparkApp):
    def __init__(self):
        super().__init__("StreamUsersCdcBronze")

    def write_batch(self, df, batch_id):
        if df.count() > 0:
            df.writeTo("matchstream.bronze.users_cdc").append()

    def run(self):
        envelope_schema = get_envelope_schema()

        raw_df = (
            self.spark.readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", self.config.kafka_bootstrap)
                .option("subscribe", "users_cdc")
                .option("startingOffsets", "earliest")
                .load()
        )

        parsed_df = (
            raw_df
            .select(
                "topic",
                "partition",
                "offset",
                F.col("timestamp").alias("kafka_timestamp"),
                F.col("value").cast("string").alias("json_str"))
            .select(
                "*",
                F.from_json("json_str", envelope_schema).alias("root"))
        )

        final_df = flatten_cdc(parsed_df)

        (
            final_df.writeStream
                .foreachBatch(self.write_batch)
                .option("checkpointLocation", "s3a://matchstream/checkpoints/users_cdc_bronze")
                .trigger(processingTime="30 seconds")
                .start()
                .awaitTermination()
        )