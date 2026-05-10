import json
import logging
from fastapi import FastAPI, Request
from typing import Dict, Any
import redis
import random
import mlflow
import xgboost as xgb
import torch

app = FastAPI()
logger = logging.getLogger(__name__)

# Redis client for shadow logging
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Load models from MLflow
MODEL_A_URI = "models:/model_a/production"
MODEL_B_URI = "models:/model_b/production"

model_a = mlflow.pyfunc.load_model(MODEL_A_URI)
model_b = mlflow.pyfunc.load_model(MODEL_B_URI)

@app.post("/predict")
async def predict(request: Request) -> Dict[str, Any]:
    """
    A/B routing for model predictions and shadow logging.

    Args:
        request (Request): Incoming request containing input data.

    Returns:
        Dict[str, Any]: Prediction results from the selected model.
    """
    data = await request.json()
    model_choice = random.choice(['A', 'B'])
    
    if model_choice == 'A':
        prediction = model_a.predict(data)
    else:
        prediction = model_b.predict(data)

    # Shadow prediction logging
    log_shadow_prediction(data, prediction, model_choice)

    return {"model": model_choice, "prediction": prediction.tolist()}

def log_shadow_prediction(data: Dict[str, Any], prediction: Any, model_choice: str) -> None:
    """
    Log shadow predictions to Redis.

    Args:
        data (Dict[str, Any]): Input data for the prediction.
        prediction (Any): Prediction result from the model.
        model_choice (str): The model used for prediction ('A' or 'B').
    """
    log_entry = {
        "input": data,
        "prediction": prediction.tolist(),
        "model": model_choice
    }
    redis_client.lpush("shadow_predictions", json.dumps(log_entry))
    logger.info(f"Shadow prediction logged for model {model_choice}: {log_entry}")

@app.get("/model_comparison")
async def model_comparison() -> Dict[str, Any]:
    """
    Compare performance metrics of the two models.

    Returns:
        Dict[str, Any]: Comparison metrics of model A and model B.
    """
    # This is a placeholder for actual comparison logic
    metrics_a = {"accuracy": 0.95, "f1_score": 0.93}  # Example metrics for model A
    metrics_b = {"accuracy": 0.92, "f1_score": 0.90}  # Example metrics for model B

    return {
        "model_a": metrics_a,
        "model_b": metrics_b,
        "comparison": {
            "better_model": "A" if metrics_a["accuracy"] > metrics_b["accuracy"] else "B"
        }
    }