from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_ingestor_to_writer"

with DAG(
    dag_id="user_ingestor_controller",
    description="Start and stop the user ingestor inside its running container",
    start_date=datetime(2025, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["matchstream", "ingestor"],
) as dag:

    start_ingestor = BashOperator(
        task_id="start_user_ingestor",
        bash_command=(
            f"docker exec {CONTAINER_NAME} "
            "bash -c 'nohup python /app/user_ingestor_to_writer/main.py > /tmp/ingestor.log 2>&1 & "
            "sleep 1 && pgrep -f \"user_ingestor_to_writer/main.py\" > /tmp/ingestor.pid'"
        ),
    )

    stop_ingestor = BashOperator(
        task_id="stop_user_ingestor",
        bash_command=(
            f"docker exec {CONTAINER_NAME} "
            "bash -c \"pkill -f '/app/user_ingestor_to_writer/main.py'\" ; true"
        ),
    )