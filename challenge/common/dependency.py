from typing import Annotated

from fastapi import Depends

from challenge.data.etl import ETL
from challenge.model import DelayModel


async def get_etl() -> ETL:
    """
    Get the ETL Pipeline.

    Returns
    -------
    ETL
        The ETL pipeline instance.
    """
    return ETL()


async def get_ml_model(etl: Annotated[ETL, Depends(get_etl)]) -> DelayModel:
    """
    Get the ML model.

    Returns
    -------
    DelayModel
        The ML model used for prediction.
    """
    return DelayModel(etl)
