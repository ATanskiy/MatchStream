from maintenance.compact_bronze_users_raw import CompactBronzeUsersRaw
from maintenance.compact_silver_all import CompactSilverAll
from streaming.stream_users_bronze import StreamUsersBronze
from ddl.create_ddl_job import CreateDDLJob

JOB_REGISTRY = {
    "compact_bronze_users_raw": CompactBronzeUsersRaw,
    "compact_silver_all": CompactSilverAll,
    "stream_users_bronze": StreamUsersBronze,
    "create_ddl": CreateDDLJob,
}