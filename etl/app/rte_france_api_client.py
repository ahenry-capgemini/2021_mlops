from datetime import datetime, timezone
from typing import Final

import requests


class RTEFranceAPIClient:
    """Class to connect to RTE API and create the payload based on parameters"""

    BASE_URL: Final = "https://digital.iservices.rte-france.com/open_api/consumption/v1"

    def __init__(self):
        self.token = self._get_oauth_token()

    def get_short_term_data(self, year: int, start_month: int, end_month: int):
        url = f"{self.BASE_URL}/short_term"
        # handling end of year specific case
        if end_month == 13:
            end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc).isoformat()
        else:
            end_date = datetime(year, end_month, 1, tzinfo=timezone.utc).isoformat(),
        payload_st = {
            "type": "REALISED",
            "start_date": datetime(year, start_month, 1, tzinfo=timezone.utc).isoformat(),
            "end_date": end_date,
        }
        response = self._get(url, payload_st)
        data = response.json()["short_term"][0]['values']
        return data

    def _get(self, url, params=None) -> requests.Response:
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, params, headers=headers)
        response.raise_for_status()
        return response

    def _get_oauth_token(self):
        b64 = "MWE0YTY3NjAtODYxMC00NmIwLWE2YzgtOTllZGZiMjk3NjVkOjdmODJjYzI5LTcwNGUtNGJlYi05ODkyLWI3NjFiYTNkZWI0NA=="
        oauth_url = "http://digital.iservices.rte-france.com/token/oauth"
        headers = {
            "Authorization": f"Basic {b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_response = requests.post(oauth_url, headers=headers)
        token_response.raise_for_status()
        return token_response.json()["access_token"]
