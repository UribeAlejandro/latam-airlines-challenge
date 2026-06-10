from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from challenge.utils.config import settings
from challenge.utils.logger import setup_logger

setup_logger()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for FastAPI application."""
    yield


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get(
    "/health",
    status_code=200,
    response_class=JSONResponse,
)
async def get_health() -> JSONResponse:
    """
    Check API health.

    Returns
    -------
    JSONResponse
        API health status.
    """
    return JSONResponse(content={"status": "OK"})


@app.post("/predict", status_code=200, response_class=JSONResponse)
async def post_predict() -> JSONResponse:
    """
    Predict delays for new flights.

    Returns
    -------
    JSONResponse
        Predicted targets.
    """
    return JSONResponse(content={"predictions": []})
