from base.spark_app import SparkApp
from base.compaction_engine import CompactionEngine

class CompactBronzeUsersRaw(SparkApp):

    def __init__(self):
        super().__init__("CompactBronzeUsersRaw")
        self.compactor = CompactionEngine(self.spark)

    def run(self):
        table = "bronze.users_raw"
        self.log.info(f"Maintaining table: {table}")

        self.compactor.rewrite_data_files(table)
        self.compactor.rewrite_manifests(table)
        self.compactor.expire_snapshots(table)
        self.compactor.remove_orphans(table)

        self.log.info("Maintenance complete.")