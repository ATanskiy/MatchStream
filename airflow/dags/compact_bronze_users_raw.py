from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK_CONTAINER = "spark_streaming"

with DAG(
    dag_id="compact_bronze_users_raw",
    description="Run Iceberg compaction for matchstream.bronze.users_raw",
    start_date=datetime(2025, 1, 1),
    schedule=None,   # run manually, like your example
    catchup=False,
    tags=["matchstream", "iceberg", "spark", "compaction"],
):

    run_compaction = BashOperator(
        task_id="run_compaction",
        bash_command=(
            "docker exec spark_streaming "
            "/opt/spark/bin/spark-submit /opt/streaming/jobs/compact_bronze_users_raw.py"
        )
    )