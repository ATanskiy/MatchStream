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
    dag_id="dbt_full_refresh",
    description="Full refresh of all dbt models (recreate all tables)",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["dbt", "spark", "full_refresh", "matchstream"],
):
    
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"""
            echo "--- Installing dbt packages ---"
            docker exec {DBT_CONTAINER} \
                dbt deps --project-dir {PROJECT_DIR}
        """
    )

    full_refresh = BashOperator(
        task_id="dbt_full_refresh",
        bash_command=f"""
            (
                echo "============================"
                echo " RUNNING DBT FULL REFRESH"
                echo "============================"

                docker exec {DBT_CONTAINER} \
                    dbt build --project-dir {PROJECT_DIR} --full-refresh
            )
        """
    )

    generate_docs = BashOperator(
        task_id="generate_dbt_docs",
        bash_command=f"""
            docker exec {DBT_CONTAINER} \
            dbt docs generate --project-dir {PROJECT_DIR}
        """
    )

    fix_docs = BashOperator(
        task_id="fix_docs_database",
        bash_command="""
            docker exec dbt_spark /scripts/fix_dbt_docs_database.sh
        """,
    )
    
    dbt_deps >> full_refresh >> generate_docs >> fix_docs