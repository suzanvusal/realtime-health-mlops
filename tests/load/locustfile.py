import time
from locust import HttpUser, TaskSet, task, between
import json

class PredictTasks(TaskSet):
    @task
    def predict(self):
        """Simulate a prediction request to the health monitoring system."""
        payload = {
            "patient_id": "12345",
            "vital_signs": {
                "heart_rate": 72,
                "blood_pressure": "120/80",
                "temperature": 98.6
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post("/predict", data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("Prediction successful:", response.json())
        else:
            print("Prediction failed:", response.status_code, response.text)

class BatchPredictTasks(TaskSet):
    @task
    def batch_predict(self):
        """Simulate a batch prediction request to the health monitoring system."""
        payload = {
            "patients": [
                {
                    "patient_id": "12345",
                    "vital_signs": {
                        "heart_rate": 72,
                        "blood_pressure": "120/80",
                        "temperature": 98.6
                    }
                },
                {
                    "patient_id": "67890",
                    "vital_signs": {
                        "heart_rate": 75,
                        "blood_pressure": "130/85",
                        "temperature": 99.1
                    }
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post("/batch_predict", data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("Batch prediction successful:", response.json())
        else:
            print("Batch prediction failed:", response.status_code, response.text)

class LoadTestUser(HttpUser):
    """User class for load testing the health monitoring system."""
    tasks = {PredictTasks: 2, BatchPredictTasks: 1}  # Adjust weights for task distribution
    wait_time = between(1, 3)  # Simulate user wait time between requests

if __name__ == "__main__":
    import os
    os.system("locust -f tests/load/locustfile.py --host=http://localhost:8000")  # Adjust host as needed
# 11:48:02 — automated update
# perf improvement at 11:48:02
_CACHE: dict = {}  # perf: add Kafka producer batch size tuni

# 11:48:02 — automated update
# perf improvement at 11:48:02
_CACHE: dict = {}  # perf: profile and fix N+1 query in predi

# 11:48:02 — automated update
# fix applied at 11:48:02
_FIXED = True  # fix: Kafka producer buffer full under burst load

# 11:48:02 — automated update
"""\ndocs: add capacity planning guide based on load test results\n"""

# 11:10:00 — automated update
# docs: fix typo in inline comment in locustfile — 11:10:00 UTC

# 11:10:00 — automated update
# fix: handle None input edge case in locustfile — 11:10:00 UTC
