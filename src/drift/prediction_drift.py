import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.metrics import roc_auc_score
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric import Metric
from evidently.metrics import ClassificationPerformance
from evidently.metrics import DataDrift
import mlflow
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionDriftMonitor:
    def __init__(self, model_name: str, model_version: str, threshold: float = 0.05):
        """
        Initializes the PredictionDriftMonitor.

        :param model_name: Name of the ML model.
        :param model_version: Version of the ML model.
        :param threshold: Drift detection threshold.
        """
        self.model_name = model_name
        self.model_version = model_version
        self.threshold = threshold
        self.previous_predictions = None

    def log_model_performance(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Logs model performance metrics.

        :param y_true: True labels.
        :param y_pred: Predicted probabilities.
        """
        auroc = roc_auc_score(y_true, y_pred)
        mlflow.log_metric("auroc", auroc)
        logger.info(f"Logged AUROC: {auroc}")

    def detect_drift(self, current_data: pd.DataFrame, reference_data: pd.DataFrame) -> Tuple[bool, float]:
        """
        Detects prediction drift between current and reference datasets.

        :param current_data: Current data for drift detection.
        :param reference_data: Reference data for drift detection.
        :return: Tuple indicating if drift is detected and the drift score.
        """
        column_mapping = ColumnMapping(target_column='target', prediction_column='prediction')
        report = Report(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
        report.run()

        drift_metric = report.get_metric(DataDrift)
        drift_score = drift_metric.get_value()
        logger.info(f"Drift score: {drift_score}")

        if drift_score > self.threshold:
            logger.warning("Drift detected!")
            return True, drift_score
        return False, drift_score

    def performance_dashboard(self, current_data: pd.DataFrame, reference_data: pd.DataFrame) -> None:
        """
        Generates and logs performance dashboard.

        :param current_data: Current data for performance evaluation.
        :param reference_data: Reference data for performance evaluation.
        """
        column_mapping = ColumnMapping(target_column='target', prediction_column='prediction')
        report = Report(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)
        report.run()

        performance_metric = report.get_metric(ClassificationPerformance)
        logger.info(f"Performance metrics: {performance_metric.get_value()}")
        report.save("performance_report.html")

    def update_predictions(self, new_predictions: np.ndarray) -> None:
        """
        Updates the stored predictions for future drift detection.

        :param new_predictions: New predictions to store.
        """
        self.previous_predictions = new_predictions
        logger.info("Updated previous predictions.")