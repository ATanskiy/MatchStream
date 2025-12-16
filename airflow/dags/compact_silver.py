from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK_CONTAINER = "spark_streaming"

with DAG(
    dag_id="compact_silver",
    description="Run full Iceberg compaction for matchstream.silver tables",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "iceberg", "spark", "compaction", "silver"],
):

    run_compaction = BashOperator(
        task_id="run_compaction",
        bash_command=(
            f"docker exec {SPARK_CONTAINER} "
            "/opt/spark/bin/spark-submit "
            "/opt/streaming/jobs/main.py --job compact_silver"
        )
    )