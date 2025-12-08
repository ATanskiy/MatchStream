from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_generator"

with DAG(
    dag_id="start_user_generator",
    description="Start the user generator inside its running container",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "user_generator"],
):

    run_generator = BashOperator(
        task_id="run_generator",
        bash_command=f"""
            docker exec {CONTAINER_NAME} \
            python -u /app/user_generator/main.py \
            || true
        """
    )