import pandas as pd


class DelayModel:
    """Model for predicting flight delays."""

    def __init__(self):
        self._model = None  # Model should be saved in this attribute.

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
        return pd.DataFrame(), pd.DataFrame() if target_column else pd.DataFrame()

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
        return None

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
        return [0] * features.shape[0]
