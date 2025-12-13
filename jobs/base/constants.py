from pathlib import Path

# Base directory (configurable, e.g., via env var if needed)
BASE_DIR = Path("/opt/streaming/jobs")

# DDL configs
DDL_CONFIG_DIR = BASE_DIR / "configs" / "ddl"
NAMESPACES_YAML = DDL_CONFIG_DIR / "namespaces.yaml"
TABLES_YAML = DDL_CONFIG_DIR / "tables.yaml"