# Real-Time Smart Health Monitoring System with Drift-Aware ML

> A production-grade MLOps system that monitors patient wearable data in real time,
> detects model drift, and automatically triggers retraining pipelines.

## Architecture

```
Wearable Data → Kafka → Faust Stream Processing → Feature Engineering
                                                         ↓
                                              FastAPI Model Inference
                                                         ↓
                                              Prediction Logging
                                                         ↓
                                         Evidently Drift Detection
                                                         ↓
                                         Airflow Retraining DAG
                                                         ↓
                                         Canary Deployment → Production
```

## Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Data Ingestion     | Apache Kafka, Pydantic              |
| Stream Processing  | Faust, Redis                        |
| ML Training        | XGBoost, PyTorch LSTM, MLflow       |
| Serving            | FastAPI, Prometheus                 |
| Drift Detection    | Evidently AI, Grafana               |
| Orchestration      | Apache Airflow                      |
| Infrastructure     | Docker Compose, GitHub Actions      |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/smart-health-mlops.git
cd smart-health-mlops

# Start infrastructure
docker compose up -d

# Run the wearable data simulator
python -m src.ingestion.simulator --patients 100 --rate 10

# Open Grafana dashboards
open http://localhost:3000
```

## Project Progress

This project is built over 30 days with automated daily commits tracking
real development progress. See [docs/architecture.md](docs/architecture.md) for details.

## License

MIT
