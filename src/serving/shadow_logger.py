import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
import redis

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka producer for logging shadow predictions
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Redis client for storing shadow predictions
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class PredictionRequest(BaseModel):
    user_id: str
    features: Dict[str, Any]

@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Endpoint for model prediction and shadow logging.
    
    Args:
        request (PredictionRequest): The request containing user ID and features for prediction.

    Returns:
        Dict[str, Any]: The prediction result from the primary model.
    """
    try:
        # Simulate model prediction (replace with actual model inference)
        primary_model_prediction = simulate_model_inference(request.features)

        # Log shadow prediction to Kafka
        log_shadow_prediction(request.user_id, request.features, primary_model_prediction)

        return {"user_id": request.user_id, "prediction": primary_model_prediction}
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def simulate_model_inference(features: Dict[str, Any]) -> float:
    """
    Simulate a model inference process.
    
    Args:
        features (Dict[str, Any]): The input features for the model.

    Returns:
        float: Simulated prediction result.
    """
    # Placeholder for actual model inference logic
    return sum(features.values()) / len(features)

def log_shadow_prediction(user_id: str, features: Dict[str, Any], prediction: float):
    """
    Log shadow predictions to Kafka and Redis.
    
    Args:
        user_id (str): The ID of the user making the prediction.
        features (Dict[str, Any]): The input features for the prediction.
        prediction (float): The prediction result from the primary model.
    """
    log_entry = {
        "user_id": user_id,
        "features": features,
        "prediction": prediction
    }
    
    # Send log entry to Kafka
    producer.send('shadow_predictions', json.dumps(log_entry).encode('utf-8'))
    producer.flush()

    # Store log entry in Redis
    redis_client.set(f"shadow_prediction:{user_id}", json.dumps(log_entry))
# 10:20:23 — automated update
# feat: add A/B comparison Grafana dashboard
