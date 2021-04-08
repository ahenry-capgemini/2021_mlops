from fastapi import FastAPI, Response

from .models import ModelHandler, PayLoad, PredictionReturned
from .monitoring import instrumentator

app = FastAPI()

instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.get("/")
def read_root():
    return "Model API"


@app.post("/predict", response_model=PredictionReturned)
async def predict(data: PayLoad, response: Response):
    model = ModelHandler()
    prediction = model.predict(data)
    response.headers["prediction"] = str(prediction[0])
    return PredictionReturned(prediction=prediction)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
