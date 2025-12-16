from typing import Dict, List
from base.compaction_engine import CompactionEngine
from base.spark_app import SparkApp
from config.job_config import JobConfig


class CompactNamespace(SparkApp):
    """Compacts and maintains all Iceberg tables in a given namespace using a policy."""

    def __init__(self, config: JobConfig, namespace: str, policy: Dict) -> None:
        super().__init__(f"Compact{namespace.capitalize()}", config)
        self.namespace = namespace
        self.policy = policy
        self.compactor = CompactionEngine(self.spark)

    def _list_tables(self) -> List[str]:
        rows = self.spark.sql(f"SHOW TABLES IN matchstream.{self.namespace}").collect()
        # Spark returns columns like: namespace, tableName, isTemporary
        return [r.tableName for r in rows if not r.isTemporary]

    def run(self) -> None:
        tables = self._list_tables()
        self.log.info(f"Found {len(tables)} tables in matchstream.{self.namespace}")

        for t in tables:
            full_table = f"{self.namespace}.{t}"
            self.log.info(f"🧹 Maintaining table: {full_table}")

            if self.policy.get("rewrite_data_files", False):
                self.compactor.rewrite_data_files(
                    full_table,
                    target_file_size_bytes=int(self.policy.get("target_file_size_bytes", 134217728)),
                )

            if self.policy.get("rewrite_manifests", False):
                self.compactor.rewrite_manifests(full_table)

            expire_days = self.policy.get("expire_snapshots_days", None)
            if expire_days is not None:
                self.compactor.expire_snapshots(full_table, older_than_days=int(expire_days))

            if self.policy.get("remove_orphans", False):
                self.compactor.remove_orphans(full_table)

        self.log.info(f"✅ Maintenance for all {self.namespace} tables complete.")
