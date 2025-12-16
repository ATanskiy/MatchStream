from pyspark.sql.types import StructType, StructField, StringType, LongType

def get_source_schema() -> StructType:
    """Standard Debezium source metadata schema."""
    return StructType([
        StructField("db", StringType(), False),
        StructField("schema", StringType(), False),
        StructField("table", StringType(), False),
        StructField("txId", LongType(), True),
        StructField("lsn", LongType(), True),
    ])

def get_envelope_schema(after_schema: StructType) -> StructType:
    """Standard Debezium envelope wrapping any after schema."""
    return StructType([
        StructField("schema", StructType(), True),
        StructField("payload", StructType([
            StructField("before", after_schema, True),
            StructField("after", after_schema, True),
            StructField("source", get_source_schema(), False),
            StructField("op", StringType(), False),
            StructField("ts_ms", LongType(), True),
        ]), True)
    ])