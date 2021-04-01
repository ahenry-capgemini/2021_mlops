from datetime import date
from typing import Final, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from discord_webhook import DiscordWebhook

from app.data_preparation_service import DataPreparationService
from app.great_expectations_service import GreatExpectationsService
from app.meteo_france_service import MeteoFranceService
from app.rte_france_service import RTEFranceService
from app.settings import DISCORD_WEBHOOK_URL

GE_STATIC_ROOT: Final = "/great-expectations"

app = FastAPI()
# app.mount(GE_STATIC_ROOT, StaticFiles(directory="./great_expectations/data_docs/local_site"),
#           name="great-expectations-local-site")

meteo_france_service: Final = MeteoFranceService()
rte_france_service: Final = RTEFranceService()
great_expectations_service: Final = GreatExpectationsService()
data_preparation_service: Final = DataPreparationService()


@app.get("/")
def read_root():
    """GET the API documentation of all endpoints"""
    return RedirectResponse("/docs")


@app.get(GE_STATIC_ROOT)
def get_ge_docs():
    """GET great_expectations documentation"""
    return RedirectResponse(f"{GE_STATIC_ROOT}/index.html")


@app.get("/retrieve-raw-weather-data")
def retrieve_raw_weather_data(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    """GET weather data based on parameters: Year, start_month, end_month and dataset name"""

    # Query validation
    if year < 1996:
        raise HTTPException(status_code=400, detail="Cannot query data before 1996")
    if start_month > end_month:
        raise HTTPException(status_code=400, detail="Bad parameter : start month > end month")
    today = date.today()
    if year > today.year or (year == today.year and end_month > today.month):
        raise HTTPException(status_code=400, detail="Cannot query data into the future")

    # retrieving and saving the data
    try:
        meteo_france_service.retrieve_raw_weather_data(year, start_month, end_month, dataset_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"response": "ok"}


@app.get("/retrieve-raw-rte-data")
def retrieve_raw_rte_data(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    """GET rte france consumption data based on parameters: Year, start_month, end_month and dataset name"""
    # End_month is exclusive in RTE service (and we want the API to be inclusive)
    end_month += 1

    # Query validation
    if year < 2013:
        raise HTTPException(status_code=400, detail="Cannot query data before 2013")
    if start_month > end_month:
        raise HTTPException(status_code=400, detail="Bad parameter : start month > end month")
    if end_month - start_month > 6:
        raise HTTPException(status_code=400, detail="Cannot query more than 6 months of data")
    today = date.today()
    if year > today.year or (year == today.year and end_month > today.month):
        raise HTTPException(status_code=400, detail="Cannot query data into the future")

    # retrieving and saving the data
    try:
        rte_france_service.retrieve_raw_short_term_data(year, start_month, end_month, dataset_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"response": "ok"}


@app.get("/prepare-raw-weather-data")
def prepare_raw_weather_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.prepare_raw_weather_data(dataset_name)
    return {"response": "ok"}


@app.get("/prepare-raw-rte-data")
def prepare_raw_rte_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.prepare_raw_rte_data(dataset_name)
    return {"response": "ok"}


@app.get("/merge-curated-data")
def merge_curated_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.merge_curated_data(dataset_name)
    return {"response": "ok"}


@app.get("/validate-refined-data")
def validate_refined_data(dataset_name: Optional[str] = "train"):
    results = great_expectations_service.validate_refined_data(dataset_name)
    # webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=results.success)
    # webhook.execute()
    validation_results_uri = great_expectations_service.get_validation_results_uri(results)
    return RedirectResponse(f"{GE_STATIC_ROOT}{validation_results_uri}")


@app.get("/run-whole-pipeline")
def run_whole_pipeline(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    # 1) retrieve raw data
    retrieve_raw_weather_data(year, start_month, end_month, dataset_name)
    retrieve_raw_rte_data(year, start_month, end_month, dataset_name)
    # 2) prepare data and store in curated
    prepare_raw_weather_data(dataset_name)
    prepare_raw_rte_data(dataset_name)
    # 3) merge data and store in refined : ready to train
    merge_curated_data(dataset_name)
    return {"response": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
