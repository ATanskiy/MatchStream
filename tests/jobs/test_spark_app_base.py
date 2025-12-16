from base.spark_app import SparkApp
from config.job_config import JobConfig

class DummySparkApp(SparkApp):
    def run(self):
        pass

def test_spark_app_creates_session(mocker):
    mock_config = mocker.Mock(spec=JobConfig)
    mocker.patch(
        "base.spark_session_factory.SparkSessionFactory.build",
        return_value=mocker.Mock()
    )

    app = DummySparkApp("test_app", mock_config)
    assert app.spark is not None
