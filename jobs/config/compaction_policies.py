BRONZE_POLICY = {
    "rewrite_data_files": True,
    "rewrite_manifests": False,
    "expire_snapshots_days": 1,
    "remove_orphans": True,
    "target_file_size_bytes": 134217728,
}

SILVER_POLICY = {
    "rewrite_data_files": True,
    "rewrite_manifests": True,
    "expire_snapshots_days": 3,
    "remove_orphans": True,
    "target_file_size_bytes": 134217728,
}