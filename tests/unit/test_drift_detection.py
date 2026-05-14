import pytest
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from src.drift.evidently_runner import DriftDetector
from src.drift.reference_builder import ReferenceBuilder
from src.drift.drift_config import DriftConfig

@pytest.fixture
def reference_data() -> pd.DataFrame:
    """Fixture for generating reference dataset."""
    data = {
        "feature_1": [1, 2, 3, 4, 5],
        "feature_2": [5, 4, 3, 2, 1],
        "target": [0, 1, 0, 1, 0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def new_data() -> pd.DataFrame:
    """Fixture for generating new dataset for drift detection."""
    data = {
        "feature_1": [1, 2, 3, 4, 6],
        "feature_2": [5, 4, 3, 2, 0],
        "target": [0, 1, 0, 1, 0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def drift_config() -> DriftConfig:
    """Fixture for loading drift configuration."""
    return DriftConfig.from_yaml("configs/drift_config.yaml")

def test_reference_builder(reference_data: pd.DataFrame, drift_config: DriftConfig) -> None:
    """Test the reference dataset builder."""
    builder = ReferenceBuilder(reference_data, drift_config)
    reference = builder.build_reference()
    assert reference.shape[0] == reference_data.shape[0], "Reference dataset size mismatch."

def test_drift_detection(reference_data: pd.DataFrame, new_data: pd.DataFrame, drift_config: DriftConfig) -> None:
    """Test the drift detection using Evidently."""
    detector = DriftDetector(reference_data, new_data, drift_config)
    report = detector.detect_drift()
    
    assert isinstance(report, Report), "Drift detection did not return a valid report."
    assert len(report.get_metrics()) > 0, "Drift report should contain metrics."

def test_drift_report_generation(reference_data: pd.DataFrame, new_data: pd.DataFrame, drift_config: DriftConfig) -> None:
    """Test the generation of the drift report."""
    detector = DriftDetector(reference_data, new_data, drift_config)
    report = detector.generate_report()
    
    assert report is not None, "Drift report generation failed."
    assert "Data Drift" in report.get_metrics(), "Drift report should contain 'Data Drift' metrics."
# 11:24:54 — automated update
# feat: save drift reports as HTML artifacts to S3

# 11:19:18 — automated update
# refactor: rename variable for clarity in test_drift_detection — 11:19:18 UTC
