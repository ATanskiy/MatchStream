import os
from pyspark.sql import SparkSession

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
THRIFT_HIVE_METASTORE = os.getenv("THRIFT_HIVE_METASTORE")
SPARK_WAREHOUSE_DIR = os.getenv("SPARK_WAREHOUSE_DIR")
CATALOG_TYPE = os.getenv("CATALOG_TYPE")
# --------------------------------------------------------
#  SparkSession with Iceberg + Hive + MinIO
# --------------------------------------------------------
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

print("✓ Spark + Iceberg catalog initialized")

def main():

    spark.sql("""
        CREATE TABLE IF NOT EXISTS matchstream.bronze.users_raw (
            event_id   string,
            json_raw   string,
            inserted_at timestamp
        )
        USING iceberg
        PARTITIONED BY (day(inserted_at))
    """)

    print("✔ Bronze users_raw table created successfully!")

    spark.stop()


if __name__ == "__main__":
    main()