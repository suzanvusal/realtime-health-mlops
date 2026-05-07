import optuna
import xgboost as xgb
import shap
import pandas as pd
from typing import Tuple, Any
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.xgboost


class HyperparameterTuner:
    def __init__(self, data: pd.DataFrame, target: str):
        """
        Initializes the HyperparameterTuner with data and target variable.

        Args:
            data (pd.DataFrame): The input data for training.
            target (str): The name of the target variable.
        """
        self.data = data
        self.target = target

    def objective(self, trial: optuna.Trial) -> float:
        """
        Objective function for Optuna to minimize.

        Args:
            trial (optuna.Trial): The trial object for hyperparameter optimization.

        Returns:
            float: The accuracy of the model on the validation set.
        """
        params = {
            'objective': 'binary:logistic',
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 5),
        }

        X_train, X_val, y_train, y_val = train_test_split(
            self.data.drop(columns=[self.target]),
            self.data[self.target],
            test_size=0.2,
            random_state=42
        )

        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        preds = model.predict(X_val)
        accuracy = accuracy_score(y_val, preds)

        return accuracy

    def tune_hyperparameters(self, n_trials: int = 100) -> Tuple[dict, float]:
        """
        Tunes hyperparameters using Optuna.

        Args:
            n_trials (int): Number of trials for hyperparameter tuning.

        Returns:
            Tuple[dict, float]: Best hyperparameters and corresponding accuracy.
        """
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=n_trials)

        return study.best_params, study.best_value

    def explain_model(self, model: Any, data: pd.DataFrame) -> None:
        """
        Generates SHAP values for model explainability.

        Args:
            model (Any): The trained model.
            data (pd.DataFrame): The data for which to explain predictions.
        """
        explainer = shap.Explainer(model)
        shap_values = explainer(data)
        shap.summary_plot(shap_values, data)

    def log_model(self, model: Any, params: dict) -> None:
        """
        Logs the trained model and parameters to MLflow.

        Args:
            model (Any): The trained model.
            params (dict): The hyperparameters used for training.
        """
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.xgboost.log_model(model, "model")