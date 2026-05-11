import json
import logging
from typing import Any, Dict

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class Outcome(BaseModel):
    prediction_id: str
    outcome: str
    timestamp: str

@app.post("/ingest_outcome/")
async def ingest_outcome(outcome: Outcome) -> Dict[str, Any]:
    """
    Ingests the outcome of a prediction into the Redis store.

    Args:
        outcome (Outcome): The outcome data containing prediction_id, outcome, and timestamp.

    Returns:
        Dict[str, Any]: A response indicating success or failure.
    """
    try:
        # Create a structured log entry
        log_entry = {
            "prediction_id": outcome.prediction_id,
            "outcome": outcome.outcome,
            "timestamp": outcome.timestamp
        }

        # Store the log entry in Redis
        redis_client.lpush("outcome_logs", json.dumps(log_entry))
        logger.info(f"Outcome ingested: {log_entry}")

        return {"status": "success", "message": "Outcome ingested successfully."}
    except Exception as e:
        logger.error(f"Error ingesting outcome: {e}")
        raise HTTPException(status_code=500, detail="Error ingesting outcome.")

@app.get("/get_outcomes/")
async def get_outcomes(limit: int = 10) -> Dict[str, Any]:
    """
    Retrieves the latest outcomes from the Redis store.

    Args:
        limit (int): The number of outcomes to retrieve.

    Returns:
        Dict[str, Any]: A list of the latest outcomes.
    """
    try:
        outcomes = redis_client.lrange("outcome_logs", 0, limit - 1)
        return {"status": "success", "outcomes": [json.loads(outcome) for outcome in outcomes]}
    except Exception as e:
        logger.error(f"Error retrieving outcomes: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving outcomes.")
# 12:17:50 — automated update
# test: add assertion for return type in outcome_ingester — 12:17:50 UTC
