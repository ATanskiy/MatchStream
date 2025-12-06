from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType
)

USER_SCHEMA = StructType([
    StructField("user_id", StringType(), False),

    StructField("gender", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("password", StringType(), True),

    StructField("dob", StringType(), True),

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

BRONZE_CHECKPOINT = "s3a://default/checkpoints/bronze_users"
BRONZE_TABLE_USERS = "matchstream.bronze.users_raw"
KAFKA_TOPIC_USERS = "users"