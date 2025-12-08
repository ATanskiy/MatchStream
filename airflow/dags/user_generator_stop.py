from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "python_user_generator"

with DAG(
    dag_id="stop_user_generator",
    description="Stop the user generator inside its running container",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "user_generator"],
):
    
    stop_generator = BashOperator(
        task_id="stop_generator",
        bash_command=f'''
            docker exec {CONTAINER_NAME} sh -c "
                pkill -f /app/user_generator/main.py \
                && echo '✔ stopped' \
                || echo 'ℹ already stopped'
            " || true
        '''
        )