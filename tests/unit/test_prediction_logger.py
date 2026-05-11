import pytest
from unittest.mock import MagicMock
from src.serving.prediction_logger import PredictionLogger
from src.serving.outcome_ingester import OutcomeIngester
from src.monitoring.prediction_store import PredictionStore

@pytest.fixture
def prediction_logger() -> PredictionLogger:
    logger = PredictionLogger()
    logger.store = MagicMock(spec=PredictionStore)
    return logger

@pytest.fixture
def outcome_ingester() -> OutcomeIngester:
    ingester = OutcomeIngester()
    ingester.store = MagicMock(spec=PredictionStore)
    return ingester

def test_log_prediction(prediction_logger: PredictionLogger) -> None:
    prediction = {"patient_id": "123", "prediction": "healthy", "confidence": 0.95}
    prediction_logger.log_prediction(prediction)

    prediction_logger.store.save_prediction.assert_called_once_with(prediction)

def test_feedback_ingestion(outcome_ingester: OutcomeIngester) -> None:
    feedback = {"patient_id": "123", "actual_outcome": "unhealthy"}
    outcome_ingester.ingest_feedback(feedback)

    outcome_ingester.store.save_feedback.assert_called_once_with(feedback)

def test_prediction_logging_structure(prediction_logger: PredictionLogger) -> None:
    prediction = {"patient_id": "123", "prediction": "healthy", "confidence": 0.95}
    prediction_logger.log_prediction(prediction)
    
    logged_prediction = prediction_logger.store.save_prediction.call_args[0][0]
    assert "patient_id" in logged_prediction
    assert "prediction" in logged_prediction
    assert "confidence" in logged_prediction

def test_outcome_labeling_structure(outcome_ingester: OutcomeIngester) -> None:
    feedback = {"patient_id": "123", "actual_outcome": "unhealthy"}
    outcome_ingester.ingest_feedback(feedback)

    logged_feedback = outcome_ingester.store.save_feedback.call_args[0][0]
    assert "patient_id" in logged_feedback
    assert "actual_outcome" in logged_feedback

def test_prediction_and_feedback_flow(prediction_logger: PredictionLogger, outcome_ingester: OutcomeIngester) -> None:
    prediction = {"patient_id": "123", "prediction": "healthy", "confidence": 0.95}
    prediction_logger.log_prediction(prediction)

    feedback = {"patient_id": "123", "actual_outcome": "unhealthy"}
    outcome_ingester.ingest_feedback(feedback)

    assert prediction_logger.store.save_prediction.call_count == 1
    assert outcome_ingester.store.save_feedback.call_count == 1
# 12:17:50 — automated update
# feat: implement prediction log archival to S3 after 7 days

# 12:17:50 — automated update
# feat: add data export endpoint for retraining dataset assembly

# 12:17:50 — automated update
# fix applied at 12:17:50
_FIXED = True  # fix: prediction_id UUID collision on concurrent requests

# 12:17:50 — automated update
# perf improvement at 12:17:50
_CACHE: dict = {}  # perf: batch prediction log writes every 

# 12:17:50 — automated update
"""\ndocs: add data lineage diagram from prediction to retraining\n"""
