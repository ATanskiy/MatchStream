import pandas as pd
import os

class CitiesLoader:
    _df = None

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

        if CitiesLoader._df is None:
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"US cities file not found: {csv_path}")

            df = pd.read_csv(csv_path)

            # Create weight column for population-based sampling
            df["weight"] = df["population"] / df["population"].sum()

            CitiesLoader._df = df

    def get_random_city(self):
        """Return one city record weighted by population size."""
        row = CitiesLoader._df.sample(weights=CitiesLoader._df["weight"]).iloc[0]
        zip_code = str(row["zips"]).split(" ")[0] if isinstance(row["zips"], str) else None

        return {
            "city": row["city"],
            "state": row["state_name"],
            "state_id": row["state_id"],
            "postcode": zip_code,
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
        }