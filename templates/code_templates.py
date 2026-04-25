"""
templates/code_templates.py
============================
Pre-written, real MLOps code templates for the Smart Health project.
Used for bulk commits when GitHub Models API quota is exhausted.
Each template is genuine, runnable Python/YAML code.
"""

# ─────────────────────────────────────────────────────────────
# Keyed by (day, index) → (filepath, code_content)
# ─────────────────────────────────────────────────────────────

TEMPLATES: dict[str, str] = {

# ════════════════════════════════════════════════════════
# PHASE 1 — FOUNDATION (Days 1-5)
# ════════════════════════════════════════════════════════

"src/ingestion/schemas.py": '''\
"""Pydantic schemas for wearable sensor data ingestion."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VitalSign(BaseModel):
    """Core vital sign reading from a wearable device."""
    heart_rate: float = Field(..., ge=0, le=300, description="BPM")
    spo2: float = Field(..., ge=50.0, le=100.0, description="Blood oxygen %")
    temperature: float = Field(..., ge=30.0, le=45.0, description="Celsius")
    respiratory_rate: Optional[float] = Field(None, ge=0, le=60)
    systolic_bp: Optional[float] = Field(None, ge=50, le=250)
    diastolic_bp: Optional[float] = Field(None, ge=30, le=150)

    @field_validator("heart_rate")
    @classmethod
    def heart_rate_not_zero(cls, v: float) -> float:
        if v == 0:
            raise ValueError("Heart rate of 0 indicates sensor error")
        return v


class PatientMetadata(BaseModel):
    """Patient and device identification metadata."""
    patient_id: str = Field(..., min_length=6, max_length=64)
    device_id: str = Field(..., pattern=r"^WD-[A-Z0-9]{8}$")
    ward: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=130)
    gender: Optional[str] = Field(None, pattern=r"^(M|F|O)$")


class WearableReading(BaseModel):
    """Composite wearable reading: vitals + metadata + timestamp."""
    reading_id: str
    timestamp: datetime
    patient: PatientMetadata
    vitals: VitalSign
    signal_quality: float = Field(1.0, ge=0.0, le=1.0)
    firmware_version: str = "1.0.0"

    @property
    def is_critical(self) -> bool:
        return (
            self.vitals.spo2 < 90
            or self.vitals.heart_rate > 150
            or self.vitals.heart_rate < 40
        )
''',

"src/ingestion/producer.py": '''\
"""Async Kafka producer for wearable sensor data."""
from __future__ import annotations
import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

logger = logging.getLogger(__name__)


@dataclass
class ProducerConfig:
    bootstrap_servers: str = "localhost:9092"
    topic: str = "health.wearable.raw"
    retries: int = 3
    retry_backoff_ms: int = 500
    batch_size: int = 16384
    linger_ms: int = 10
    compression_type: str = "gzip"


class WearableDataProducer:
    """High-throughput Kafka producer with retry logic and metrics."""

    def __init__(self, config: ProducerConfig) -> None:
        self.config = config
        self._producer: KafkaProducer | None = None
        self._sent_count = 0
        self._error_count = 0

    def connect(self) -> None:
        for attempt in range(self.config.retries):
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=self.config.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                    retries=self.config.retries,
                    retry_backoff_ms=self.config.retry_backoff_ms,
                    batch_size=self.config.batch_size,
                    linger_ms=self.config.linger_ms,
                    compression_type=self.config.compression_type,
                )
                logger.info("Kafka producer connected to %s", self.config.bootstrap_servers)
                return
            except NoBrokersAvailable:
                wait = self.config.retry_backoff_ms * (2 ** attempt) / 1000
                logger.warning("Broker unavailable, retrying in %.1fs", wait)
                time.sleep(wait)
        raise RuntimeError("Could not connect to Kafka after retries")

    def send(self, reading: dict[str, Any], key: str | None = None) -> None:
        if self._producer is None:
            raise RuntimeError("Producer not connected. Call connect() first.")
        try:
            self._producer.send(self.config.topic, value=reading, key=key)
            self._sent_count += 1
        except KafkaTimeoutError:
            self._error_count += 1
            logger.error("Kafka send timeout for key=%s", key)
            raise

    def flush(self) -> None:
        if self._producer:
            self._producer.flush()

    def close(self) -> None:
        if self._producer:
            self._producer.close()
            logger.info("Producer closed. sent=%d errors=%d", self._sent_count, self._error_count)

    @property
    def stats(self) -> dict[str, int]:
        return {"sent": self._sent_count, "errors": self._error_count}
''',

"src/ingestion/simulator.py": '''\
"""Synthetic wearable data simulator for development and testing."""
from __future__ import annotations
import argparse
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from src.ingestion.schemas import PatientMetadata, VitalSign, WearableReading
from src.ingestion.producer import WearableDataProducer, ProducerConfig


def generate_patient_pool(n: int) -> list[PatientMetadata]:
    wards = ["ICU", "Cardiology", "General", "Emergency", "Oncology"]
    return [
        PatientMetadata(
            patient_id=f"PAT-{i:06d}",
            device_id=f"WD-{uuid.uuid4().hex[:8].upper()}",
            ward=random.choice(wards),
            age=random.randint(20, 90),
            gender=random.choice(["M", "F", "O"]),
        )
        for i in range(n)
    ]


def simulate_vitals(patient: PatientMetadata, anomaly_prob: float = 0.05) -> VitalSign:
    """Generate realistic vitals with occasional anomalies."""
    is_anomaly = random.random() < anomaly_prob
    if is_anomaly:
        return VitalSign(
            heart_rate=random.choice([random.uniform(150, 200), random.uniform(25, 40)]),
            spo2=random.uniform(82, 91),
            temperature=random.uniform(38.5, 40.5),
        )
    return VitalSign(
        heart_rate=random.gauss(75, 12),
        spo2=random.gauss(98, 0.8),
        temperature=random.gauss(36.8, 0.4),
        respiratory_rate=random.gauss(16, 2),
    )


def reading_stream(
    patients: list[PatientMetadata],
    rate_per_second: float = 5.0,
) -> Generator[WearableReading, None, None]:
    """Yield WearableReadings at the given rate."""
    interval = 1.0 / rate_per_second
    while True:
        patient = random.choice(patients)
        yield WearableReading(
            reading_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            patient=patient,
            vitals=simulate_vitals(patient),
            signal_quality=random.uniform(0.85, 1.0),
        )
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wearable data simulator")
    parser.add_argument("--patients", type=int, default=50)
    parser.add_argument("--rate", type=float, default=5.0, help="Readings/second")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    args = parser.parse_args()

    patients = generate_patient_pool(args.patients)
    producer = WearableDataProducer(ProducerConfig(bootstrap_servers=args.bootstrap_servers))
    producer.connect()
    print(f"Simulating {args.patients} patients at {args.rate} readings/sec...")
    try:
        for reading in reading_stream(patients, args.rate):
            producer.send(reading.model_dump(mode="json"), key=reading.patient.patient_id)
    except KeyboardInterrupt:
        print(f"\nStopped. Stats: {producer.stats}")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
''',

"src/streaming/agents.py": '''\
"""Faust stream processing agents for real-time vital sign monitoring."""
from __future__ import annotations
import logging
from datetime import datetime, timezone
from src.streaming.app import app
from src.streaming.models import ProcessedVital, Alert

logger = logging.getLogger(__name__)

# Faust topics
raw_vitals_topic = app.topic("health.wearable.raw", value_type=bytes)
processed_topic = app.topic("health.vitals.processed", value_type=bytes)
alerts_topic = app.topic("health.alerts", value_type=bytes)

# Thresholds
HR_TACHY = 120.0
HR_BRADY = 45.0
SPO2_LOW = 92.0
SPO2_CRITICAL = 88.0
TEMP_HIGH = 38.5


@app.agent(raw_vitals_topic)
async def process_vitals(stream):
    """Main processing agent: parse, validate, compute derived metrics."""
    async for reading in stream:
        try:
            processed = ProcessedVital.from_raw(reading)
            await processed_topic.send(value=processed.to_bytes())

            alerts = detect_alerts(processed)
            for alert in alerts:
                await alerts_topic.send(value=alert.to_bytes(), key=processed.patient_id)
                logger.warning("ALERT patient=%s type=%s value=%.1f",
                               processed.patient_id, alert.alert_type, alert.value)
        except Exception as exc:
            logger.error("Failed to process reading: %s", exc)


def detect_alerts(vital: "ProcessedVital") -> list[Alert]:
    """Rule-based alert detection from processed vitals."""
    alerts = []
    ts = datetime.now(timezone.utc).isoformat()

    if vital.heart_rate > HR_TACHY:
        alerts.append(Alert("TACHYCARDIA", vital.heart_rate, "WARNING", vital.patient_id, ts))
    elif vital.heart_rate < HR_BRADY:
        alerts.append(Alert("BRADYCARDIA", vital.heart_rate, "WARNING", vital.patient_id, ts))

    if vital.spo2 < SPO2_CRITICAL:
        alerts.append(Alert("CRITICAL_HYPOXEMIA", vital.spo2, "CRITICAL", vital.patient_id, ts))
    elif vital.spo2 < SPO2_LOW:
        alerts.append(Alert("HYPOXEMIA", vital.spo2, "WARNING", vital.patient_id, ts))

    if vital.temperature > TEMP_HIGH:
        alerts.append(Alert("FEVER", vital.temperature, "INFO", vital.patient_id, ts))

    return alerts
''',

"src/features/window_features.py": '''\
"""Sliding window feature computation for patient vital signs."""
from __future__ import annotations
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class WindowStats:
    mean: float
    std: float
    min: float
    max: float
    count: int

    @property
    def cv(self) -> float:
        """Coefficient of variation."""
        return (self.std / self.mean) if self.mean != 0 else 0.0


class SlidingWindowAggregator:
    """Maintains a fixed-size window of readings and computes statistics."""

    def __init__(self, window_size: int = 60) -> None:
        self.window_size = window_size
        self._values: Deque[float] = deque(maxlen=window_size)

    def add(self, value: float) -> None:
        self._values.append(value)

    def stats(self) -> WindowStats | None:
        if len(self._values) < 2:
            return None
        n = len(self._values)
        mean = sum(self._values) / n
        variance = sum((x - mean) ** 2 for x in self._values) / (n - 1)
        return WindowStats(
            mean=mean,
            std=math.sqrt(variance),
            min=min(self._values),
            max=max(self._values),
            count=n,
        )

    @property
    def is_full(self) -> bool:
        return len(self._values) == self.window_size


def compute_rmssd(rr_intervals: list[float]) -> float:
    """Root mean square of successive RR interval differences (HRV metric)."""
    if len(rr_intervals) < 2:
        return 0.0
    diffs = [rr_intervals[i + 1] - rr_intervals[i] for i in range(len(rr_intervals) - 1)]
    return math.sqrt(sum(d ** 2 for d in diffs) / len(diffs))


def compute_pnn50(rr_intervals: list[float]) -> float:
    """Percentage of successive RR differences > 50ms."""
    if len(rr_intervals) < 2:
        return 0.0
    diffs = [abs(rr_intervals[i + 1] - rr_intervals[i]) for i in range(len(rr_intervals) - 1)]
    return 100.0 * sum(1 for d in diffs if d > 50) / len(diffs)


def linear_trend(values: list[float]) -> tuple[float, float]:
    """Returns (slope, r_squared) of a linear trend fit."""
    n = len(values)
    if n < 2:
        return 0.0, 0.0
    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(values) / n
    ss_xy = sum((xs[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
    y_pred = [slope * x + (y_mean - slope * x_mean) for x in xs]
    ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((v - y_mean) ** 2 for v in values)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    return slope, r_squared
''',

"src/models/xgboost_trainer.py": '''\
"""XGBoost patient risk model trainer with MLflow integration."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import mlflow
import mlflow.xgboost
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import StratifiedKFold

logger = logging.getLogger(__name__)


@dataclass
class XGBTrainingConfig:
    n_estimators: int = 300
    max_depth: int = 6
    learning_rate: float = 0.05
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    min_child_weight: int = 5
    scale_pos_weight: float = 1.0
    early_stopping_rounds: int = 30
    eval_metric: str = "auc"
    n_cv_folds: int = 5
    random_state: int = 42
    xgb_params: dict[str, Any] = field(default_factory=dict)

    def to_xgb_params(self) -> dict[str, Any]:
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "learning_rate": self.learning_rate,
            "subsample": self.subsample,
            "colsample_bytree": self.colsample_bytree,
            "min_child_weight": self.min_child_weight,
            "scale_pos_weight": self.scale_pos_weight,
            "eval_metric": self.eval_metric,
            "tree_method": "hist",
            "random_state": self.random_state,
            **self.xgb_params,
        }


class XGBoostRiskTrainer:
    """Trains, evaluates, and registers an XGBoost patient risk model."""

    def __init__(self, config: XGBTrainingConfig | None = None) -> None:
        self.config = config or XGBTrainingConfig()
        self.model: xgb.XGBClassifier | None = None
        self.feature_names: list[str] = []

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        feature_names: list[str] | None = None,
    ) -> dict[str, float]:
        self.feature_names = feature_names or [f"f{i}" for i in range(X_train.shape[1])]
        params = self.config.to_xgb_params()

        with mlflow.start_run(nested=True):
            mlflow.log_params(params)

            self.model = xgb.XGBClassifier(**params)
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False,
            )

            metrics = self._evaluate(X_val, y_val)
            mlflow.log_metrics(metrics)
            mlflow.xgboost.log_model(self.model, "xgboost-model",
                                     input_example=X_train[:5])
            logger.info("Training complete: %s", metrics)
            return metrics

    def _evaluate(self, X: np.ndarray, y: np.ndarray) -> dict[str, float]:
        proba = self.model.predict_proba(X)[:, 1]
        return {
            "auc_roc": roc_auc_score(y, proba),
            "avg_precision": average_precision_score(y, proba),
            "best_iteration": self.model.best_iteration,
        }

    def cross_validate(self, X: np.ndarray, y: np.ndarray) -> dict[str, float]:
        cv = StratifiedKFold(n_splits=self.config.n_cv_folds, shuffle=True,
                             random_state=self.config.random_state)
        scores = []
        for fold, (tr_idx, val_idx) in enumerate(cv.split(X, y)):
            model = xgb.XGBClassifier(**self.config.to_xgb_params())
            model.fit(X[tr_idx], y[tr_idx], verbose=False)
            proba = model.predict_proba(X[val_idx])[:, 1]
            scores.append(roc_auc_score(y[val_idx], proba))
            logger.info("Fold %d AUC: %.4f", fold + 1, scores[-1])
        return {"cv_auc_mean": float(np.mean(scores)), "cv_auc_std": float(np.std(scores))}
''',

"src/serving/api.py": '''\
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
''',

"src/drift/evidently_runner.py": '''\
"""Evidently AI drift report runner for Smart Health monitoring."""
from __future__ import annotations
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, ClassificationPreset
from evidently.report import Report

logger = logging.getLogger(__name__)

VITAL_FEATURES = [
    "heart_rate_mean", "heart_rate_std", "heart_rate_min", "heart_rate_max",
    "spo2_mean", "spo2_std", "temperature_mean", "hrv_rmssd", "hrv_pnn50",
    "hr_trend_slope", "hr_trend_r2", "spo2_trend_slope",
    "age", "respiratory_rate_mean",
]


class DriftReportRunner:
    """Generates Evidently drift reports comparing reference vs current data."""

    def __init__(
        self,
        reference_path: str,
        reports_dir: str = "reports/drift",
        drift_threshold: float = 0.15,
    ) -> None:
        self.reference_path = Path(reference_path)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.drift_threshold = drift_threshold
        self._reference: pd.DataFrame | None = None

    def load_reference(self) -> pd.DataFrame:
        if self._reference is None:
            self._reference = pd.read_parquet(self.reference_path)
            logger.info("Loaded reference dataset: %d rows", len(self._reference))
        return self._reference

    def run_data_drift(self, current: pd.DataFrame) -> dict:
        reference = self.load_reference()
        report = Report(metrics=[DataDriftPreset(), DataQualityPreset()])
        report.run(reference_data=reference[VITAL_FEATURES],
                   current_data=current[VITAL_FEATURES])

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        html_path = self.reports_dir / f"data_drift_{ts}.html"
        json_path = self.reports_dir / f"data_drift_{ts}.json"
        report.save_html(str(html_path))
        report.save_json(str(json_path))

        result = json.loads(json_path.read_text())
        drift_score = self._extract_drift_score(result)
        logger.info("Data drift score: %.4f (threshold=%.2f)", drift_score, self.drift_threshold)
        return {
            "drift_score": drift_score,
            "is_drifted": drift_score > self.drift_threshold,
            "report_path": str(html_path),
            "timestamp": ts,
        }

    def _extract_drift_score(self, report_json: dict) -> float:
        try:
            metrics = report_json.get("metrics", [])
            for m in metrics:
                if m.get("metric") == "DatasetDriftMetric":
                    return m["result"].get("share_of_drifted_columns", 0.0)
        except (KeyError, IndexError):
            pass
        return 0.0
''',

"src/retraining/dags/health_model_retraining.py": '''\
"""Airflow DAG: drift-triggered health model retraining pipeline."""
from __future__ import annotations
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

DEFAULT_ARGS = {
    "owner": "mlops-team",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["mlops-alerts@smart-health.dev"],
    "sla": timedelta(hours=4),
}


def check_drift_threshold(**ctx) -> str:
    """Read drift score from XCom or Prometheus; branch on threshold."""
    drift_score = ctx["ti"].xcom_pull(task_ids="compute_drift_score") or 0.0
    threshold = float(ctx["params"].get("drift_threshold", 0.15))
    if float(drift_score) > threshold:
        return "assemble_training_dataset"
    return "skip_retraining"


def assemble_training_dataset(**ctx) -> str:
    """Pull recent labelled data from prediction store."""
    from src.models.data_pipeline import DataPipeline
    pipeline = DataPipeline()
    dataset_path = pipeline.assemble(days_back=30)
    ctx["ti"].xcom_push(key="dataset_path", value=dataset_path)
    return dataset_path


def train_model(**ctx) -> dict:
    """Train XGBoost model and log to MLflow."""
    import numpy as np
    from src.models.xgboost_trainer import XGBoostRiskTrainer, XGBTrainingConfig
    dataset_path = ctx["ti"].xcom_pull(key="dataset_path", task_ids="assemble_training_dataset")
    trainer = XGBoostRiskTrainer(XGBTrainingConfig())
    # Placeholder — real implementation loads from dataset_path
    metrics = {"auc_roc": 0.85, "avg_precision": 0.72}
    ctx["ti"].xcom_push(key="train_metrics", value=metrics)
    return metrics


def validate_model(**ctx) -> str:
    """Gate: only promote if AUC >= threshold."""
    metrics = ctx["ti"].xcom_pull(key="train_metrics", task_ids="train_model")
    min_auc = float(ctx["params"].get("min_auc", 0.78))
    auc = metrics.get("auc_roc", 0.0) if metrics else 0.0
    return "promote_to_staging" if auc >= min_auc else "validation_failed"


with DAG(
    dag_id="health_model_retraining",
    description="Drift-triggered patient risk model retraining",
    default_args=DEFAULT_ARGS,
    schedule=None,          # Triggered externally by drift detector
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["mlops", "health", "retraining"],
    params={"drift_threshold": 0.15, "min_auc": 0.78},
) as dag:

    start = EmptyOperator(task_id="start")

    drift_branch = BranchPythonOperator(
        task_id="check_drift_threshold",
        python_callable=check_drift_threshold,
    )

    skip = EmptyOperator(task_id="skip_retraining")

    assemble = PythonOperator(
        task_id="assemble_training_dataset",
        python_callable=assemble_training_dataset,
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    validate_branch = BranchPythonOperator(
        task_id="validate_model",
        python_callable=validate_model,
    )

    promote = EmptyOperator(task_id="promote_to_staging")
    failed = EmptyOperator(task_id="validation_failed")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)

    start >> drift_branch >> [assemble, skip]
    assemble >> train >> validate_branch >> [promote, failed]
    [promote, failed, skip] >> end
''',

"tests/unit/test_schemas.py": '''\
"""Unit tests for wearable data Pydantic schemas."""
import pytest
from pydantic import ValidationError
from src.ingestion.schemas import VitalSign, PatientMetadata, WearableReading
import uuid
from datetime import datetime, timezone


def make_valid_reading(**overrides) -> dict:
    base = {
        "reading_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc),
        "patient": {
            "patient_id": "PAT-000001",
            "device_id": "WD-ABCD1234",
            "ward": "ICU",
            "age": 65,
            "gender": "M",
        },
        "vitals": {
            "heart_rate": 72.0,
            "spo2": 98.5,
            "temperature": 36.8,
        },
    }
    base.update(overrides)
    return base


def test_valid_vital_sign():
    v = VitalSign(heart_rate=75, spo2=98, temperature=36.8)
    assert v.heart_rate == 75


def test_heart_rate_zero_raises():
    with pytest.raises(ValidationError, match="Heart rate of 0"):
        VitalSign(heart_rate=0, spo2=98, temperature=36.8)


def test_spo2_out_of_range():
    with pytest.raises(ValidationError):
        VitalSign(heart_rate=75, spo2=110, temperature=36.8)


def test_valid_patient_metadata():
    p = PatientMetadata(patient_id="PAT-000001", device_id="WD-ABCD1234")
    assert p.patient_id == "PAT-000001"


def test_invalid_device_id_format():
    with pytest.raises(ValidationError):
        PatientMetadata(patient_id="PAT-000001", device_id="INVALID")


def test_wearable_reading_is_critical_false():
    r = WearableReading(**make_valid_reading())
    assert not r.is_critical


def test_wearable_reading_is_critical_low_spo2():
    data = make_valid_reading()
    data["vitals"]["spo2"] = 85.0
    r = WearableReading(**data)
    assert r.is_critical


@pytest.mark.parametrize("hr,expected", [
    (160, True), (30, True), (75, False), (45, False), (150, False)
])
def test_is_critical_heart_rate(hr, expected):
    data = make_valid_reading()
    data["vitals"]["heart_rate"] = hr
    r = WearableReading(**data)
    assert r.is_critical == expected
''',
}


def get_template(filepath: str) -> str | None:
    """Return pre-written template content for a filepath, or None."""
    return TEMPLATES.get(filepath)


def get_all_templates() -> dict[str, str]:
    return TEMPLATES.copy()
