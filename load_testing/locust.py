"""
Run simulate traffic:
locust -f load_testing/locust.py --host http://127.0.0.1:8089
"""

import json
import random

import pandas as pd

from locust import HttpUser, task

dataset = pd.read_csv("test_data.csv", delimiter=",")
dataset[["t", "u", "pres", "tend24"]] = dataset[["t", "u", "pres", "tend24"]].astype(
    float
)
dataset = dataset.to_dict(orient="records")


class DataSent(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        record = random.choice(dataset).copy()
        self.client.post("/predict", json=record)
