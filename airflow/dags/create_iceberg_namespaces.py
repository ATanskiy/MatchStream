from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

SPARK_CONTAINER = "spark_streaming"

with DAG(
    dag_id="create_iceberg_namespaces",
    description="Run Spark DDL job (namespaces + tables) using the OOP job framework",
    start_date=datetime(2025, 1, 1),
    schedule=None,   # run manually
    catchup=False,
    tags=["matchstream", "iceberg", "spark"],
):

    run_schema_job = BashOperator(
        task_id="run_schema_job",
        bash_command=(
            "docker exec spark_streaming "
            "/opt/spark/bin/spark-submit /opt/streaming/jobs/main.py --job create_ddl"
        )
    )
