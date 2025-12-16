# tests/jobs/conftest.py
import sys
from pathlib import Path
import pytest
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[2]

# this makes `jobs` importable
JOBS_PKG_ROOT = ROOT / "jobs"

if str(JOBS_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(JOBS_PKG_ROOT))


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest-spark-jobs")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()
