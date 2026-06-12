import pandas as pd
from challenge.constants import TOP_10_FEATURES, TARGET_COL
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from challenge.model import DelayModel


def test_model_preprocess_for_training(data: pd.DataFrame, model: DelayModel):
    """Test the preprocess method of the DelayModel for training data."""
    features, target = model.preprocess(data=data, target_column=TARGET_COL[0])

    assert isinstance(features, pd.DataFrame)
    assert features.shape[1] == len(TOP_10_FEATURES)
    assert set(features.columns) == set(TOP_10_FEATURES)

    assert isinstance(target, pd.DataFrame)
    assert target.shape[1] == len(TARGET_COL)
    assert set(target.columns) == set(TARGET_COL)

def test_model_preprocess_for_serving(data: pd.DataFrame, model: DelayModel):
    """Test the preprocess method of the DelayModel for serving data."""
    features = model.preprocess(data=data)

    assert isinstance(features, pd.DataFrame)
    assert features.shape[1] == len(TOP_10_FEATURES)
    assert set(features.columns) == set(TOP_10_FEATURES)

def test_model_fit(data: pd.DataFrame, model: DelayModel):
    """Test the fit method of the DelayModel."""
    features, target = model.preprocess(data=data, target_column=TARGET_COL[0])
    _, features_validation, _, target_validation = train_test_split(
        features, target, test_size=0.33, random_state=42
    )

    model.fit(features=features, target=target) # pyrefly: ignore [bad-argument-type]

    predicted_target = model._model.predict(features_validation)    # pyrefly: ignore [missing-attribute]

    report = classification_report(target_validation, predicted_target, output_dict=True)

    assert report["0"]["recall"] > 0.60     # pyrefly: ignore[bad-index]
    assert report["0"]["f1-score"] > 0.70   # pyrefly: ignore[bad-index]
    assert report["1"]["recall"] < 0.60     # pyrefly: ignore[bad-index]
    assert report["1"]["f1-score"] < 0.30   # pyrefly: ignore[bad-index]

def test_model_predict(data: pd.DataFrame, model: DelayModel):
    """Test the predict method of the DelayModel."""
    features: pd.DataFrame = model.preprocess(data=data)
    predicted_targets = model.predict(features=features)

    assert isinstance(predicted_targets, list)
    assert len(predicted_targets) == features.shape[0]
    assert all(isinstance(predicted_target, int) for predicted_target in predicted_targets)
