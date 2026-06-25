import pytest
from model_validator import ModelValidator
import numpy as np
import pandas as pd


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture to create sample input data for testing."""
    return pd.DataFrame({
        'feature_1': [0.1, 0.2, 0.3, 0.4],
        'feature_2': [1, 2, 3, 4],
        'target': [0, 1, 0, 1]
    })


@pytest.fixture
def model_validator() -> ModelValidator:
    """Fixture to create an instance of ModelValidator."""
    return ModelValidator(model_path='path/to/model')


def test_validate_model_accuracy(model_validator: ModelValidator, sample_data: pd.DataFrame) -> None:
    """Test the model accuracy validation."""
    accuracy = model_validator.validate_accuracy(sample_data)
    assert accuracy >= 0.8, "Model accuracy is below the acceptable threshold."


def test_validate_input_shape(model_validator: ModelValidator, sample_data: pd.DataFrame) -> None:
    """Test the input shape validation."""
    valid_shape = model_validator.validate_input_shape(sample_data)
    assert valid_shape, "Input shape validation failed."


def test_validate_feature_distribution(model_validator: ModelValidator, sample_data: pd.DataFrame) -> None:
    """Test the feature distribution validation."""
    distribution_valid = model_validator.validate_feature_distribution(sample_data)
    assert distribution_valid, "Feature distribution validation failed."


def test_validate_target_distribution(model_validator: ModelValidator, sample_data: pd.DataFrame) -> None:
    """Test the target distribution validation."""
    target_distribution_valid = model_validator.validate_target_distribution(sample_data)
    assert target_distribution_valid, "Target distribution validation failed."


def test_validate_model_predictions(model_validator: ModelValidator, sample_data: pd.DataFrame) -> None:
    """Test the model predictions validation."""
    predictions = model_validator.validate_model_predictions(sample_data)
    assert len(predictions) == len(sample_data), "Predictions length does not match input data."


def test_model_validator_with_invalid_data(model_validator: ModelValidator) -> None:
    """Test the model validator with invalid data."""
    invalid_data = pd.DataFrame({
        'feature_1': [None, 0.2, 0.3],
        'feature_2': [1, 2, None],
        'target': [0, 1, 0]
    })
    with pytest.raises(ValueError, match="Invalid input data"):
        model_validator.validate_input_shape(invalid_data)


@pytest.mark.parametrize("input_data,expected", [
    (pd.DataFrame({'feature_1': [0.1], 'feature_2': [1]}), True),
    (pd.DataFrame({'feature_1': [], 'feature_2': []}), False)
])
def test_parametrized_input_shape_validation(model_validator: ModelValidator, input_data: pd.DataFrame, expected: bool) -> None:
    """Test input shape validation with parameterized tests."""
    result = model_validator.validate_input_shape(input_data)
    assert result == expected, f"Expected {expected} but got {result}."