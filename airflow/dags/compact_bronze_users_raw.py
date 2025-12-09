from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK_CONTAINER = "spark_streaming"

with DAG(
    dag_id="compact_bronze_users_raw",
    description="Run Iceberg compaction for matchstream.bronze.users_raw",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "iceberg", "spark", "compaction"],
):

    run_compaction = BashOperator(
        task_id="run_compaction",
        bash_command=(
            f"docker exec {SPARK_CONTAINER} "
            "/opt/spark/bin/spark-submit "
            "/opt/streaming/jobs/main.py --job compact_bronze_users_raw"
        ) + " || true"
    )