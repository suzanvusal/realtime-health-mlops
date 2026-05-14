import pytest
import pandas as pd
from src.models.xgboost_trainer import XGBoostTrainer
from src.models.hyperparameter_tuner import HyperparameterTuner
from src.models.explainability import Explainability
import shap

@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture to provide sample patient data for testing."""
    data = {
        'age': [25, 30, 45, 50],
        'blood_pressure': [120, 130, 140, 150],
        'cholesterol': [200, 210, 220, 230],
        'risk': [0, 1, 1, 0]
    }
    return pd.DataFrame(data)

def test_xgboost_trainer(sample_data: pd.DataFrame) -> None:
    """Test the XGBoost model training."""
    trainer = XGBoostTrainer()
    X = sample_data.drop('risk', axis=1)
    y = sample_data['risk']
    
    model = trainer.train(X, y)
    
    assert model is not None
    assert hasattr(model, 'predict')

def test_hyperparameter_tuner(sample_data: pd.DataFrame) -> None:
    """Test hyperparameter tuning functionality."""
    tuner = HyperparameterTuner()
    X = sample_data.drop('risk', axis=1)
    y = sample_data['risk']
    
    best_params = tuner.tune(X, y)
    
    assert isinstance(best_params, dict)
    assert 'max_depth' in best_params
    assert 'learning_rate' in best_params

def test_explainability(sample_data: pd.DataFrame) -> None:
    """Test SHAP explainability for the trained model."""
    trainer = XGBoostTrainer()
    X = sample_data.drop('risk', axis=1)
    y = sample_data['risk']
    
    model = trainer.train(X, y)
    explainer = Explainability(model)
    
    shap_values = explainer.shap_values(X)
    
    assert isinstance(shap_values, np.ndarray)
    assert shap_values.shape == X.shape

def test_model_prediction(sample_data: pd.DataFrame) -> None:
    """Test model prediction functionality."""
    trainer = XGBoostTrainer()
    X = sample_data.drop('risk', axis=1)
    y = sample_data['risk']
    
    model = trainer.train(X, y)
    predictions = model.predict(X)
    
    assert len(predictions) == len(y)
    assert set(predictions).issubset({0, 1})  # Assuming binary classification
# 11:13:34 — automated update
# test marker: test: add test that trained model achieves AUC > 0.75 on hel
_TEST_MARKER = 'test_model_trainer'

# 11:19:18 — automated update
# refactor: rename variable for clarity in test_model_trainer — 11:19:18 UTC
