from challenge.model import DelayModel
from challenge.common.dependency import get_ml_model
import os
import pytest

from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from challenge.api import app

pytest_plugins = ["anyio"]


class MockDelayModel(DelayModel):
    """Mock implementation of the DelayModel for testing purposes."""
    def preprocess(self, data, target_column=None):
        """Mock preprocess method that returns the input data as features."""
        return data

    def predict(self, features):
        """Mock predict method that returns a list of zeros with the same length as the input features."""
        return [0] * len(features)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Specifies the AnyIO backend to use for asynchronous tests."""
    return "asyncio"

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    """Provides a TestClient for testing the FastAPI application."""

    async def override_get_ml_model():
        """Override for the get_ml_model dependency to provide a mock model during testing."""
        return MockDelayModel(None) # pyrefly: ignore [bad-argument-type]

    app.dependency_overrides[get_ml_model] = override_get_ml_model

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
