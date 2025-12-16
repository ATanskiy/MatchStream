def test_kafka_send(mocker):
    mock_producer_cls = mocker.patch(
        "matchstream_app.user_generator.kafka_producer.kafka_producer.KafkaProducer"
    )
    mock_producer = mock_producer_cls.return_value

    from matchstream_app.user_generator.kafka_producer.kafka_producer import (
        UserKafkaProducer,
    )

    producer = UserKafkaProducer()
    producer.send({"id": 1})

    mock_producer.send.assert_called_once()