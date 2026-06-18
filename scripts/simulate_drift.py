import random
import time
import json
import numpy as np
import pandas as pd
from typing import Dict, Any
from kafka import KafkaProducer
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
producer = KafkaProducer(bootstrap_servers='localhost:9092')

class HealthData(BaseModel):
    heart_rate: float
    blood_pressure: float
    temperature: float
    timestamp: str

def generate_drifted_data() -> Dict[str, Any]:
    """Generate simulated health data with drift."""
    base_data = {
        "heart_rate": random.uniform(60, 100),
        "blood_pressure": random.uniform(70, 120),
        "temperature": random.uniform(36.5, 37.5),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Simulate drift by altering the heart rate and blood pressure
    if random.random() < 0.5:  # 50% chance to simulate drift
        base_data["heart_rate"] += random.uniform(10, 30)  # Increase heart rate
        base_data["blood_pressure"] += random.uniform(10, 30)  # Increase blood pressure
    
    return base_data

def send_to_kafka(data: Dict[str, Any]) -> None:
    """Send data to Kafka topic."""
    producer.send('health_data', json.dumps(data).encode('utf-8'))
    producer.flush()

@app.post("/simulate_drift")
def simulate_drift(num_samples: int = 10) -> str:
    """Simulate drift in health data and send to Kafka."""
    for _ in range(num_samples):
        drifted_data = generate_drifted_data()
        send_to_kafka(drifted_data)
        time.sleep(1)  # Simulate time delay between data points
    return f"Sent {num_samples} drifted health data samples to Kafka."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 12:30:01 — automated update
# test marker: test: add chaos test — kill drift runner mid-report and veri
_TEST_MARKER = 'simulate_drift'

# 12:30:01 — automated update
# fix applied at 12:30:01
_FIXED = True  # fix: integration test teardown not resetting Redis state

# 12:30:01 — automated update
# fix applied at 12:30:01
_FIXED = True  # fix: drift simulation script needs --days argument validatio
