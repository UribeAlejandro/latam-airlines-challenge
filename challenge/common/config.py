from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(StrEnum):
    """Application runtime environments."""

    local = "local"
    ci = "ci"
    dev = "dev"
    prod = "prod"


class AppSettings(BaseSettings):
    """Configuration settings for the application."""

    environment: Environment = Field(..., alias="ENVIRONMENT")
    debug: bool
    project_name: str
    version: str
    description: str

    # MLFlow
    mlflow_tracking_uri: str

    # Model
    model_path: str = "model/logistic_regression.pkl"
    encoder_path: str = "model/encoder.pkl"


settings = AppSettings()
