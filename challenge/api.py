from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import pandas as pd
import structlog
from fastapi import Body, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from challenge.common.config import settings
from challenge.common.dependency import get_ml_model
from challenge.common.logger import setup_logger
from challenge.common.schemas import HealthResponse, PredictionRequest, PredictionResponse
from challenge.model import DelayModel

setup_logger()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for FastAPI application."""
    logger.info("Starting API.")
    yield
    logger.info("Shutting down API.")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Overrides default response to Validation Errors.

    Parameters
    ----------
    request : Request
        Incoming request that caused the validation error.
    exc : RequestValidationError
        The validation error exception containing details about the error.

    Returns
    -------
    JSONResponse
        A JSON response with status code 400 and details about the validation error.
    """
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "errors": exc.errors()},
    )


@app.get(
    "/health",
    status_code=200,
    response_model=HealthResponse,
)
async def get_health() -> HealthResponse:
    """
    Check API health.

    Returns
    -------
    HealthResponse
        API health status.
    """
    return HealthResponse(status="OK")


@app.post("/predict", status_code=200, response_model=PredictionResponse)
async def post_predict(
    ml_model: Annotated[DelayModel, Depends(get_ml_model)],
    flights: list[PredictionRequest] = Body(..., embed=True),  # noqa: F821
) -> PredictionResponse:
    """
    Predict delays for new flights.

    Returns
    -------
    PredictionResponse
        Predicted targets.
    """
    data = pd.DataFrame([flight.model_dump() for flight in flights])
    features = ml_model.preprocess(data=data)
    predictions = ml_model.predict(features=features)  # pyrefly: ignore [bad-argument-type]
    return PredictionResponse(predict=predictions)
