from pyspark.sql.types import (
    StructType, StructField,
    StringType, LongType
)

def get_after_schema() -> StructType:
    return StructType([
        StructField("user1", StringType(), False),
        StructField("user2", StringType(), False),
        StructField("created_at", StringType(), True),
    ])

def get_source_schema() -> StructType:
    return StructType([
        StructField("db", StringType(), False),
        StructField("schema", StringType(), False),
        StructField("table", StringType(), False),
        StructField("txId", LongType(), True),
        StructField("lsn", LongType(), True),
    ])

def get_envelope_schema() -> StructType:
    return StructType([
        StructField("schema", StructType(), True),
        StructField(
            "payload",
            StructType([
                StructField("before", get_after_schema(), True),
                StructField("after", get_after_schema(), True),
                StructField("source", get_source_schema(), False),
                StructField("op", StringType(), False),
                StructField("ts_ms", LongType(), True),
            ]),
            True,
        ),
    ])