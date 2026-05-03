import pytest
import pandas as pd
from src.features.window_features import SlidingWindowFeatures
from src.features.hrv_calculator import HRVCalculator
from src.features.trend_detector import TrendDetector

@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Create a sample DataFrame for testing."""
    data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='T'),
        'heart_rate': [60 + (i % 10) for i in range(100)],
        'rr_intervals': [800 + (i % 5) * 20 for i in range(100)]
    }
    return pd.DataFrame(data)

def test_sliding_window_features(sample_data: pd.DataFrame) -> None:
    """Test sliding window feature extraction."""
    window_size = 10
    features = SlidingWindowFeatures(window_size)
    result = features.extract(sample_data)

    assert result.shape[0] == len(sample_data) - window_size + 1
    assert 'mean_heart_rate' in result.columns
    assert 'std_heart_rate' in result.columns

def test_hrv_calculator(sample_data: pd.DataFrame) -> None:
    """Test HRV calculation."""
    hrv_calculator = HRVCalculator()
    hrv_values = hrv_calculator.calculate(sample_data['rr_intervals'])

    assert len(hrv_values) == len(sample_data)
    assert all(isinstance(val, float) for val in hrv_values)

def test_trend_detector(sample_data: pd.DataFrame) -> None:
    """Test trend detection on heart rate data."""
    trend_detector = TrendDetector()
    trends = trend_detector.detect(sample_data['heart_rate'])

    assert isinstance(trends, list)
    assert len(trends) == len(sample_data)
    assert all(isinstance(trend, str) for trend in trends)

def test_combined_feature_extraction(sample_data: pd.DataFrame) -> None:
    """Test combined feature extraction including HRV and trends."""
    window_size = 10
    features = SlidingWindowFeatures(window_size)
    hrv_calculator = HRVCalculator()
    trend_detector = TrendDetector()

    windowed_features = features.extract(sample_data)
    hrv_values = hrv_calculator.calculate(sample_data['rr_intervals'])
    trends = trend_detector.detect(sample_data['heart_rate'])

    combined_features = windowed_features.copy()
    combined_features['hrv'] = hrv_values[window_size - 1:].reset_index(drop=True)
    combined_features['trend'] = trends[window_size - 1:].reset_index(drop=True)

    assert 'hrv' in combined_features.columns
    assert 'trend' in combined_features.columns
    assert combined_features.shape[0] == len(sample_data) - window_size + 1
# 10:27:16 — automated update
"""\ndocs: add docstrings with formula references to HRV functions\n"""

# 10:11:53 — automated update
# ci: update step name for readability — 10:11:53 UTC
