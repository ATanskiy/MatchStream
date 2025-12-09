import yaml
from base.spark_app import SparkApp

class CreateDDLJob(SparkApp):

    def __init__(self):
        super().__init__("CreateDDLJob")

    # -------------------------
    # Helpers
    # -------------------------
    def load_yaml(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def namespace_exists(self, name):
        df = self.spark.sql("SHOW NAMESPACES IN matchstream")
        namespaces = [row.namespace for row in df.collect()]
        return name in namespaces

    def table_exists(self, namespace, table):
        df = self.spark.sql(f"SHOW TABLES IN matchstream.{namespace}")
        tables = [row.tableName for row in df.collect()]
        return table in tables

    # -------------------------
    # Namespace creation
    # -------------------------
    def create_namespace(self, name, location):
        if self.namespace_exists(name):
            self.log.info(f"Namespace already exists: matchstream.{name}")
            return

        loc = f" LOCATION '{location}'" if location else ""
        self.log.info(f"Creating namespace matchstream.{name}")

        self.spark.sql(f"CREATE NAMESPACE IF NOT EXISTS matchstream.{name}{loc}")

    # -------------------------
    # Table creation
    # -------------------------
    def create_table(self, ns, table, columns, partitions):
        if self.table_exists(ns, table):
            self.log.info(f"Table already exists: matchstream.{ns}.{table}")
            return

        col_defs = ",\n".join([f"{name} {dtype}" for name, dtype in columns.items()])

        part_stmt = ""
        if partitions:
            part_expr = ", ".join(partitions)
            part_stmt = f" PARTITIONED BY ({part_expr})"

        self.log.info(f"Creating table matchstream.{ns}.{table}")

        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS matchstream.{ns}.{table} (
                {col_defs}
            )
            USING iceberg
            {part_stmt}
        """)

    # -------------------------
    # Run logic
    # -------------------------
    def run(self):
        BASE = "/opt/streaming/jobs/configs/ddl"
        ns_config = self.load_yaml(f"{BASE}/namespaces.yaml")
        tables_config = self.load_yaml(f"{BASE}/tables.yaml")

        # Namespaces
        for ns in ns_config["namespaces"]:
            self.create_namespace(ns["name"], ns.get("location"))

        # Tables
        for t in tables_config["tables"]:
            self.create_table(
                ns=t["namespace"],
                table=t["table"],
                columns=t["columns"],
                partitions=t.get("partition_by")
            )

        self.log.info("DDL creation completed.")