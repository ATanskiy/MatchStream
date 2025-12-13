from base.compaction_engine import CompactionEngine
from base.spark_app import SparkApp
from configs.jobs.job_config import JobConfig


class CompactBronzeUsersRaw(SparkApp):
    """Job to compact the bronze.users_raw table."""

    def __init__(self, config: JobConfig) -> None:
        super().__init__("CompactBronzeUsersRaw", config)
        self.compactor = CompactionEngine(self.spark)
        self.table = "bronze.users_raw"

    def run(self) -> None:
        self.log.info(f"Maintaining table: {self.table}")
        self.compactor.rewrite_data_files(self.table)
        self.compactor.rewrite_manifests(self.table)
        self.compactor.expire_snapshots(self.table)
        self.compactor.remove_orphans(self.table)
        self.log.info("Maintenance complete.")