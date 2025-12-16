from pyspark.sql import DataFrame, functions as F


def flatten_cdc(df: DataFrame) -> DataFrame:
    """Flatten matches CDC JSON structure into a flat DataFrame."""
    pl = F.col("root.payload")

    return (
        df.select(
            F.concat_ws("-", F.col("topic"), F.col("partition"), F.col("offset"))
                .alias("event_id"),
            pl.op.alias("op"),
            pl.ts_ms.alias("cdc_ts_ms"),
            pl.source.db.alias("source_db"),
            pl.source.schema.alias("source_schema"),
            pl.source.table.alias("source_table"),
            pl.source.txId.alias("source_tx_id"),
            pl.after.user1.alias("user1"),
            pl.after.user2.alias("user2"),
            F.to_timestamp(pl.after.created_at).alias("created_at"),
            F.current_timestamp().alias("ingested_at"),
        )
        .where(pl.after.isNotNull())
    )