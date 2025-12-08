from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_ingestor_to_writer"

with DAG(
    dag_id="start_user_ingestion",
    description="Start the user ingestion continuously until manually stopped",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "ingestor"],
):

    run_ingestor = BashOperator(
        task_id="run_ingestor",
        bash_command=(
            f"docker exec {CONTAINER_NAME} "
            "python -u /app/user_ingestor_to_writer/main.py"
        )
    )