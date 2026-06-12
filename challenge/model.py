from functools import lru_cache
from pickle import dump, load

import pandas as pd
import structlog
from sklearn.linear_model import LogisticRegression

from challenge.constants import RANDOM_STATE
from challenge.data.etl import transform_data

logger = structlog.get_logger(__name__)


class DelayModel:
    """Model for predicting flight delays."""

    def __init__(self):
        self.__model_path = "model/logistic_regression.pkl"
        self._model: LogisticRegression | None = None

    @property
    @lru_cache
    def model(self) -> LogisticRegression:
        """
        Model for predicting flight delays.

        Returns
        -------
        LogisticRegression
            The logistic regression model used for prediction.
        """
        logger.info("Accessing the model.")
        self.__load_model()
        return self._model  # pyrefly: ignore [bad-return]

    def preprocess(
        self, data: pd.DataFrame, target_column: str | None = None
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
        logger.info("Preprocessing data.", data_shape=data.shape, target_column=target_column)
        return transform_data(data, target_column=target_column)

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Parameters
        ----------
        features: pd.DataFrame
            Preprocessed data.
        target: pd.DataFrame
            Target data.
        """
        logger.info("Fitting model.", features_shape=features.shape, target_shape=target.shape)

        self._model = LogisticRegression(random_state=RANDOM_STATE, n_jobs=-1)
        self._model.fit(X=features, y=target.values.ravel())
        with open(self.__model_path, "wb") as model_file:
            logger.info("Saving model to disk.", model_path=self.__model_path)
            dump(self._model, model_file)

    def predict(self, features: pd.DataFrame) -> list[int]:
        """
        Predict delays for new flights.

        Parameters
        ----------
        features: pd.DataFrame
            Preprocessed data.

        Returns
        -------
        List[int]
            Predicted targets.
        """
        self.__load_model()
        return self._model.predict(X=features).tolist()  # pyrefly: ignore [missing-attribute]

    def __load_model(self) -> None:
        """Load model from disk."""
        # TODO: MLFlow model registry
        if self._model is None:
            logger.info("Loading model from disk.", model_path=self.__model_path)
            with open(self.__model_path, "rb") as model_file:
                self._model = load(model_file)
