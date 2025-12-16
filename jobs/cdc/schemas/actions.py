from pyspark.sql.types import (
    StructType, StructField,
    StringType, LongType
)
from cdc.schemas.common import get_envelope_schema as build_envelope

def get_after_schema() -> StructType:
    return StructType([
        StructField("user_id", StringType(), False),
        StructField("target_id", StringType(), False),
        StructField("action", StringType(), False),
        StructField("created_at", StringType(), True),
    ])

def get_envelope_schema() -> StructType:
    """Full CDC envelope schema for users stream."""
    return build_envelope(get_after_schema())