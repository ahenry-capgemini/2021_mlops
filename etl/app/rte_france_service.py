from typing import Final
import pandas as pd

from app.rte_france_api_client import RTEFranceAPIClient


class RTEFranceService:
    """Class to retrieve RTE data, transform it to pandas dataframe and save it"""

    def __init__(self):
        self.api_client: Final = RTEFranceAPIClient()

    def retrieve_raw_short_term_data(self, year: int, start_month: int, end_month: int, dataset_name: str = "train"):
        data = self.api_client.get_short_term_data(year, start_month, end_month)
        rte_df = pd.DataFrame.from_dict(data)
        rte_df.to_csv(f"./raw/{dataset_name}_rte_df.csv", index=False)
