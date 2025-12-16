import sys
from pathlib import Path

# Add user_generator root to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[2]
USER_GENERATOR_ROOT = BASE_DIR / "matchstream_app" / "user_generator"

sys.path.insert(0, str(USER_GENERATOR_ROOT))