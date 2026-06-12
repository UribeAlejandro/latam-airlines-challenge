from typing import Literal

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Response model for predictions."""

    predict: list[int] = Field(..., description="Predicted target values.")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="API health status.")


class PredictionRequest(BaseModel):
    """Model for flight data input."""

    OPERA: Literal[
        "American Airlines",
        "Air Canada",
        "Air France",
        "Aeromexico",
        "Aerolineas Argentinas",
        "Austral",
        "Avianca",
        "Alitalia",
        "British Airways",
        "Copa Air",
        "Delta Air",
        "Gol Trans",
        "Iberia",
        "K.L.M.",
        "Qantas Airways",
        "United Airlines",
        "Grupo LATAM",
        "Sky Airline",
        "Latin American Wings",
        "Plus Ultra Lineas Aereas",
        "JetSmart SPA",
        "Oceanair Linhas Aereas",
        "Lacsa",
    ] = Field(..., description="Airline operator.")
    TIPOVUELO: Literal["N", "I"] = Field(..., description="Type of flight.")
    MES: int = Field(..., ge=1, le=12, description="Month of the flight.")
