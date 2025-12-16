# job_factories.py
from streaming.stream_cdc_bronze import StreamCDCBronze
from schemas.cdc_users import get_envelope_schema as get_users_schema
from schemas.cdc_actions import get_envelope_schema as get_actions_schema
from schemas.cdc_matches import get_envelope_schema as get_matches_schema
from transformers.users_cdc_transform import flatten_cdc as flatten_users
from transformers.actions_cdc_transform import flatten_cdc as flatten_actions
from transformers.matches_cdc_transform import flatten_cdc as flatten_matches


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