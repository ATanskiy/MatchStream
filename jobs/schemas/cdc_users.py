from pyspark.sql.types import (
    StructType, StructField,
    StringType, LongType, IntegerType, DoubleType
)


def get_after_schema():
    return StructType([
        StructField("id", LongType(), False),
        StructField("user_id", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("password", StringType(), True),
        StructField("dob", IntegerType(), True),
        StructField("phone", StringType(), True),
        StructField("cell", StringType(), True),
        StructField("picture_large", StringType(), True),
        StructField("picture_medium", StringType(), True),
        StructField("picture_thumbnail", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("state_id", StringType(), True),
        StructField("postcode", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("created_at", StringType(), True),
    ])


def get_source_schema():
    return StructType([
        StructField("db", StringType(), False),
        StructField("schema", StringType(), False),
        StructField("table", StringType(), False),
        StructField("txId", LongType(), True),
        StructField("lsn", LongType(), True),
    ])


def get_envelope_schema():
    return StructType([
        StructField("schema", StructType(), True),
        StructField("payload", StructType([
            StructField("before", get_after_schema(), True),
            StructField("after", get_after_schema(), True),
            StructField("source", get_source_schema(), False),
            StructField("op", StringType(), False),
            StructField("ts_ms", LongType(), True),
        ]), True)
    ])