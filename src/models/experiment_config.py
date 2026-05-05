import os
from typing import Dict, Any
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import mlflow.xgboost

class ExperimentConfig:
    """
    A class to manage MLflow experiment configurations.
    """

    def __init__(self, experiment_name: str, tracking_uri: str, artifact_location: str):
        """
        Initializes the ExperimentConfig with the provided parameters.

        Args:
            experiment_name (str): Name of the MLflow experiment.
            tracking_uri (str): URI for the MLflow tracking server.
            artifact_location (str): Location for storing artifacts.
        """
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        self.artifact_location = artifact_location
        self._set_mlflow_config()

    def _set_mlflow_config(self) -> None:
        """
        Sets the MLflow tracking URI and initializes the experiment.
        """
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Logs parameters to the current MLflow run.

        Args:
            params (Dict[str, Any]): Dictionary of parameters to log.
        """
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        """
        Logs metrics to the current MLflow run.

        Args:
            metrics (Dict[str, float]): Dictionary of metrics to log.
        """
        mlflow.log_metrics(metrics)

    def log_model(self, model: Any, model_name: str) -> None:
        """
        Logs the model to the MLflow model registry.

        Args:
            model (Any): The trained model to log (XGBoost, PyTorch, etc.).
            model_name (str): The name under which to log the model.
        """
        if isinstance(model, (mlflow.sklearn.SklearnModel, mlflow.xgboost.XGBoostModel)):
            mlflow.sklearn.log_model(model, model_name)
        elif isinstance(model, mlflow.pytorch.PyTorchModel):
            mlflow.pytorch.log_model(model, model_name)
        else:
            raise ValueError("Unsupported model type for logging.")

    def get_experiment_id(self) -> str:
        """
        Retrieves the experiment ID for the current experiment.

        Returns:
            str: The experiment ID.
        """
        return mlflow.get_experiment_by_name(self.experiment_name).experiment_id

# Example usage:
# config = ExperimentConfig("HealthMonitoringExperiment", "http://localhost:5000", "/artifacts")
# config.log_params({"learning_rate": 0.01, "n_estimators": 100})
# 10:51:30 — automated update
# notebook: add experiment setup and baseline run notebook

# 10:51:30 — automated update
# fix applied at 10:51:30
_FIXED = True  # fix: MLflow artifact path encoding issue on Windows paths
