"""XGBoost patient risk model trainer with MLflow integration."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import mlflow
import mlflow.xgboost
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import StratifiedKFold

logger = logging.getLogger(__name__)


@dataclass
class XGBTrainingConfig:
    n_estimators: int = 300
    max_depth: int = 6
    learning_rate: float = 0.05
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    min_child_weight: int = 5
    scale_pos_weight: float = 1.0
    early_stopping_rounds: int = 30
    eval_metric: str = "auc"
    n_cv_folds: int = 5
    random_state: int = 42
    xgb_params: dict[str, Any] = field(default_factory=dict)

    def to_xgb_params(self) -> dict[str, Any]:
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "learning_rate": self.learning_rate,
            "subsample": self.subsample,
            "colsample_bytree": self.colsample_bytree,
            "min_child_weight": self.min_child_weight,
            "scale_pos_weight": self.scale_pos_weight,
            "eval_metric": self.eval_metric,
            "tree_method": "hist",
            "random_state": self.random_state,
            **self.xgb_params,
        }


class XGBoostRiskTrainer:
    """Trains, evaluates, and registers an XGBoost patient risk model."""

    def __init__(self, config: XGBTrainingConfig | None = None) -> None:
        self.config = config or XGBTrainingConfig()
        self.model: xgb.XGBClassifier | None = None
        self.feature_names: list[str] = []

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        feature_names: list[str] | None = None,
    ) -> dict[str, float]:
        self.feature_names = feature_names or [f"f{i}" for i in range(X_train.shape[1])]
        params = self.config.to_xgb_params()

        with mlflow.start_run(nested=True):
            mlflow.log_params(params)

            self.model = xgb.XGBClassifier(**params)
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False,
            )

            metrics = self._evaluate(X_val, y_val)
            mlflow.log_metrics(metrics)
            mlflow.xgboost.log_model(self.model, "xgboost-model",
                                     input_example=X_train[:5])
            logger.info("Training complete: %s", metrics)
            return metrics

    def _evaluate(self, X: np.ndarray, y: np.ndarray) -> dict[str, float]:
        proba = self.model.predict_proba(X)[:, 1]
        return {
            "auc_roc": roc_auc_score(y, proba),
            "avg_precision": average_precision_score(y, proba),
            "best_iteration": self.model.best_iteration,
        }

    def cross_validate(self, X: np.ndarray, y: np.ndarray) -> dict[str, float]:
        cv = StratifiedKFold(n_splits=self.config.n_cv_folds, shuffle=True,
                             random_state=self.config.random_state)
        scores = []
        for fold, (tr_idx, val_idx) in enumerate(cv.split(X, y)):
            model = xgb.XGBClassifier(**self.config.to_xgb_params())
            model.fit(X[tr_idx], y[tr_idx], verbose=False)
            proba = model.predict_proba(X[val_idx])[:, 1]
            scores.append(roc_auc_score(y[val_idx], proba))
            logger.info("Fold %d AUC: %.4f", fold + 1, scores[-1])
        return {"cv_auc_mean": float(np.mean(scores)), "cv_auc_std": float(np.std(scores))}

# 11:13:33 — automated update
# feat: log SHAP summary plots as MLflow artifacts
