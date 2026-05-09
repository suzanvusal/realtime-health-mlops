from pydantic import BaseModel
from typing import List, Any, Dict


class HealthMonitoringResponse(BaseModel):
    """Response model for health monitoring predictions."""
    patient_id: str
    predictions: List[Dict[str, Any]]
    status: str
    message: str


class BatchHealthMonitoringResponse(BaseModel):
    """Response model for batch health monitoring predictions."""
    results: List[HealthMonitoringResponse]
    overall_status: str
    overall_message: str


class ErrorResponse(BaseModel):
    """Error response model for handling errors."""
    detail: str


class PredictionResponse(BaseModel):
    """Response model for a single prediction."""
    patient_id: str
    prediction: float
    status: str
    message: str


class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    predictions: List[PredictionResponse]
    overall_status: str
    overall_message: str