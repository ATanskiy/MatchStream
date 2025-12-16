from jobs.streaming.stream_cdc_bronze import StreamCDCBronze


def test_write_batch_calls_append(mocker, spark):
    # create static dataframe (NOT streaming)
    df = spark.createDataFrame(
        [(1, "a"), (2, "b")],
        ["id", "val"]
    )

    # mock Iceberg writer
    mock_writer = mocker.Mock()
    mocker.patch.object(df, "writeTo", return_value=mock_writer)

    # fake job instance (no __init__)
    job = mocker.Mock(spec=StreamCDCBronze)
    job.table_name = "matchstream.bronze.users"
    job.log = mocker.Mock()

    # call ONLY the batch writer
    StreamCDCBronze.write_batch(job, df, batch_id=1)

    mock_writer.append.assert_called_once()
