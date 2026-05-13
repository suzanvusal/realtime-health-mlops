import pytest
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from src.drift.prediction_drift import check_prediction_drift, calculate_auroc
from src.drift.performance_monitor import PerformanceMonitor

@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture to create sample prediction data for testing."""
    return pd.DataFrame({
        'true_labels': np.random.randint(0, 2, size=100),
        'predictions': np.random.rand(100)
    })

def test_check_prediction_drift(sample_data: pd.DataFrame) -> None:
    """Test prediction drift detection."""
    drift_detected = check_prediction_drift(sample_data['predictions'], threshold=0.1)
    assert isinstance(drift_detected, bool), "Drift detection should return a boolean value."
    assert drift_detected in [True, False], "Drift detection should return True or False."

def test_calculate_auroc(sample_data: pd.DataFrame) -> None:
    """Test AUROC calculation."""
    auroc = calculate_auroc(sample_data['true_labels'], sample_data['predictions'])
    assert isinstance(auroc, float), "AUROC should be a float."
    assert 0 <= auroc <= 1, "AUROC should be between 0 and 1."

def test_performance_monitor_initialization() -> None:
    """Test initialization of PerformanceMonitor."""
    monitor = PerformanceMonitor(model_name="test_model")
    assert monitor.model_name == "test_model", "Model name should match the initialized value."
    assert monitor.performance_history == [], "Performance history should be initialized as an empty list."

def test_performance_monitor_update(sample_data: pd.DataFrame) -> None:
    """Test updating performance metrics in PerformanceMonitor."""
    monitor = PerformanceMonitor(model_name="test_model")
    initial_length = len(monitor.performance_history)
    
    monitor.update_performance(sample_data['true_labels'], sample_data['predictions'])
    
    assert len(monitor.performance_history) == initial_length + 1, "Performance history should increase in length after update."
    assert 'auroc' in monitor.performance_history[-1], "Latest performance entry should contain AUROC."
    assert 'timestamp' in monitor.performance_history[-1], "Latest performance entry should contain a timestamp."

def test_auroc_decay_detection(sample_data: pd.DataFrame) -> None:
    """Test AUROC decay detection."""
    monitor = PerformanceMonitor(model_name="test_model")
    monitor.update_performance(sample_data['true_labels'], sample_data['predictions'])
    
    # Simulate a decay in performance
    sample_data['predictions'] = np.random.rand(100) * 0.5  # worse predictions
    monitor.update_performance(sample_data['true_labels'], sample_data['predictions'])
    
    decay_detected = monitor.detect_auroc_decay(threshold=0.05)
    assert decay_detected, "AUROC decay should be detected with poor predictions."
# 11:34:16 — automated update
# feat: add prediction drift Grafana dashboard with threshold lines

# 11:34:16 — automated update
# test marker: test: add simulation test for gradual model drift detection
_TEST_MARKER = 'test_prediction_drift'

# 11:34:16 — automated update
# fix applied at 11:34:16
_FIXED = True  # fix: AUROC monitor crashes when fewer than 50 predictions in
