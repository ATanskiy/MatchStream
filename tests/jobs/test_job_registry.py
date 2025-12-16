from job_registry import JOB_REGISTRY

def test_job_registry_contains_expected_jobs():
    expected = {
        "stream_users_cdc_bronze",
        "stream_actions_cdc_bronze",
        "stream_matches_cdc_bronze",
        "compact_bronze",
        "compact_silver",
        "create_schemas_tables",
    }
    assert expected.issubset(JOB_REGISTRY.keys())
