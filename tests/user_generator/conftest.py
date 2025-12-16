import sys
from pathlib import Path

HERE = Path(__file__).resolve()

REPO_ROOT = HERE.parents[2]
MATCHSTREAM_APP_ROOT = REPO_ROOT / "matchstream_app"
USER_GENERATOR_ROOT = MATCHSTREAM_APP_ROOT / "user_generator"

for path in (MATCHSTREAM_APP_ROOT, USER_GENERATOR_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))