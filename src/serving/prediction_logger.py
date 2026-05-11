import json
import logging
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import mlflow

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define Pydantic models for request and response
class PredictionLog(BaseModel):
    user_id: str
    prediction: Any
    ground_truth: Any
    timestamp: str

class FeedbackResponse(BaseModel):
    status: str
    message: str

@app.post("/log_prediction", response_model=FeedbackResponse)
async def log_prediction(prediction_log: PredictionLog) -> FeedbackResponse:
    """
    Log the prediction and ground truth to Redis and MLflow.

    Args:
        prediction_log (PredictionLog): The prediction log data.

    Returns:
        FeedbackResponse: Response indicating the status of the logging operation.
    """
    try:
        # Log to Redis
        redis_key = f"prediction:{prediction_log.user_id}:{prediction_log.timestamp}"
        redis_client.set(redis_key, prediction_log.json())
        
        # Log to MLflow
        with mlflow.start_run():
            mlflow.log_param("user_id", prediction_log.user_id)
            mlflow.log_param("timestamp", prediction_log.timestamp)
            mlflow.log_metric("prediction", prediction_log.prediction)
            mlflow.log_metric("ground_truth", prediction_log.ground_truth)

        logger.info(f"Logged prediction for user {prediction_log.user_id} at {prediction_log.timestamp}")
        return FeedbackResponse(status="success", message="Prediction logged successfully.")
    
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/get_predictions/{user_id}", response_model=List[PredictionLog])
async def get_predictions(user_id: str) -> List[PredictionLog]:
    """
    Retrieve all predictions for a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        List[PredictionLog]: A list of prediction logs for the user.
    """
    try:
        keys = redis_client.keys(f"prediction:{user_id}:*")
        predictions = [json.loads(redis_client.get(key)) for key in keys]
        return predictions
    
    except Exception as e:
        logger.error(f"Error retrieving predictions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")