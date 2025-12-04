import os, sys
sys.path.append("/opt/streaming")
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, to_date




from configs.spark_streaming.configs import (
    USER_SCHEMA,
    BRONZE_CHECKPOINT,
    WRITER_CHECKPOINT,
    KAFKA_TOPIC_USERS,
    BRONZE_TABLE_USERS,
    WRITER_STREAM_TABLE,
)

# ---------------------------
# Environment variables
# ---------------------------
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
THRIFT_HIVE_METASTORE = os.getenv("THRIFT_HIVE_METASTORE")
CATALOG_TYPE = os.getenv("CATALOG_TYPE")

WRITER_DB_URL = os.getenv("WRITER_DB_URL")
WRITER_USER = os.getenv("POSTGRES_USER")
WRITER_PASSWORD = os.getenv("POSTGRES_PASSWORD")

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


# ==========================================================
#                SPARK SESSION CREATION
# ==========================================================
def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("MatchStreamUsersIngestion")

        # Iceberg catalog
        .config("spark.sql.catalog.matchstream", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.matchstream.type", CATALOG_TYPE)
        .config("spark.sql.catalog.matchstream.uri", THRIFT_HIVE_METASTORE)
        .config("spark.sql.catalog.matchstream.warehouse", "s3a://matchstream/")
        .config("spark.sql.catalog.matchstream.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")

        # MinIO
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT_URL)
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark


# ==========================================================
#                   FOREACHBATCH WRITER
# ==========================================================
def write_to_postgres(batch_df, batch_id):
    # Avoid empty batch writes
    if not batch_df.head(1):
        return
    (
        batch_df
        .select(
            "user_id", "gender", "first_name", "last_name",
            "email", "password", "dob", "phone", "cell",
            "picture_large", "picture_medium", "picture_thumbnail",
            "city", "state", "state_id", "postcode",
            "latitude", "longitude", "created_at"
        )
        .write
        .format("jdbc")
        .option("url", WRITER_DB_URL)
        .option("dbtable", WRITER_STREAM_TABLE)
        .option("user", WRITER_USER)
        .option("password", WRITER_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

# ==========================================================
#                    MAIN STREAMING JOB
# ==========================================================
def main():
    spark = create_spark_session()

     # -----------------------------------------------------------
    # 1. Read from Kafka
    # -----------------------------------------------------------
    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC_USERS)
        .option("startingOffsets", "latest")
        .load()
    )

    # For parsing into structured users:
    value_df = kafka_df.selectExpr("CAST(value AS STRING) AS json_str")

    # -----------------------------------------------------------
    # 2a. Parse JSON → clean users for Postgres
    # -----------------------------------------------------------
    parsed_df = (
        value_df
        .select(from_json(col("json_str"), USER_SCHEMA).alias("data"))
        .select("data.*")
    )

    clean_df = (
        parsed_df
        .withColumn("dob", to_date(to_timestamp(col("dob"))))
        .withColumn("created_at", to_timestamp(col("created_at")))
        .withColumn("latitude", col("latitude").cast("double"))
        .withColumn("longitude", col("longitude").cast("double"))
    )

    pg_stream = (
        clean_df.writeStream
        .foreachBatch(write_to_postgres)
        .option("checkpointLocation", WRITER_CHECKPOINT)
        .trigger(processingTime="1 second")
        .outputMode("append")
        .start()
    )

    # -----------------------------------------------------------
    # 2b. Raw events → Iceberg bronze.users_raw
    #      (event_id, json_raw, inserted_at)
    # -----------------------------------------------------------
    bronze_df = value_df.selectExpr(
        "uuid() AS event_id",
        "json_str AS json_raw",
        "current_timestamp() AS inserted_at"
    )

    bronze_stream = (
        bronze_df.writeStream
        .format("iceberg")
        .option("checkpointLocation", BRONZE_CHECKPOINT)
        .trigger(processingTime="30 seconds")
        .toTable(BRONZE_TABLE_USERS)  # <- matchstream.bronze.users_raw
    )

    # -----------------------------------------------------------
    # 3. Keep both streams alive
    # -----------------------------------------------------------
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()