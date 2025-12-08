from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_generator"

with DAG(
    dag_id="user_generator_controller",
    description="Start and stop the user generator inside its running container",
    start_date=datetime(2025, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["matchstream", "generator"],
) as dag:

    start_generator = BashOperator(
        task_id="start_user_generator",
        bash_command=(
            f"docker exec {CONTAINER_NAME} "
            "bash -c 'nohup python main.py > /tmp/generator.log 2>&1 & "
            "sleep 1 && pgrep -f \"python main.py\" > /tmp/generator.pid'"
        ),
    )

    stop_generator = BashOperator(
        task_id="stop_user_generator",
        bash_command=(
            f"docker exec {CONTAINER_NAME} "
            "bash -c 'kill $(cat /tmp/generator.pid)'"
        ),
    )
