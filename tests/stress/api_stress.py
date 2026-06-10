from locust import HttpUser, task, between


class StressUser(HttpUser):

    @task
    def predict_argentinas(self) -> None:
        """Stress for predict (argentinas) endpoint."""
        self.client.post("/predict", json={"flights": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}]})

    @task(3)
    def predict_latam(self) -> None:
        """Stress for predict (latam) endpoint."""
        self.client.post("/predict", json={"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "N", "MES": 3}]})
