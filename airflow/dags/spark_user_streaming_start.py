from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "spark_streaming"

with DAG(
    dag_id="start_users_streaming",
    description="Start the Spark Structured Streaming job that writes users to Iceberg",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "spark", "streaming"],
):

    run_streaming = BashOperator(
        task_id="run_streaming",
        bash_command=f"""
            docker exec {CONTAINER_NAME} \
            /opt/spark/bin/spark-submit /opt/streaming/jobs/stream_users_bronze.py \
            || true
        """
    )