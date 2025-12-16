from matchstream_app.user_ingestor_to_writer.main import UserIngestorApplication


def test_app_builds(mocker):
    mocker.patch(
        "matchstream_app.user_ingestor_to_writer.main.KafkaConsumer"
    )

    app = UserIngestorApplication()
    service = app.build()

    assert service is not None
