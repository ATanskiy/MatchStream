from pyspark.sql.types import (
    StructType, StructField,
    StringType, LongType, IntegerType, DoubleType
)
from cdc.schemas.common import get_envelope_schema as build_envelope

def get_after_schema() -> StructType:
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

def get_envelope_schema() -> StructType:
    """Full CDC envelope schema for users stream."""
    return build_envelope(get_after_schema())