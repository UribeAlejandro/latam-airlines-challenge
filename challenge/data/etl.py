from datetime import datetime
from typing import Literal

import numpy as np
import pandas as pd
import structlog
from sklearn.utils import shuffle

from challenge.constants import DUMMY_COLUMNS, RANDOM_STATE, THRESHOLD_IN_MINUTES, TOP_10_FEATURES

logger = structlog.get_logger(__name__)


def extract_data(source: str) -> pd.DataFrame:
    """
    Extract data from a given source.

    Parameters
    ----------
    source : str
        The path to the data source (e.g., a CSV file).

    Returns
    -------
    pd.DataFrame
        The extracted data as a DataFrame.
    """
    logger.info("Extracting data from source.", source=source)
    data = pd.read_csv(source)
    return data


def load_data(data: pd.DataFrame, destination: str) -> None:
    """
    Load data to a given destination.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to be loaded.
    destination : str
        The path to the destination where the data should be saved (e.g., a CSV file).
    """
    logger.info("Loading data to destination.", destination=destination)
    data.to_csv(destination, index=False)


def transform_data(
    data: pd.DataFrame, target_column: str | None = None
) -> tuple[pd.DataFrame, pd.DataFrame] | pd.DataFrame:
    """
    Prepare raw data for training or predict.

    Parameters
    ----------
    data: pd.DataFrame
        Raw data.
    target_column: str | None
        If set, the target is returned.

    Returns
    -------
    Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]
        Features and target if target_column is set, otherwise only features.
    """
    logger.info("Shuffling data.")
    data = shuffle(data, random_state=RANDOM_STATE)
    data = data.reset_index(drop=True)

    logger.info("Extracting features and target.")
    features = pd.concat([pd.get_dummies(data[col], prefix=col) for col in DUMMY_COLUMNS], axis=1)
    features = features[TOP_10_FEATURES]

    if not target_column:
        return features

    logger.info("Calculating delay column.")
    data["min_diff"] = data.apply(get_min_diff, axis=1)
    data["delay"] = np.where(data["min_diff"] > THRESHOLD_IN_MINUTES, 1, 0)
    target = data["delay"].to_frame(name=target_column)
    return features, target


def get_min_diff(data: pd.Series) -> float:
    """
    Calculate the difference in minutes between two datetime columns "Fecha-O" and "Fecha-I".

    Parameters
    ----------
    data : pd.Series
        A Series representing a single row containing the columns "Fecha-O" and "Fecha-I" with datetime strings

    Returns
    -------
    float
        The difference in minutes between "Fecha-O" and "Fecha-I".
    """
    fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
    fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
    min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
    return min_diff


def get_period_day(date_str: str) -> Literal["mañana", "tarde", "noche"]:
    """
    Determine the period of the day for a given datetime.

    Parameters
    ----------
    date_str : str
        A string representing a datetime in the format "%Y-%m-%d %H:%M:%S".

    Returns
    -------
    str
        The period of the day ("mañana", "tarde", or "noche").
    """
    date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").time()
    morning_min = datetime.strptime("05:00", "%H:%M").time()
    morning_max = datetime.strptime("11:59", "%H:%M").time()
    afternoon_min = datetime.strptime("12:00", "%H:%M").time()
    afternoon_max = datetime.strptime("18:59", "%H:%M").time()

    if morning_min <= date_time <= morning_max:
        return "mañana"
    elif afternoon_min <= date_time <= afternoon_max:
        return "tarde"
    else:
        return "noche"


def is_high_season(fecha_str: str) -> Literal[0, 1]:
    """
    Determine if a given date falls within the high season periods.

    Parameters
    ----------
    fecha_str : str
        A string representing a datetime in the format "%Y-%m-%d %H:%M:%S".

    Returns
    -------
    Literal[0, 1]
        1 if the date falls within the high season periods, 0 otherwise.
    """
    fecha_año = int(fecha_str.split("-")[0])
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    range1_min = datetime.strptime("15-Dec", "%d-%b").replace(year=fecha_año)
    range1_max = datetime.strptime("31-Dec", "%d-%b").replace(year=fecha_año)
    range2_min = datetime.strptime("1-Jan", "%d-%b").replace(year=fecha_año)
    range2_max = datetime.strptime("3-Mar", "%d-%b").replace(year=fecha_año)
    range3_min = datetime.strptime("15-Jul", "%d-%b").replace(year=fecha_año)
    range3_max = datetime.strptime("31-Jul", "%d-%b").replace(year=fecha_año)
    range4_min = datetime.strptime("11-Sep", "%d-%b").replace(year=fecha_año)
    range4_max = datetime.strptime("30-Sep", "%d-%b").replace(year=fecha_año)

    if (
        (fecha >= range1_min and fecha <= range1_max)
        or (fecha >= range2_min and fecha <= range2_max)
        or (fecha >= range3_min and fecha <= range3_max)
        or (fecha >= range4_min and fecha <= range4_max)
    ):
        return 1
    else:
        return 0


def get_rate_from_column(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Calculate the delay rate for each unique value in a specified column.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the flight data, including a "delay" column.
    column : str
        The column name for which to calculate delay rates.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the delay rates for each unique value in the specified column.
    """
    delays = {}
    for _, row in data.iterrows():
        if row["delay"] == 1:
            if row[column] not in delays:
                delays[row[column]] = 1
            else:
                delays[row[column]] += 1
    total = data[column].value_counts().to_dict()

    rates = {}
    for name, count in total.items():
        if name in delays:
            rates[name] = round(100 * delays[name] / count, 2)
        else:
            rates[name] = 0

    return pd.DataFrame.from_dict(data=rates, orient="index", columns=["Tasa (%)"])
