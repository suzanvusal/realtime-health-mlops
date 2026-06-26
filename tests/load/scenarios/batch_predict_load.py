import time
from typing import Any, Dict, List
import requests
from locust import HttpUser, task, between

class BatchPredictLoadTest(HttpUser):
    """Load test for batch prediction endpoint of the Smart Health Monitoring System."""
    
    wait_time = between(1, 3)
    base_url: str = "http://localhost:8000"  # Adjust based on your FastAPI server

    @task
    def batch_predict(self) -> None:
        """Simulate a batch prediction request."""
        payload = self.generate_batch_payload()
        start_time = time.time()
        
        response = requests.post(f"{self.base_url}/predict/batch", json=payload)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            print(f"Batch prediction successful: {response.json()}")
        else:
            print(f"Batch prediction failed: {response.status_code} - {response.text}")
        
        print(f"Latency: {latency:.2f} seconds")

    def generate_batch_payload(self) -> List[Dict[str, Any]]:
        """Generate a mock payload for batch predictions."""
        return [
            {
                "patient_id": f"patient_{i}",
                "data": {
                    "heart_rate": 70 + i,
                    "blood_pressure": [120 + i, 80 + i],
                    "temperature": 36.5 + (i * 0.1),
                }
            }
            for i in range(10)  # Adjust the range for larger batch sizes
        ]


if __name__ == "__main__":
    import os
    os.system("locust -f tests/load/locustfile.py")  # Run Locust server for load testing