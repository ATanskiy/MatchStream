def test_user_kafka_producer_send(mocker):
    # Patch config values WHERE THEY ARE USED
    mocker.patch(
        "config.settings.KAFKA_BOOTSTRAP_SERVERS",
        "localhost:9092",
        create=True,
    )
    mocker.patch(
        "config.settings.KAFKA_USERS_TOPIC",
        "users",
        create=True,
    )

    # Patch KafkaProducer
    mock_kafka = mocker.Mock()
    mocker.patch(
        "matchstream_app.user_generator.kafka_producer.kafka_producer.KafkaProducer",
        return_value=mock_kafka,
    )

    from matchstream_app.user_generator.kafka_producer.kafka_producer import (
        UserKafkaProducer,
    )

    producer = UserKafkaProducer(
        servers="localhost:9092",
        topic="users",
    )

    payload = {"a": 1}
    producer.send(payload)

    mock_kafka.send.assert_called_once_with("users", value=payload)