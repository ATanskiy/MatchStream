from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="matchstream_sanity_check",
    description="Simple test DAG to verify Airflow setup",
    start_date=datetime(2025, 1, 1),
    schedule=None,          # only manual runs; controlled from UI
    catchup=False,
    tags=["matchstream", "test"],
) as dag:

    hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'MatchStream Airflow is alive!'",
    )
