import io
from typing import Final

import pandas as pd
import requests


class MeteoFranceService:
    """Class to prepare the request and save the data in raw repository"""

    BASE_URL: Final = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive"
    WEATHER_COLUMNS: Final = ["numer_sta", "date", "t", "u", "pres", "tend24"]
    WEATHER_STATIONS: Final = [7015, 7110, 7149, 7190, 7481, 7690, 7630]

    def retrieve_raw_weather_data(self, year: int, start_month: int, end_month: int, dataset_name: str = 'train'):
        raw_weather_df = self.get_weather_data(year, start_month, end_month)
        raw_weather_df.to_csv(f"./raw/{dataset_name}_weather_df.csv", index=False)

    def get_weather_data(self, year: int, start_month: int, end_month: int):
        weather_df = []
        for month in range(start_month, end_month + 1):
            resource_url = f"{self.BASE_URL}/synop.{year}{month:02}.csv.gz"
            response = requests.get(resource_url)
            monthly_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), sep=";",
                                     usecols=self.WEATHER_COLUMNS)
            monthly_df = monthly_df[monthly_df["numer_sta"].isin(self.WEATHER_STATIONS)]
            weather_df.append(monthly_df)
        weather_df = pd.concat(weather_df)
        return weather_df
