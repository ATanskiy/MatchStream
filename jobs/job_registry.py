# job_registry.py
from jobs.ddl.create_schemas_tables import CreateSchemasTablesJob
from job_factories import (
    create_users_cdc_job,
    create_actions_cdc_job,
    create_matches_cdc_job,
    create_compact_bronze_job,
    create_compact_silver_job,
)

JOB_REGISTRY = {
    "compact_bronze": create_compact_bronze_job,
    "compact_silver": create_compact_silver_job,
    "stream_users_cdc_bronze": create_users_cdc_job,
    "stream_actions_cdc_bronze": create_actions_cdc_job,
    "stream_matches_cdc_bronze": create_matches_cdc_job,
    "create_schemas_tables": CreateSchemasTablesJob,
}