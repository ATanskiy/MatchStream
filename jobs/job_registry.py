from ddl.create_schemas_tables import CreateSchemasTablesJob
from maintenance.compact_bronze_users_raw import CompactBronzeUsersRaw
from maintenance.compact_silver_all import CompactSilverAll
from streaming.stream_users_cdc_bronze import StreamUsersCDCBronze
from streaming.stream_actions_cdc_bronze import StreamActionsCDCBronze
from streaming.stream_matches_cdc_bronze import StreamMatchesCDCBronze

JOB_REGISTRY = {
    "compact_bronze_users_raw": CompactBronzeUsersRaw,
    "compact_silver_all": CompactSilverAll,
    "stream_users_cdc_bronze": StreamUsersCDCBronze,
    "stream_actions_cdc_bronze": StreamActionsCDCBronze,
    "stream_matches_cdc_bronze": StreamMatchesCDCBronze,
    "create_schemas_tables": CreateSchemasTablesJob,
}