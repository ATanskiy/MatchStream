from datetime import datetime, timedelta
import time

class CompactionEngine:

    def __init__(self, spark):
        self.spark = spark

    def _gc(self):
        self.spark.sparkContext._jvm.System.gc()
        time.sleep(2)

    def rewrite_data_files(self, table):
        print(f"📦 Compacting {table}...")
        self.spark.sql(f"""
            CALL matchstream.system.rewrite_data_files(
                table => '{table}',
                strategy => 'binpack',
                options => map('target-file-size-bytes', '134217728'))
        """).show(truncate=False)
        self._gc()

    def rewrite_manifests(self, table):
        print(f"🗂 Rewriting manifests for {table}...")
        self.spark.sql(f"CALL matchstream.system.rewrite_manifests('{table}')").show()
        self._gc()

    def expire_snapshots(self, table):
        ts = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Expiring snapshots older than {ts}")
        self.spark.sql(f"""
            CALL matchstream.system.expire_snapshots(
                table => '{table}', older_than => TIMESTAMP '{ts}')
        """).show()
        self._gc()

    def remove_orphans(self, table):
        print(f"🧹 Removing orphan files for {table}...")
        self.spark.sql(f"CALL matchstream.system.remove_orphan_files('{table}')").show()
        self._gc()