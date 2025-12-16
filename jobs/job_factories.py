from jobs.streaming.stream_cdc_bronze import StreamCDCBronze
from cdc.schemas.users import get_envelope_schema as get_users_schema
from cdc.schemas.actions import get_envelope_schema as get_actions_schema
from cdc.schemas.matches import get_envelope_schema as get_matches_schema
from cdc.transforms.users import flatten_cdc as flatten_users
from cdc.transforms.actions import flatten_cdc as flatten_actions
from cdc.transforms.matches import flatten_cdc as flatten_matches
from jobs.maintenance.compact_namespace import CompactNamespace
from config.compaction_policies import BRONZE_POLICY, SILVER_POLICY
from config.constants import (
    BRONZE_SCHEMA, 
    SILVER_SCHEMA, 
    CATALOG_NAME, 
    ACTIONS_CDC_TABLE, 
    USERS_CDC_TABLE, 
    MATCHES_CDC_TABLE
)

def create_users_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_users_cdc_topic,
        schema_getter=get_users_schema,
        transform_fn=flatten_users,
        table_name=f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{USERS_CDC_TABLE}",
        checkpoint_suffix=config.checkpoint_users_cdc_bronze,
    )

def create_actions_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_actions_cdc_topic,
        schema_getter=get_actions_schema,
        transform_fn=flatten_actions,
        table_name=f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{ACTIONS_CDC_TABLE}",
        checkpoint_suffix=config.checkpoint_actions_cdc_bronze,
    )

def create_matches_cdc_job(config):
    return StreamCDCBronze(
        config=config,
        topic=config.kafka_matches_cdc_topic,
        schema_getter=get_matches_schema,
        transform_fn=flatten_matches,
        table_name=f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{MATCHES_CDC_TABLE}",
        checkpoint_suffix=config.checkpoint_matches_cdc_bronze,
    )

def create_compact_bronze_job(config):
    return CompactNamespace(config=config, namespace=BRONZE_SCHEMA, policy=BRONZE_POLICY)

def create_compact_silver_job(config):
    return CompactNamespace(config=config, namespace=SILVER_SCHEMA, policy=SILVER_POLICY)