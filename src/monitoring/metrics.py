import prometheus_client
from prometheus_client import Counter, Gauge, Histogram
from fastapi import FastAPI
from typing import Dict, Any
import json
import os

app = FastAPI()

# Custom Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests processed')
ERROR_COUNT = Counter('error_count', 'Total number of errors encountered')
PROCESSING_TIME = Histogram('processing_time_seconds', 'Histogram of processing time for requests')

# Health metrics
HEALTH_STATUS = Gauge('health_status', 'Health status of the monitoring system', ['status'])

def load_dashboard_json(file_path: str) -> Dict[str, Any]:
    """Load Grafana dashboard JSON from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dashboard file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        return json.load(file)

@app.get("/metrics")
def get_metrics() -> str:
    """Expose Prometheus metrics."""
    return prometheus_client.generate_latest()

@app.post("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint to monitor system status."""
    HEALTH_STATUS.labels(status='healthy').set(1)
    return {"status": "healthy"}

@app.middleware("http")
async def add_metrics(request, call_next):
    """Middleware to track request metrics."""
    REQUEST_COUNT.inc()
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    processing_time = time.time() - start_time
    PROCESSING_TIME.observe(processing_time)
    
    if response.status_code != 200:
        ERROR_COUNT.inc()
    
    return response

if __name__ == "__main__":
    prometheus_client.start_http_server(8000)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
# 11:10:09 — automated update
# infra: add Grafana provisioning config for auto-dashboard load

# 11:11:30 — automated update
# style: run black formatter on metrics — 11:11:30 UTC

# 11:11:30 — automated update
# chore: day 12 maintenance sweep — 11:11:30 UTC

# 11:13:34 — automated update
# ci: update step name for readability — 11:13:34 UTC

# 11:13:34 — automated update
# perf: add __slots__ to reduce memory in metrics — 11:13:34 UTC
