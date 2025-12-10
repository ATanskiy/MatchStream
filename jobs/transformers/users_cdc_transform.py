from pyspark.sql import functions as F

def flatten_cdc(df):
    pl = F.col("root.payload")

    return df.select(
        F.concat_ws("-", F.col("topic"), F.col("partition"), F.col("offset")).alias("event_id"),
        pl.op.alias("op"),
        pl.ts_ms.alias("cdc_ts_ms"),
        pl.source.db.alias("source_db"),
        pl.source.schema.alias("source_schema"),
        pl.source.table.alias("source_table"),
        pl.source.txId.alias("source_tx_id"),
        pl.after.id.alias("id"),
        pl.after.user_id.alias("user_id"),
        pl.after.gender.alias("gender"),
        pl.after.first_name.alias("first_name"),
        pl.after.last_name.alias("last_name"),
        pl.after.email.alias("email"),
        pl.after.password.alias("password"),
        pl.after.dob.alias("dob_days"),
        pl.after.phone.alias("phone"),
        pl.after.cell.alias("cell"),
        pl.after.picture_large.alias("picture_large"),
        pl.after.picture_medium.alias("picture_medium"),
        pl.after.picture_thumbnail.alias("picture_thumbnail"),
        pl.after.city.alias("city"),
        pl.after.state.alias("state"),
        pl.after.state_id.alias("state_id"),
        pl.after.postcode.alias("postcode"),
        pl.after.latitude.alias("latitude"),
        pl.after.longitude.alias("longitude"),
        F.to_timestamp(pl.after.created_at).alias("created_at"),
        F.current_timestamp().alias("ingested_at"),
    ).where(
        pl.after.isNotNull()
    )