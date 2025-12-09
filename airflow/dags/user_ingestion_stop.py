from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_ingestor_to_writer"

with DAG(
    dag_id="stop_user_ingestion",
    description="Stop the user ingestion",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "ingestor"],
):

    stop_ingestor = BashOperator(
        task_id="stop_ingestor",
        bash_command=f"""
            (
                echo '--- Checking running processes ---';
                docker exec {CONTAINER_NAME} ps -ef | grep user_ingestor_to_writer | grep -v grep \
                    || echo 'No matching process';

                echo '--- Attempting kill ---';
                docker exec {CONTAINER_NAME} pkill -f /app/user_ingestor_to_writer/main.py 2>&1 \
                    && echo '✔ Process killed' \
                    || echo 'ℹ No running process';
            ) || true
        """
    )