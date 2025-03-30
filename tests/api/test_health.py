from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_get_health(app: FastAPI) -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
