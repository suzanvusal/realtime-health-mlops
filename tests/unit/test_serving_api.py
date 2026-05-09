import pytest
from fastapi.testclient import TestClient
from src.serving.api import app
from src.serving.request_models import PredictionRequest
from src.serving.response_models import PredictionResponse

client = TestClient(app)

@pytest.fixture
def valid_request_data() -> dict:
    return {
        "features": [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]]
    }

@pytest.fixture
def invalid_request_data() -> dict:
    return {
        "features": [[0.1, 0.2], [0.5, 0.6, 0.7, 0.8]]
    }

def test_predict_valid(valid_request_data: dict) -> None:
    response = client.post("/predict", json=valid_request_data)
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert len(response.json()["predictions"]) == len(valid_request_data["features"])

def test_predict_invalid(invalid_request_data: dict) -> None:
    response = client.post("/predict", json=invalid_request_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid list"

def test_predict_empty_features() -> None:
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid list"

def test_predict_single_feature() -> None:
    single_feature_request = {"features": [[0.1, 0.2, 0.3, 0.4]]}
    response = client.post("/predict", json=single_feature_request)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 1

def test_predict_batch_size_limit(valid_request_data: dict) -> None:
    oversized_request = {"features": [[0.1] * 100] * 11}  # Assuming max batch size is 10
    response = client.post("/predict", json=oversized_request)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Batch size exceeds limit"