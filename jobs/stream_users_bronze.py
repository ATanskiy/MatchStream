import os, sys, signal, traceback
sys.path.append("/opt/streaming")

from pyspark.sql import SparkSession
from configs.spark_streaming.configs import (
    BRONZE_CHECKPOINT,
    KAFKA_TOPIC_USERS,
    BRONZE_TABLE_USERS,
)

# -------------------------------------------------------------------
# ENV VARS
# -------------------------------------------------------------------
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
THRIFT_HIVE_METASTORE = os.getenv("THRIFT_HIVE_METASTORE")
CATALOG_TYPE = os.getenv("CATALOG_TYPE")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


# -------------------------------------------------------------------
# SPARK SESSION
# -------------------------------------------------------------------
def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("MatchStreamUsersIngestion")
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.matchstream", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.matchstream.type", CATALOG_TYPE)
        .config("spark.sql.catalog.matchstream.uri", THRIFT_HIVE_METASTORE)
        .config("spark.sql.catalog.matchstream.warehouse", "s3a://matchstream/")
        .config("spark.sql.catalog.matchstream.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT_URL)
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


# ------------------------------------------------------------
# WRITE TO ICEBERG (foreachBatch)
# ------------------------------------------------------------
def write_to_iceberg(df, batch_id):
    try:
        row_count = df.count()
        print("=" * 80)
        print(f"🔥 Writing batch {batch_id} → Iceberg table: {BRONZE_TABLE_USERS}")
        print(f"Rows: {row_count}")
        print("=" * 80)

        if row_count > 0:
            (
                df.writeTo(BRONZE_TABLE_USERS)
                .append()
            )

    except Exception:
        print("❌ ERROR in write_to_iceberg()")
        traceback.print_exc()


# -------------------------------------------------------------------
# SHUTDOWN HANDLER
# -------------------------------------------------------------------
_ACTIVE_QUERIES = []
_RUNNING = True
_SPARK = None


def _shutdown(*args):
    global _RUNNING
    print("\n🛑 Graceful shutdown signal received")
    _RUNNING = False

    for q in _ACTIVE_QUERIES:
        try:
            print(f"➡ Stopping query: {q.name}")
            q.stop()
        except:
            traceback.print_exc()

    if _SPARK:
        try:
            print("➡ Stopping Spark session…")
            _SPARK.stop()
        except:
            traceback.print_exc()

    print("✨ Shutdown complete.")
    sys.exit(0)


# ------------------------------------------------------------
# MAIN JOB
# ------------------------------------------------------------
def main():
    global _SPARK, _ACTIVE_QUERIES

    # handle termination
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    spark = create_spark_session()
    _SPARK = spark

    # --------------------------------------------------------
    # STREAM READ FROM KAFKA
    # --------------------------------------------------------
    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC_USERS)
        .option("startingOffsets", "earliest")
        .load()
    )

    value_df = kafka_df.selectExpr("CAST(value AS STRING) AS json_str")

    # --------------------------------------------------------
    # BRONZE STRUCTURE
    # --------------------------------------------------------
    bronze_df = value_df.selectExpr(
        "uuid() AS event_id",
        "json_str AS json_raw",
        "current_timestamp() AS inserted_at"
    )

    # --------------------------------------------------------
    # STREAM WRITE → ICEBERG
    # --------------------------------------------------------
    bronze_query = (
        bronze_df.writeStream
        .foreachBatch(write_to_iceberg)
        .option("checkpointLocation", BRONZE_CHECKPOINT)
        .queryName("bronze_users_raw_writer")
        .trigger(processingTime="10 seconds")
        .start()
    )

    _ACTIVE_QUERIES.append(bronze_query)

    print("🔥 Bronze stream started! Writing to Iceberg via foreachBatch…")

    # keep process alive
    while _RUNNING:
        spark.streams.awaitAnyTermination(5)

if __name__ == "__main__":
    main()