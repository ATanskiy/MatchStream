from maintenance.compact_bronze_users_raw import CompactBronzeUsersRaw
from maintenance.compact_silver_all import CompactSilverAll
from streaming.stream_users_cdc_bronze import StreamUsersCDCBronze
from jobs.ddl.create_schemas_tables import CreateSchemasTablesJob

JOB_REGISTRY = {
    "compact_bronze_users_raw": CompactBronzeUsersRaw,
    "compact_silver_all": CompactSilverAll,
    "stream_users_cdc_bronze": StreamUsersCDCBronze,
    "create_schemas_tables": CreateSchemasTablesJob,
}