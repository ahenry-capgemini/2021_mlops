from fastapi import FastAPI
from typing import Optional

from .train import TrainingService

app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to the training API"


@app.get("/train")
def train(dataset_name: Optional[str] = "train"):
    service = TrainingService()
    service.train(dataset_name)
    return {"response": "ok"}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
