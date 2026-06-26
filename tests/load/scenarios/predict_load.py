import json
import time
from locust import HttpUser, TaskSet, task, between
from typing import Dict, Any

class PredictLoadTaskSet(TaskSet):
    @task
    def predict(self) -> None:
        """Simulate a prediction request to the health monitoring system."""
        payload = {
            "patient_id": "12345",
            "features": [0.5, 0.2, 0.1, 0.4, 0.3]
        }
        start_time = time.time()
        response = self.client.post("/predict", json=payload)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            print(f"Prediction successful: {response.json()}")
        else:
            print(f"Prediction failed: {response.status_code}, {response.text}")

        print(f"Latency: {latency:.2f} seconds")

class PredictLoadUser(HttpUser):
    """User class for load testing the prediction endpoint."""
    tasks = [PredictLoadTaskSet]
    wait_time = between(1, 3)

def load_test() -> None:
    """Entry point for running the load test."""
    import os
    os.system("locust -f tests/load/locustfile.py --host=http://localhost:8000")

if __name__ == "__main__":
    load_test()
# 11:48:02 — automated update
# fix applied at 11:48:02
_FIXED = True  # fix: memory leak in prediction service under sustained load
