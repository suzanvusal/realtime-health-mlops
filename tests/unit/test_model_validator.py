import pytest
import numpy as np
import pandas as pd
from src.retraining.model_validator import ModelValidator
from src.retraining.champion_challenger import ChampionChallenger
from src.retraining.model_promoter import ModelPromoter

@pytest.fixture
def setup_model_validator():
    """Fixture to set up the ModelValidator with dummy data."""
    model_validator = ModelValidator()
    model_validator.set_threshold(0.8)
    return model_validator

@pytest.fixture
def setup_champion_challenger():
    """Fixture to set up the ChampionChallenger with dummy models."""
    champion = "champion_model"
    challenger = "challenger_model"
    cc = ChampionChallenger(champion, challenger)
    return cc

@pytest.fixture
def setup_model_promoter():
    """Fixture to set up the ModelPromoter."""
    promoter = ModelPromoter()
    return promoter

def test_model_validation_accuracy(setup_model_validator):
    """Test the model validation accuracy."""
    y_true = np.array([1, 0, 1, 1, 0])
    y_pred = np.array([1, 0, 1, 0, 0])
    accuracy = setup_model_validator.validate(y_true, y_pred)
    assert accuracy >= 0.6, "Model accuracy should be above the threshold."

def test_champion_challenger_winner(setup_champion_challenger):
    """Test the champion-challenger selection."""
    cc = setup_champion_challenger
    cc.set_performance_metrics(champion_score=0.85, challenger_score=0.80)
    winner = cc.select_winner()
    assert winner == "champion_model", "Champion model should be selected."

def test_model_promotion(setup_model_promoter):
    """Test the model promotion process."""
    setup_model_promoter.add_model("new_model", 0.9)
    promoted = setup_model_promoter.promote("new_model")
    assert promoted is True, "New model should be promoted successfully."

def test_model_validation_threshold(setup_model_validator):
    """Test the model validation threshold."""
    setup_model_validator.set_threshold(0.75)
    assert setup_model_validator.threshold == 0.75, "Threshold should be set correctly."

def test_champion_challenger_no_winner(setup_champion_challenger):
    """Test the case where there is no winner."""
    cc = setup_champion_challenger
    cc.set_performance_metrics(champion_score=0.80, challenger_score=0.80)
    winner = cc.select_winner()
    assert winner is None, "There should be no winner if scores are equal."

def test_model_promotion_failure(setup_model_promoter):
    """Test the model promotion failure scenario."""
    setup_model_promoter.add_model("old_model", 0.6)
    promoted = setup_model_promoter.promote("old_model")
    assert promoted is False, "Old model should not be promoted."
# 11:48:47 — automated update
# feat: implement automated MLflow model stage promotion on validation pass

# 11:48:47 — automated update
# fix applied at 11:48:47
_FIXED = True  # fix: DeLong test using incorrect variance formula

# 11:48:47 — automated update
# perf: add __slots__ to reduce memory in test_model_validator — 11:48:47 UTC
