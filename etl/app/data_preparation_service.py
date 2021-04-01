from datetime import datetime

import pandas as pd


class DataPreparationService:
    """Class with methods to clean the data and prepare the data"""
    REGEX_DATE = '[0-9]{8}(?:06|12|18)0000'

    def prepare_raw_weather_data(self, dataset_name: str = "train"):
        raw_weather_df = pd.read_csv(f"./raw/{dataset_name}_weather_df.csv")
        curated_weather_df = self._process_weather_features(raw_weather_df)
        curated_weather_df.to_csv(f"./curated/{dataset_name}_weather_df.csv")

    def prepare_raw_rte_data(self, dataset_name: str = "train"):
        raw_rte_df = pd.read_csv(f"./raw/{dataset_name}_rte_df.csv")
        curated_rte_df = self._process_rte_api_short_term(raw_rte_df)
        curated_rte_df.to_csv(f"./curated/{dataset_name}_rte_df.csv")

    def merge_curated_data(self, dataset_name: str = "train"):
        curated_weather_df = pd.read_csv(f"./curated/{dataset_name}_weather_df.csv", index_col="date")
        curated_rte_df = pd.read_csv(f"./curated/{dataset_name}_rte_df.csv", index_col="date_formated")
        merged_df = pd.merge(curated_weather_df, curated_rte_df, left_index=True, right_index=True)
        merged_df.to_csv(f"./refined/{dataset_name}_data.csv", index=True, index_label='datetime')

    def _process_weather_features(self, raw_weather_df: pd.DataFrame):
        for col in raw_weather_df.columns:
            raw_weather_df[col] = pd.to_numeric(raw_weather_df[col], downcast='signed', errors='coerce')

        df_weather_clean = (
            raw_weather_df
                .groupby("date")
                .agg({
                "t": "mean",
                "u": "mean",
                "pres": "mean",
                "tend24": "mean"
            })
        )

        df_weather_clean = (
            df_weather_clean
                .dropna(how="any")
                .astype(int)
        )
        return df_weather_clean

    def _process_rte_api_short_term(self, raw_rte_df: pd.DataFrame):
        df = raw_rte_df[["end_date", "value"]]
        df["date_formated"] = df["end_date"].apply(
            lambda x: datetime.fromisoformat(x).strftime('%Y%m%d%H%M%S')
        )
        df = df.rename({"value": "consumption"}, axis=1)
        idx = df.date_formated.str.match(self.REGEX_DATE)
        df["date_formated"] = df["date_formated"].astype(int)
        df_clean = (
            df[["consumption", "date_formated"]]
                .loc[idx]
                .set_index("date_formated")
        )
        return df_clean
