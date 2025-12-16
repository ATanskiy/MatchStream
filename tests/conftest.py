import sys
from pathlib import Path
from types import SimpleNamespace

# --------------------------------------------------
# Make matchstream_app importable
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MATCHSTREAM_APP = PROJECT_ROOT / "matchstream_app"
sys.path.insert(0, str(MATCHSTREAM_APP))

# --------------------------------------------------
# Stub psycopg so database layer never loads libpq
# --------------------------------------------------
fake_psycopg = SimpleNamespace(
    connect=lambda *args, **kwargs: None
)

sys.modules["psycopg"] = fake_psycopg
