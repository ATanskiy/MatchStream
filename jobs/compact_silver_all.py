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
        .appName("IcebergMaintenanceSilverAll")
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
# Load all Iceberg tables from matchstream.silver
# ============================================================
def list_silver_tables(spark):
    print("📋 Fetching list of tables from matchstream.silver...")

    df = spark.sql("SHOW TABLES IN matchstream.silver")
    tables = [row.tableName for row in df.collect()]

    print(f"✔ Found {len(tables)} tables:")
    for t in tables:
        print(f"   - {t}")
    return tables

# ============================================================
# Run full maintenance pipeline on a specific table
# ============================================================
def run_maintenance_for_table(spark, table_full_name):
    print(f"\n==============================")
    print(f"🧊 Running maintenance for table: {table_full_name}")
    print(f"==============================\n")

    rewrite_data_files(spark, table_full_name)
    force_gc(spark)

    rewrite_manifest_files(spark, table_full_name)
    force_gc(spark)

    expire_old_snapshots(spark, table_full_name)
    force_gc(spark)

    remove_orphan_files(spark, table_full_name)

    print("\n📌 Final snapshots:")
    spark.sql(f"""SELECT snapshot_id, parent_id, operation, committed_at
                    FROM matchstream.{table_full_name}.snapshots
                    ORDER BY committed_at DESC""") \
        .show(truncate=False)
    print(f"✅ Finished: {table_full_name}\n")

# ============================================================
# MAIN PIPELINE
# ============================================================
def main():
    spark = create_spark()
    silver_tables = list_silver_tables(spark)

    print("\n=== START ICEBERG MAINTENANCE FOR ALL SILVER TABLES ===\n")

    for table in silver_tables:
        full_table = f"silver.{table}"
        run_maintenance_for_table(spark, full_table)

    print("\n🎉 ALL SILVER TABLES PROCESSED SUCCESSFULLY!\n")

    spark.stop()

if __name__ == "__main__":
    main()