import os

import mlflow
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from .settings import MLFLOW_TRACKING_URI, N_ESTIMATORS, RANDOM_STATE


class TrainingService:
    def __init__(self):
        self.root_path = "/mlflow/projects/data"

    def load_data(self, dataset_name):
        df = pd.read_csv(f"{self.root_path}/{dataset_name}_data.csv")
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y%m%d%H%M%S').dt.day_name()
        df.drop('datetime', axis='columns', inplace=True)
        return df

    @staticmethod
    def split_train_test(data, predict_column):
        """Create Train/Test datasets from input (target and features) data."""
        X = data.drop([predict_column], axis=1)
        Y = data[predict_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.33, random_state=42
        )
        return X_train, X_test, y_train, y_test

    def train(self, dataset_name: str):
        if MLFLOW_TRACKING_URI:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        data = self.load_data(dataset_name)
        X_train, X_test, y_train, y_test = TrainingService.split_train_test(
            data, "consumption"
        )

        with mlflow.start_run(run_name="train"):
            mlflow.log_params(
                {
                    "n_estimators": N_ESTIMATORS,
                    "random_state": RANDOM_STATE,
                }
            )

            columns = X_train.columns.to_list()
            ct = ColumnTransformer(transformers=[('float', StandardScaler(), columns)])

            rf = RandomForestRegressor(
                n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE
            )

            model = Pipeline(steps=[('t', ct), ('m', rf)])

            model.fit(X_train, y_train)
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="forecast_model",
                registered_model_name="forecast_model",
            )
            y_pred = model.predict(X_test)
            metrics_dict = {
                "MAE": metrics.mean_absolute_error(y_test, y_pred),
                "MSE": metrics.mean_squared_error(y_test, y_pred),
                "RMSE": np.sqrt(metrics.mean_squared_error(y_test, y_pred)),
                "MAPE": round(
                    np.mean(100 * (abs(y_pred - y_test.values) / y_test.values)), 2
                ),
            }
            mlflow.log_metrics(metrics_dict)
            mlflow.log_artifact(f"{self.root_path}/{dataset_name}_data.csv")
