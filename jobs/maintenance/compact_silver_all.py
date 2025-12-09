from base.spark_app import SparkApp
from base.compaction_engine import CompactionEngine

class CompactSilverAll(SparkApp):

    def __init__(self):
        super().__init__("CompactSilverAll")
        self.compactor = CompactionEngine(self.spark)

    def run(self):
        tables = [
            row.tableName
            for row in self.spark.sql("SHOW TABLES IN matchstream.silver").collect()
        ]

        for t in tables:
            full = f"silver.{t}"
            self.log.info(f"Maintaining table: {full}")
            self.compactor.rewrite_data_files(full)
            self.compactor.rewrite_manifests(full)
            self.compactor.expire_snapshots(full)
            self.compactor.remove_orphans(full)

        self.log.info("Maintenance for all silver tables complete.")