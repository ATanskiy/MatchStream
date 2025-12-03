import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, to_timestamp, to_date
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
THRIFT_HIVE_METASTORE = os.getenv("THRIFT_HIVE_METASTORE")
SPARK_WAREHOUSE_DIR = os.getenv("SPARK_WAREHOUSE_DIR")
CATALOG_TYPE = os.getenv("CATALOG_TYPE")


# ===============================================================
#                   CONFIGURATION
# ===============================================================

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka_broker:9092")
KAFKA_TOPIC = os.getenv("KAFKA_USERS_TOPIC", "users")

PG_URL = os.getenv("WRITER_DB_URL", "jdbc:postgresql://pg_writer:5432/matchstream")
PG_USER = os.getenv("WRITER_DB_USER", "writer_user")
PG_PASSWORD = os.getenv("WRITER_DB_PASSWORD", "writer_pass")
PG_TABLE = "matchstream.users"

BRONZE_TABLE = "bronze.users_raw"

BRONZE_CHECKPOINT = "s3a://default/checkpoints/bronze_users"
PG_CHECKPOINT = "s3a://default/checkpoints/pg_users"


# ===============================================================
#                   USER JSON SCHEMA
# ===============================================================

user_schema = StructType([
    StructField("user_id", StringType(), False),

    StructField("gender", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("password", StringType(), True),

    StructField("dob", StringType(), True),

    StructField("phone", StringType(), True),
    StructField("cell", StringType(), True),

    StructField("picture_large", StringType(), True),
    StructField("picture_medium", StringType(), True),
    StructField("picture_thumbnail", StringType(), True),

    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("state_id", StringType(), True),
    StructField("postcode", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),

    StructField("created_at", StringType(), True),
])


# ===============================================================
#                   MAIN SPARK JOB
# ===============================================================
def write_to_postgres(batch_df, batch_id):
    if batch_df.rdd.isEmpty():
        return

    (
        batch_df
        .select(
            "user_id",
            "gender",
            "first_name",
            "last_name",
            "email",
            "password",
            "dob",
            "phone",
            "cell",
            "picture_large",
            "picture_medium",
            "picture_thumbnail",
            "city",
            "state",
            "state_id",
            "postcode",
            "latitude",
            "longitude",
            "created_at",
        )
        .write
        .format("jdbc")
        .option("url", PG_URL)
        .option("dbtable", PG_TABLE)
        .option("user", PG_USER)
        .option("password", PG_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

def main():

    # Spark session with Iceberg support
    spark = (
    SparkSession.builder
        .appName("IcebergCreateTableTest")

        # Iceberg catalog
        .config("spark.sql.catalog.matchstream", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.matchstream.type", CATALOG_TYPE)
        .config("spark.sql.catalog.matchstream.uri", THRIFT_HIVE_METASTORE)
        .config("spark.sql.catalog.matchstream.warehouse", "s3a://matchstream/")

        # Use S3AFileIO (NOT AWS SDK)
        .config("spark.sql.catalog.matchstream.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")

        # MinIO S3 endpoint settings
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT_URL)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

        .getOrCreate()
)

     # -----------------------------------------------------------
    # 1. Read from Kafka
    # -----------------------------------------------------------
    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )

    # For parsing into structured users:
    value_df = kafka_df.selectExpr("CAST(value AS STRING) AS json_str")

    # -----------------------------------------------------------
    # 2a. Parse JSON → clean users for Postgres
    # -----------------------------------------------------------
    parsed_df = (
        value_df
        .select(from_json(col("json_str"), user_schema).alias("data"))
        .select("data.*")
    )

    clean_df = (
        parsed_df
        .withColumn("dob", to_date(to_timestamp(col("dob"))))
        .withColumn("created_at", to_timestamp(col("created_at")))
        .withColumn("latitude", col("latitude").cast("double"))
        .withColumn("longitude", col("longitude").cast("double"))
    )

    pg_query = (
        clean_df.writeStream
        .foreachBatch(write_to_postgres)
        .option("checkpointLocation", PG_CHECKPOINT)
        .outputMode("update")
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

    bronze_query = (
        bronze_df.writeStream
        .format("iceberg")
        .option("checkpointLocation", BRONZE_CHECKPOINT)
        .toTable(BRONZE_TABLE)  # <- matchstream.bronze.users_raw
    )

    # -----------------------------------------------------------
    # 3. Keep both streams alive
    # -----------------------------------------------------------
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()