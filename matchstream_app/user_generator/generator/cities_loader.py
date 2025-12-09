import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class CitiesLoader:
    _df = None

    def __init__(self, csv_path):
        if CitiesLoader._df is None:
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"US cities file not found: {csv_path}")

            df = pd.read_csv(csv_path)
            df["weight"] = df["population"] / df["population"].sum()
            CitiesLoader._df = df
            logger.info(f"Loaded {len(df)} cities into memory")

    def get_random_city(self):
        row = CitiesLoader._df.sample(weights=CitiesLoader._df["weight"]).iloc[0]
        zips = row["zips"]
        postcode = str(zips).split(" ")[0] if isinstance(zips, str) else None

        return {
            "city": row["city"],
            "state": row["state_name"],
            "state_id": row["state_id"],
            "postcode": postcode,
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
        }