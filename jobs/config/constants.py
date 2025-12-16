from pathlib import Path

# Resolve project root dynamically
# config/constants.py → jobs/config/constants.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# parents[1] = jobs/

DDL_CONFIG_DIR = PROJECT_ROOT / "config" / "ddl"

NAMESPACES_YAML = DDL_CONFIG_DIR / "namespaces.yaml"
TABLES_YAML = DDL_CONFIG_DIR / "tables.yaml"

CATALOG_NAME = "matchstream"
SILVER_SCHEMA = "silver"
BRONZE_SCHEMA = "bronze"

ACTIONS_CDC_TABLE = "actions_cdc"
USERS_CDC_TABLE = "users_cdc"
MATCHES_CDC_TABLE = "matches_cdc"