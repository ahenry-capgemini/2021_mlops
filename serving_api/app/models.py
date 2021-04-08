import mlflow
import numpy as np
import pandas as pd
from pydantic import BaseModel

from .settings import MLFLOW_TRACKING_URI, MODEL_NAME, STAGE


class PayLoad(BaseModel):
    t: float
    u: float
    pres: float
    tend24: float


def transaction_to_numpy_array(pl: PayLoad):
    array = np.array([pl.t, pl.u, pl.pres, pl.tend24]).reshape(1, 4)
    df = pd.DataFrame(array, columns=['t', 'u', 'pres', 'tend24'])
    return df


class PredictionReturned(BaseModel):
    prediction: float


class ModelHandler:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{MODEL_NAME}/{STAGE}")
        return model

    def _preprocess(self, pl: PayLoad):
        data = transaction_to_numpy_array(pl)
        return data

    def predict(self, pl: PayLoad):
        pred = self.model.predict(self._preprocess(pl))
        return pred
