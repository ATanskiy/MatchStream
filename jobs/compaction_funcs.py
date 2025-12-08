import time
from datetime import datetime, timedelta

# ============================================================
# Helper: Force Java GC between maintenance actions
# ============================================================
def force_gc(spark):
    print("→ Running JVM GC...")
    spark.sparkContext._jvm.System.gc()
    time.sleep(3)
    print("✓ GC complete\n")

# ============================================================
# 1. Rewrite Data Files (Compaction)
# ============================================================
def rewrite_data_files(spark, table):
    print(f"📦 Step 1: Rewriting data files on {table}...")
    df = spark.sql(f"""
        CALL matchstream.system.rewrite_data_files(
          table => '{table}',
          strategy => 'binpack',
          options => map(
            'min-input-files', '1',
            'target-file-size-bytes', '134217728'   -- 128 MB))
    """)
    df.show(truncate=False)
    print("✓ rewrite_data_files completed\n")

# ============================================================
# 2. Rewrite Manifest Files
# ============================================================
def rewrite_manifest_files(spark, table):
    print(f"🗂️ Step 2: Rewriting manifest files on {table}...")
    df = spark.sql(f"""CALL matchstream.system.rewrite_manifests('{table}')""")
    df.show(truncate=False)
    print("✓ rewrite_manifest_files completed\n")

# ============================================================
# 3. Expire Old Snapshots
# ============================================================
def expire_old_snapshots(spark, table):
    print(f"🕒 Step 3: Expiring old snapshots on {table}...")

    # Calculate timestamp (UTC)
    threshold = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    print(f"Expiring snapshots older than: {threshold}")

    df = spark.sql(f"""CALL matchstream.system.expire_snapshots(
                        table => '{table}',
                        older_than => TIMESTAMP '{threshold}')""")
    df.show(truncate=False)
    print("✓ expire_old_snapshots completed\n")

# ============================================================
# 4. Remove Orphan Files
# ============================================================
def remove_orphan_files(spark, table):
    print(f"🧹 Step 4: Removing orphan files on {table}...")
    df = spark.sql(f"""CALL matchstream.system.remove_orphan_files('{table}')""")
    df.show(truncate=False)
    print("✓ remove_orphan_files completed\n")