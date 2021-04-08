from typing import Final
import json

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from discord_webhook import DiscordWebhook

from app.drift_detection_service import DriftDetectionService
from app.settings import DISCORD_WEBHOOK_URL

app = FastAPI()

# set docker to False in local/debug mode
drift_detection_service: Final = DriftDetectionService(docker=True)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/detect-data-drift")
async def detect_data_drift(dataset_name_1: str, dataset_name_2: str):
    results = drift_detection_service.detect_drift(dataset_name_1, dataset_name_2)
    print(results)
    print(results["any_drift"])
    if results["any_drift"]:
        print(results["any_drift"])
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=json.dumps(results))
        webhook.execute()
    return {"response": results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
