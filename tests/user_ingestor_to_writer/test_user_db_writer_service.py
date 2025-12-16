from matchstream_app.user_ingestor_to_writer.services.user_db_writer_service import UserDbWriterService


def test_service_processes_and_commits(mocker):
    mock_consumer = mocker.Mock()
    mock_mapper = mocker.Mock()
    mock_repo = mocker.Mock()

    mock_consumer.poll.return_value = {
        None: [mocker.Mock(value={"x": 1})]
    }

    mock_mapper.from_event.return_value = "USER"
    mock_repo.upsert.return_value = 1

    service = UserDbWriterService(
        consumer=mock_consumer,
        mapper=mock_mapper,
        repository=mock_repo,
        batch_size=10,
    )

    # stop AFTER first poll
    def stop_after_poll(*args, **kwargs):
        service._running = False
        return {
            None: [mocker.Mock(value={"x": 1})]
        }

    mock_consumer.poll.side_effect = stop_after_poll

    service.run()

    mock_mapper.from_event.assert_called()
    mock_repo.upsert.assert_called()
