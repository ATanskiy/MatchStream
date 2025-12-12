from datetime import datetime, timedelta
import time

class CompactionEngine:
    """Engine for compacting and maintaining Iceberg tables."""

    def __init__(self, spark) -> None:
        self.spark = spark

    def _gc(self) -> None:
        """Trigger JVM garbage collection with a short delay."""
        self.spark.sparkContext._jvm.System.gc()
        time.sleep(2)

    def rewrite_data_files(self, table: str) -> None:
        """Rewrite data files for the given table using binpack strategy."""
        print(f"📦 Compacting {table}...")
        self.spark.sql(f"""
            CALL matchstream.system.rewrite_data_files(
                table => '{table}',
                strategy => 'binpack',
                options => map('target-file-size-bytes', '134217728'))
        """).show(truncate=False)
        self._gc()

    def rewrite_manifests(self, table: str) -> None:
        """Rewrite manifests for the given table."""
        print(f"🗂 Rewriting manifests for {table}...")
        self.spark.sql(f"CALL matchstream.system.rewrite_manifests('{table}')").show()
        self._gc()

    def expire_snapshots(self, table: str) -> None:
        """Expire snapshots older than 3 days for the given table."""
        ts = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Expiring snapshots older than {ts}")
        self.spark.sql(f"""
            CALL matchstream.system.expire_snapshots(
                table => '{table}', older_than => TIMESTAMP '{ts}')
        """).show()
        self._gc()

    def remove_orphans(self, table: str) -> None:
        """Remove orphan files for the given table."""
        print(f"🧹 Removing orphan files for {table}...")
        self.spark.sql(f"CALL matchstream.system.remove_orphan_files('{table}')").show()
        self._gc()