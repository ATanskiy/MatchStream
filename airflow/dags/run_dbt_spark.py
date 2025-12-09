from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_CONTAINER = "dbt_spark"
PROJECT_DIR = "/workspace"

default_args = {
    "owner": "matchstream",
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}

with DAG(
    dag_id="run_dbt_spark",
    description="Run dbt models on Spark every 5 minutes",
    start_date=datetime(2025, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    default_args=default_args,
    tags=["dbt", "spark", "matchstream"],
):

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
            (
                echo '--- Running dbt ---';
                docker exec {DBT_CONTAINER} \
                    dbt run --project-dir {PROJECT_DIR}
            ) || true
        """
    )