from typing import List
from base.compaction_engine import CompactionEngine
from base.spark_app import SparkApp
from configs.jobs.job_config import JobConfig


class CompactSilverAll(SparkApp):
    """Job to compact all tables in the silver namespace."""

    def __init__(self, config: JobConfig) -> None:
        super().__init__("CompactSilverAll", config)
        self.compactor = CompactionEngine(self.spark)

    def run(self) -> None:
        tables: List[str] = [
            row.tableName
            for row in self.spark.sql("SHOW TABLES IN matchstream.silver").collect()
        ]

        for t in tables:
            full_table = f"silver.{t}"
            self.log.info(f"Maintaining table: {full_table}")
            self.compactor.rewrite_data_files(full_table)
            self.compactor.rewrite_manifests(full_table)
            self.compactor.expire_snapshots(full_table)
            self.compactor.remove_orphans(full_table)
        self.log.info("Maintenance for all silver tables complete.")