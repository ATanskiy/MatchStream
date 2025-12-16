import sys
from pathlib import Path

# --------------------------------------------------
# Make script-style imports work
# --------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
USER_INGESTOR_ROOT = (
    REPO_ROOT / "matchstream_app" / "user_ingestor_to_writer"
)

sys.path.insert(0, str(USER_INGESTOR_ROOT))