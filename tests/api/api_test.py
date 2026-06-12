import pytest
from fastapi.testclient import TestClient

@pytest.mark.anyio
async def test_should_get_predict(client: TestClient):
    data = {"flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}]}
    # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0])) # change this line to the model of choosing
    response = await client.post("/predict", json=data)
    assert response.status_code == 200
    assert response.json() == {"predict": [0]}

@pytest.mark.anyio
async def test_should_failed_unkown_column_1(client: TestClient):
    data = {"flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 13}]}
    # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))# change this line to the model of choosing
    response = await client.post("/predict", json=data)
    assert response.status_code == 400

@pytest.mark.anyio
async def test_should_failed_unkown_column_2(client: TestClient):
    data = {"flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "O", "MES": 13}]}
    # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))# change this line to the model of choosing
    response = await client.post("/predict", json=data)
    assert response.status_code == 400

@pytest.mark.anyio
async def test_should_failed_unkown_column_3(client: TestClient):
    data = {"flights": [{"OPERA": "Argentinas", "TIPOVUELO": "O", "MES": 13}]}
    # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))
    response = await client.post("/predict", json=data)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_should_get_health(client: TestClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


@pytest.mark.anyio
async def test_should_get_predict_multiple(client: TestClient):
    data = {"flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}, {"OPERA": "Delta Air", "TIPOVUELO": "I", "MES": 5}]}
    # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0])) # change this line to the model of choosing
    response = await client.post("/predict", json=data)
    assert response.status_code == 200
    assert response.json() == {"predict": [0, 0]}
