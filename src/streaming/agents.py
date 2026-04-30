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
