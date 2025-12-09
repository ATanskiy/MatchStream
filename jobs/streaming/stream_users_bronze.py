from base.spark_app import SparkApp

class StreamUsersBronze(SparkApp):
    def __init__(self):
        super().__init__("StreamUsersBronze")

    def write_batch(self, df, batch_id):
        count = df.count()
        self.log.info(f"Writing batch {batch_id} with {count} rows")

        if count > 0:
            df.writeTo("matchstream.bronze.users_raw").append()
            self.log.info(f"Successfully wrote {count} rows to matchstream.bronze.users_raw")

    def run(self):
        df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.config.kafka_bootstrap)
            .option("subscribe", self.config.kafka_users_topic)
            .load()
            .selectExpr(
                "uuid() AS event_id",
                "CAST(value AS STRING) AS json_raw",
                "current_timestamp() AS inserted_at")
        )

        query = (
            df.writeStream
            .foreachBatch(self.write_batch)
            .option("checkpointLocation", "s3a://matchstream/checkpoints/users_bronze")
            .trigger(processingTime="30 seconds")
            .start())

        self.log.info("Streaming started.")
        query.awaitTermination()