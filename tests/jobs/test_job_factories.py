from job_factories import (
    create_users_cdc_job,
    create_actions_cdc_job,
    create_matches_cdc_job
)
from jobs.streaming.stream_cdc_bronze import StreamCDCBronze
from config.job_config import JobConfig
from base.spark_session_factory import SparkSessionFactory

def test_create_users_cdc_job(mocker):
    # 🔹 IMPORTANT: prevent real Spark session creation
    mocker.patch.object(
        SparkSessionFactory,
        "build",
        return_value=mocker.Mock()
    )

    mock_config = mocker.Mock(spec=JobConfig)
    mock_config.kafka_users_cdc_topic = "users_topic"
    mock_config.checkpoint_users_cdc_bronze = "users_cp"
    mock_config.checkpoint_base = "/chk"

    job = create_users_cdc_job(mock_config)

    assert isinstance(job, StreamCDCBronze)
    assert job.topic == "users_topic"
    assert "users_cdc" in job.table_name
