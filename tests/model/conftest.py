from challenge.constants import TARGET_COL
import pytest

import pandas as pd
from challenge.constants import DATA_PATH

from challenge.model import DelayModel

@pytest.fixture(scope="session")
def model()-> DelayModel:
    """Fixture for the DelayModel instance."""
    return DelayModel()

@pytest.fixture
def data()-> pd.DataFrame:
    """Fixture for loading the dataset."""
    return pd.read_csv(filepath_or_buffer=DATA_PATH)
