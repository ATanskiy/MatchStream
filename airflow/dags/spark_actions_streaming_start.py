from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK_CONTAINER = "spark_streaming"

with DAG(
    dag_id="start_actions_streaming",
    description="Run Spark Structured Streaming job safely (no failure on stop)",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["streaming", "spark", "matchstream", "actions_cdc"],
):

    run_streaming = BashOperator(
        task_id="run_users_streaming",
        bash_command=(
            "docker exec {container} "
            "/opt/spark/bin/spark-submit "
            "/opt/streaming/jobs/main.py --job stream_actions_cdc_bronze "
            "|| [ $? -eq 143 ] || [ $? -eq 130 ] || exit $?".format(
                container=SPARK_CONTAINER
            )
        )
    )