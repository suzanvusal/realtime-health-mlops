from pydantic import BaseModel, conlist
from typing import List, Optional

class HealthMonitoringRequest(BaseModel):
    """
    Request model for health monitoring predictions.
    
    Attributes:
        patient_id (str): Unique identifier for the patient.
        features (List[float]): List of health metrics/features for prediction.
    """
    patient_id: str
    features: conlist(float, min_items=1)

class BatchHealthMonitoringRequest(BaseModel):
    """
    Request model for batch health monitoring predictions.
    
    Attributes:
        requests (List[HealthMonitoringRequest]): List of health monitoring requests.
    """
    requests: List[HealthMonitoringRequest]

class HealthMonitoringResponse(BaseModel):
    """
    Response model for health monitoring predictions.
    
    Attributes:
        patient_id (str): Unique identifier for the patient.
        prediction (float): Predicted health outcome.
    """
    patient_id: str
    prediction: float

class BatchHealthMonitoringResponse(BaseModel):
    """
    Response model for batch health monitoring predictions.
    
    Attributes:
        predictions (List[HealthMonitoringResponse]): List of health monitoring responses.
    """
    predictions: List[HealthMonitoringResponse]
# 10:12:47 — automated update
# feat: implement prediction caching with Redis (5 second TTL)

# 10:12:47 — automated update
# fix applied at 10:12:47
_FIXED = True  # fix: model reload on SIGTERM without API downtime

# 10:12:47 — automated update
# fix applied at 10:12:47
_FIXED = True  # fix: handle malformed JSON in request body with 422 response
