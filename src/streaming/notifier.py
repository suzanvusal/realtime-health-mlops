import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

# Kafka producer configuration
KAFKA_BROKER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

class Notification(BaseModel):
    user_id: str
    severity: str
    message: str

def send_notification(notification: Notification) -> None:
    """Send notification to Kafka topic."""
    try:
        notification_data = notification.json().encode('utf-8')
        producer.send('notifications', notification_data)
        producer.flush()
        logger.info(f"Notification sent: {notification}")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

@app.post("/notify")
async def notify(notification: Notification):
    """Endpoint to receive notifications and route them."""
    severity_levels = {"low", "medium", "high"}
    
    if notification.severity not in severity_levels:
        raise HTTPException(status_code=400, detail="Invalid severity level")

    send_notification(notification)
    return {"status": "Notification sent", "notification": notification}

def load_alert_rules(file_path: str) -> Dict[str, Any]:
    """Load alert rules from a YAML file."""
    import yaml
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

@app.on_event("startup")
def startup_event():
    """Load alert rules on startup."""
    try:
        rules = load_alert_rules('configs/alert_rules.yaml')
        logger.info(f"Alert rules loaded: {rules}")
    except Exception as e:
        logger.error(f"Error loading alert rules: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 10:11:53 — automated update
# feat: add alert audit log to PostgreSQL
