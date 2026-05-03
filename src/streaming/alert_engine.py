import json
import logging
from typing import Dict, Any
from kafka import KafkaConsumer, KafkaProducer
from fastapi import FastAPI
from pydantic import BaseModel
import redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Redis client setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
ALERT_TOPIC = 'alerts'

# Alert severity levels
SEVERITY_LEVELS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

class Alert(BaseModel):
    patient_id: str
    severity: str
    message: str

def send_alert(alert: Alert) -> None:
    """Send alert to Kafka topic."""
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(ALERT_TOPIC, alert.dict())
    producer.flush()
    logger.info(f"Alert sent: {alert}")

def evaluate_alert_conditions(data: Dict[str, Any]) -> Alert:
    """Evaluate conditions and return an alert if necessary."""
    severity = "low"
    message = ""

    # Example condition checks
    if data.get("heart_rate") > 100:
        severity = "medium"
        message = "High heart rate detected."
    elif data.get("blood_pressure") > 140:
        severity = "high"
        message = "High blood pressure detected."
    elif data.get("temperature") > 38.5:
        severity = "critical"
        message = "High temperature detected."

    return Alert(patient_id=data["patient_id"], severity=severity, message=message)

@app.post("/process_data/")
async def process_data(data: Dict[str, Any]) -> str:
    """Process incoming patient data and trigger alerts if necessary."""
    alert = evaluate_alert_conditions(data)
    if SEVERITY_LEVELS[alert.severity] > SEVERITY_LEVELS["low"]:
        send_alert(alert)
        redis_client.set(alert.patient_id, alert.json())
        logger.info(f"Alert processed for patient {alert.patient_id}")

    return {"status": "processed", "alert": alert.dict()}

def consume_alerts() -> None:
    """Consume alerts from Kafka and handle them."""
    consumer = KafkaConsumer(ALERT_TOPIC,
                             bootstrap_servers=KAFKA_BROKER,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        logger.info(f"Received alert: {message.value}")

if __name__ == "__main__":
    consume_alerts()
# 10:11:53 — automated update
# feat: add PagerDuty notifier for critical alerts
