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
        bash_command=f'''
            docker exec {CONTAINER_NAME} sh -c "
                pkill -f /app/user_ingestor_to_writer/main.py \
                && echo '✔ stopped' \
                || echo 'ℹ already stopped'
            " || true
        '''
    )