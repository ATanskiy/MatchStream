# job_registry.py
from ddl.create_schemas_tables import CreateSchemasTablesJob
from maintenance.compact_bronze_users_raw import CompactBronzeUsersRaw
from maintenance.compact_silver_all import CompactSilverAll
from job_factories import (
    create_users_cdc_job,
    create_actions_cdc_job,
    create_matches_cdc_job,
)

JOB_REGISTRY = {
    "compact_bronze_users_raw": CompactBronzeUsersRaw,
    "compact_silver_all": CompactSilverAll,
    "stream_users_cdc_bronze": create_users_cdc_job,
    "stream_actions_cdc_bronze": create_actions_cdc_job,
    "stream_matches_cdc_bronze": create_matches_cdc_job,
    "create_schemas_tables": CreateSchemasTablesJob,
}