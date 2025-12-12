from pyspark.sql import SparkSession
from configs.jobs.job_config import JobConfig

class SparkSessionFactory:
    """Factory for building Spark sessions with Iceberg configurations."""

    @staticmethod
    def build(config: JobConfig, app_name: str) -> SparkSession:
        return (
            SparkSession.builder
            .appName(app_name)
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.matchstream", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.matchstream.type", config.catalog_type)
            .config("spark.sql.catalog.matchstream.uri", config.hive_metastore)
            .config("spark.sql.catalog.matchstream.warehouse", "s3a://matchstream/")
            .config("spark.sql.catalog.matchstream.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")
            .config("spark.hadoop.fs.s3a.endpoint", config.s3_endpoint)
            .config("spark.hadoop.fs.s3a.access.key", config.aws_key)
            .config("spark.hadoop.fs.s3a.secret.key", config.aws_secret)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .getOrCreate()
        )