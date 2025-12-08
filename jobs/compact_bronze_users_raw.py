import os
from pyspark.sql import SparkSession
from jobs.compaction_funcs import (
    rewrite_data_files,
    rewrite_manifest_files,
    expire_old_snapshots,
    remove_orphan_files,
    force_gc
)

# ============================================================
# Spark Session Builder
# ============================================================
def create_spark():
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    THRIFT_HIVE_METASTORE = os.getenv("THRIFT_HIVE_METASTORE")
    CATALOG_TYPE = os.getenv("CATALOG_TYPE", "hive")

    spark = (
        SparkSession.builder
        .appName("IcebergMaintenanceBronzeUsersRaw")
        .config("spark.sql.catalog.matchstream", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.matchstream.type", CATALOG_TYPE)
        .config("spark.sql.catalog.matchstream.uri", THRIFT_HIVE_METASTORE)
        .config("spark.sql.catalog.matchstream.warehouse", "s3a://matchstream/")
        .config("spark.sql.catalog.matchstream.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT_URL)
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        .getOrCreate()
    )

    print("\n✓ Spark + Iceberg initialized\n")
    return spark

# ============================================================
# MAIN PIPELINE
# ============================================================
def main():
    spark = create_spark()

    # Which table we maintain
    table = "bronze.users_raw"

    print("\n=== START ICEBERG MAINTENANCE PIPELINE ===\n")

    # Step 1: Data compaction
    rewrite_data_files(spark, table)
    force_gc(spark)

    # Step 2: Manifest optimization
    rewrite_manifest_files(spark, table)
    force_gc(spark)

    # Step 3: Snapshot expiration
    expire_old_snapshots(spark, table)
    force_gc(spark)

    # Step 4: Remove orphan files
    remove_orphan_files(spark, table)

    print("\n=== FINAL SNAPSHOTS ===")
    spark.sql(f"""
        SELECT snapshot_id, parent_id, operation, committed_at
        FROM matchstream.{table}.snapshots
        ORDER BY committed_at DESC
    """).show(truncate=False)

    print("\n✅ ALL MAINTENANCE TASKS COMPLETED SUCCESSFULLY\n")
    spark.stop()

if __name__ == "__main__":
    main()