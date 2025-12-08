from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

CONTAINER_NAME = "spark_streaming"

with DAG(
    dag_id="stop_users_streaming",
    description="Stop the Spark Structured Streaming ingestion job",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["matchstream", "spark", "streaming"],
):

    stop_streaming = BashOperator(
        task_id="stop_streaming",
        bash_command=f'''
            docker exec {CONTAINER_NAME} sh -c "
                pkill -f org.apache.spark.deploy.SparkSubmit \
                && echo '✔ Spark Streaming stopped' \
                || echo 'ℹ Spark Streaming was not running'
            " || true
        '''
    )