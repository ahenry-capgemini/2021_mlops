import os

MODEL_NAME = os.environ.get("MODEL_NAME", "forecast_model")
STAGE = os.environ.get("STAGE", "Production")
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000")
