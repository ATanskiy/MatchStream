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

    def rewrite_data_files(self, table: str, target_file_size_bytes: int = 134217728) -> None:
        """Rewrite data files for the given table using binpack strategy."""
        print(f"📦 Compacting {table} (target={target_file_size_bytes} bytes)...")
        self.spark.sql(f"""
            CALL matchstream.system.rewrite_data_files(
                table => '{table}',
                strategy => 'binpack',
                options => map('target-file-size-bytes', '{target_file_size_bytes}'))
        """).show(truncate=False)
        self._gc()

    def rewrite_manifests(self, table: str) -> None:
        """Rewrite manifests for the given table."""
        print(f"🗂 Rewriting manifests for {table}...")
        self.spark.sql(f"CALL matchstream.system.rewrite_manifests('{table}')").show()
        self._gc()

    def expire_snapshots(self, table: str, older_than_days: int = 3) -> None:
        """Expire snapshots older than N days for the given table."""
        ts = (datetime.utcnow() - timedelta(days=older_than_days)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Expiring snapshots older than {ts} (>{older_than_days} days)")
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