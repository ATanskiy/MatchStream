from jobs.streaming.stream_cdc_bronze import StreamCDCBronze
from cdc.schemas.users import get_envelope_schema as get_users_schema
from cdc.schemas.actions import get_envelope_schema as get_actions_schema
from cdc.schemas.matches import get_envelope_schema as get_matches_schema
from cdc.transforms.users import flatten_cdc as flatten_users
from cdc.transforms.actions import flatten_cdc as flatten_actions
from cdc.transforms.matches import flatten_cdc as flatten_matches
from config.job_config import JobConfig
from base.spark_app import SparkApp


def create_users_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_users_cdc_topic,
        schema_getter=get_users_schema,
        transform_fn=flatten_users,
        table_name="matchstream.bronze.users_cdc",
        checkpoint_suffix=config.checkpoint_users_cdc_bronze,
    )


def create_actions_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_actions_cdc_topic,
        schema_getter=get_actions_schema,
        transform_fn=flatten_actions,
        table_name="matchstream.bronze.actions_cdc",
        checkpoint_suffix=config.checkpoint_actions_cdc_bronze,
    )


def create_matches_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_matches_cdc_topic,
        schema_getter=get_matches_schema,
        transform_fn=flatten_matches,
        table_name="matchstream.bronze.matches_cdc",
        checkpoint_suffix=config.checkpoint_matches_cdc_bronze,
    )