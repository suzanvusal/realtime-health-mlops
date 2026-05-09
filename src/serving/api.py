"""FastAPI model serving application for patient risk inference."""
from __future__ import annotations
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any
import mlflow.pyfunc
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Prometheus metrics
PREDICTION_COUNTER = Counter("predictions_total", "Total predictions served", ["status"])
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency",
                                buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0])
MODEL_VERSION_GAUGE = Counter("model_version_loads_total", "Model version loads", ["version"])

# Global model state
_model: mlflow.pyfunc.PythonModel | None = None
_model_version: str = "unknown"


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _model, _model_version
    model_uri = os.getenv("MLFLOW_MODEL_URI", "models:/patient-risk-scorer/Production")
    try:
        _model = mlflow.pyfunc.load_model(model_uri)
        _model_version = os.getenv("MODEL_VERSION", "latest")
        MODEL_VERSION_GAUGE.labels(version=_model_version).inc()
        logger.info("Model loaded from %s (version=%s)", model_uri, _model_version)
    except Exception as exc:
        logger.warning("Model load failed: %s — serving will return 503", exc)
    yield
    logger.info("Shutting down serving API")


app = FastAPI(
    title="Smart Health Patient Risk API",
    version="1.0.0",
    lifespan=lifespan,
)


class PredictionRequest(BaseModel):
    patient_id: str
    features: dict[str, float]


class PredictionResponse(BaseModel):
    patient_id: str
    risk_score: float
    risk_level: str
    model_version: str
    latency_ms: float


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    start = time.perf_counter()
    try:
        import pandas as pd
        df = pd.DataFrame([request.features])
        score = float(_model.predict(df)[0])
        latency = (time.perf_counter() - start) * 1000
        PREDICTION_COUNTER.labels(status="success").inc()
        PREDICTION_LATENCY.observe(latency / 1000)
        level = "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW"
        return PredictionResponse(
            patient_id=request.patient_id,
            risk_score=round(score, 4),
            risk_level=level,
            model_version=_model_version,
            latency_ms=round(latency, 2),
        )
    except Exception as exc:
        PREDICTION_COUNTER.labels(status="error").inc()
        logger.error("Prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": _model is not None, "version": _model_version}


@app.get("/metrics")
async def metrics():
    from fastapi.responses import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# 10:12:47 — automated update
# feat: add request ID tracing header for observability
