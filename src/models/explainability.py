import pandas as pd
import shap
import xgboost as xgb
from typing import Any, Dict
from mlflow import log_artifact, log_param, log_metric
from mlflow.xgboost import log_model

class Explainability:
    def __init__(self, model: xgb.Booster, feature_names: list):
        """
        Initialize the Explainability class.

        :param model: Trained XGBoost model.
        :param feature_names: List of feature names used in the model.
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.Explainer(model)

    def explain(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate SHAP values for the provided input data.

        :param X: Input features as a pandas DataFrame.
        :return: SHAP values and feature importance.
        """
        shap_values = self.explainer(X)
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': shap_values.abs.mean(axis=0)
        }).sort_values(by='importance', ascending=False)

        return {
            'shap_values': shap_values,
            'feature_importance': feature_importance
        }

    def log_explanation(self, X: pd.DataFrame, run_id: str) -> None:
        """
        Log SHAP values and feature importance to MLflow.

        :param X: Input features as a pandas DataFrame.
        :param run_id: MLflow run ID for logging.
        """
        explanation = self.explain(X)
        shap_values = explanation['shap_values']
        feature_importance = explanation['feature_importance']

        # Log SHAP values
        shap.summary_plot(shap_values, X, feature_names=self.feature_names, show=False)
        log_artifact('shap_summary_plot.png')

        # Log feature importance
        feature_importance.to_csv('feature_importance.csv', index=False)
        log_artifact('feature_importance.csv')

        # Log metrics
        for idx, row in feature_importance.iterrows():
            log_metric(row['feature'], row['importance'])

def load_model(model_path: str) -> xgb.Booster:
    """
    Load a trained XGBoost model from a specified path.

    :param model_path: Path to the trained model.
    :return: Loaded XGBoost model.
    """
    return xgb.Booster(model_file=model_path)
# 11:13:34 — automated update
# perf improvement at 11:13:34
_CACHE: dict = {}  # perf: enable GPU training with tree_meth

# 11:13:34 — automated update
# refactor: refactor: extract evaluation metrics to shared metrics modul
_REFACTORED = True

# 10:44:06 — automated update
# refactor: rename variable for clarity in explainability — 10:44:06 UTC
