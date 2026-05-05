import os
from typing import Any, Dict
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import mlflow.xgboost
import yaml


class MLflowClient:
    def __init__(self, config_path: str):
        """
        Initialize the MLflowClient with the configuration from the specified YAML file.

        Args:
            config_path (str): Path to the YAML configuration file for MLflow.
        """
        self.config = self.load_config(config_path)
        self.setup_mlflow()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Loaded configuration as a dictionary.
        """
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def setup_mlflow(self) -> None:
        """
        Set up MLflow tracking server and experiment configuration.
        """
        mlflow.set_tracking_uri(self.config['tracking_uri'])
        mlflow.set_experiment(self.config['experiment_name'])
        mlflow.log_param("artifact_location", self.config['artifact_location'])
        mlflow.log_param("model_registry", self.config['model_registry'])

    def log_model(self, model: Any, model_name: str, params: Dict[str, Any], metrics: Dict[str, Any]) -> None:
        """
        Log a model to MLflow.

        Args:
            model (Any): The model object to log (XGBoost, PyTorch, etc.).
            model_name (str): The name of the model.
            params (Dict[str, Any]): Parameters used for the model.
            metrics (Dict[str, Any]): Metrics to log for the model.
        """
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            if isinstance(model, mlflow.pyfunc.PythonFunction):
                mlflow.pyfunc.log_model(model_name, python_model=model)
            elif hasattr(model, 'get_booster'):
                mlflow.xgboost.log_model(model, model_name)
            elif hasattr(model, 'state_dict'):
                mlflow.pytorch.log_model(model, model_name)
            else:
                raise ValueError("Unsupported model type for logging.")

    def register_model(self, model_uri: str, model_name: str) -> None:
        """
        Register a model in the MLflow model registry.

        Args:
            model_uri (str): URI of the model to register.
            model_name (str): Name to assign to the registered model.
        """
        mlflow.register_model(model_uri=model_uri, name=model_name)


if __name__ == "__main__":
    client = MLflowClient(config_path='configs/mlflow_config.yaml')
# 10:51:30 — automated update
# infra: add MLflow server Dockerfile with Nginx reverse proxy
