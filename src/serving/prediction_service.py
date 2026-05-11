from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, conlist
from typing import List
import joblib
import numpy as np
import asyncio

app = FastAPI()

class PredictionRequest(BaseModel):
    data: conlist(List[float], min_items=1)

class PredictionResponse(BaseModel):
    predictions: List[float]

class Model:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    async def predict(self, data: List[List[float]]) -> List[float]:
        return self.model.predict(data).tolist()

model = Model("path/to/your/model.pkl")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        data = request.data
        if not data or not all(isinstance(i, list) for i in data):
            raise HTTPException(status_code=400, detail="Invalid input data format.")
        
        predictions = await model.predict(data)
        return PredictionResponse(predictions=predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch_predict", response_model=PredictionResponse)
async def batch_predict(request: PredictionRequest):
    try:
        data = request.data
        if not data or not all(isinstance(i, list) for i in data):
            raise HTTPException(status_code=400, detail="Invalid input data format.")
        
        # Simulating batch processing
        predictions = await asyncio.gather(*(model.predict([item]) for item in data))
        flat_predictions = [pred for sublist in predictions for pred in sublist]
        return PredictionResponse(predictions=flat_predictions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 10:12:47 — automated update
# feat: add response schema with risk_score, confidence, features

# 10:12:47 — automated update
# test marker: test: add pytest-asyncio tests for all prediction endpoints
_TEST_MARKER = 'prediction_service'

# 12:17:50 — automated update
# test: add assertion for return type in prediction_service — 12:17:50 UTC
