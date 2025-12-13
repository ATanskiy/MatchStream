from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from base.constants import NAMESPACES_YAML, TABLES_YAML
from base.spark_app import SparkApp
from configs.jobs.job_config import JobConfig


class CreateSchemasTablesJob(SparkApp):
    """Job to create namespaces and tables from YAML configs."""

    def __init__(self, config: JobConfig) -> None:
        super().__init__("CreateDDLJob", config)
        self.namespaces_path: Path = NAMESPACES_YAML
        self.tables_path: Path = TABLES_YAML

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load YAML file safely."""
        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {path}")
        with path.open("r") as f:
            return yaml.safe_load(f)

    def _namespace_exists(self, name: str) -> bool:
        df = self.spark.sql("SHOW NAMESPACES IN matchstream")
        return name in [row.namespace for row in df.collect()]

    def _table_exists(self, namespace: str, table: str) -> bool:
        df = self.spark.sql(f"SHOW TABLES IN matchstream.{namespace}")
        return table in [row.tableName for row in df.collect()]

    def _create_namespace(self, name: str, location: Optional[str] = None) -> None:
        if self._namespace_exists(name):
            self.log.info(f"Namespace already exists: matchstream.{name}")
            return
        loc = f" LOCATION '{location}'" if location else ""
        self.log.info(f"Creating namespace matchstream.{name}")
        self.spark.sql(f"CREATE NAMESPACE IF NOT EXISTS matchstream.{name}{loc}")

    def _create_table(
        self,
        namespace: str,
        table: str,
        columns: Dict[str, str],
        partitions: Optional[List[str]] = None,
    ) -> None:
        if self._table_exists(namespace, table):
            self.log.info(f"Table already exists: matchstream.{namespace}.{table}")
            return
        col_defs = ",\n".join([f"{name} {dtype}" for name, dtype in columns.items()])
        part_stmt = ""
        if partitions:
            part_expr = ", ".join(partitions)
            part_stmt = f" PARTITIONED BY ({part_expr})"
        self.log.info(f"Creating table matchstream.{namespace}.{table}")
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS matchstream.{namespace}.{table} (
                {col_defs})
            USING iceberg
            {part_stmt}""")

    def run(self) -> None:
        ns_config = self._load_yaml(self.namespaces_path)
        tables_config = self._load_yaml(self.tables_path)

        # Namespaces
        for ns in ns_config["namespaces"]:
            self._create_namespace(ns["name"], ns.get("location"))

        # Tables
        for t in tables_config["tables"]:
            self._create_table(
                namespace=t["namespace"],
                table=t["table"],
                columns=t["columns"],
                partitions=t.get("partition_by"),
            )
        self.log.info("DDL creation completed.")