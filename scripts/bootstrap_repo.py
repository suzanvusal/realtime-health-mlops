#!/usr/bin/env python3
"""
Bootstrap Script — Run this ONCE locally to set up your GitHub repo.
========================================================================
This script:
1. Creates all required directories
2. Writes base configuration files
3. Makes the initial commit
4. Pushes to your GitHub remote

Usage:
    python3 scripts/bootstrap_repo.py --repo https://github.com/YOUR_USERNAME/smart-health-mlops.git
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# ─────────────────────────────────────────────
# Directory structure
# ─────────────────────────────────────────────
DIRS = [
    "src/ingestion", "src/streaming", "src/features",
    "src/models", "src/serving", "src/drift", "src/retraining",
    "src/monitoring",
    "infra/docker", "infra/k8s", "infra/airflow",
    "infra/grafana/dashboards", "infra/grafana/provisioning",
    "infra/prometheus",
    "tests/unit", "tests/integration", "tests/load",
    "notebooks", "docs/runbooks", "scripts", "configs",
    ".github/workflows", ".automation_state", "plan"
]

# ─────────────────────────────────────────────
# Base files
# ─────────────────────────────────────────────
BASE_FILES = {
    "README.md": """\
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
""",

    "pyproject.toml": """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "smart-health-mlops"
version = "0.1.0"
description = "Real-Time Smart Health Monitoring System with Drift-Aware ML"
requires-python = ">=3.11"
dependencies = [
    "kafka-python>=2.0.2",
    "faust-streaming>=0.10.14",
    "redis>=5.0.1",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "httpx>=0.25.2",
    "xgboost>=2.0.2",
    "torch>=2.1.0",
    "pytorch-lightning>=2.1.2",
    "mlflow>=2.9.2",
    "evidently>=0.4.11",
    "apache-airflow>=2.7.3",
    "prometheus-client>=0.19.0",
    "optuna>=3.4.0",
    "shap>=0.43.0",
    "numpy>=1.26.2",
    "pandas>=2.1.4",
    "scikit-learn>=1.3.2",
    "asyncpg>=0.29.0",
    "orjson>=3.9.10",
    "pyyaml>=6.0.1",
    "jinja2>=3.1.2",
    "anthropic>=0.8.0",
    "gitpython>=3.1.40",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "hypothesis>=6.92.1",
    "fakeredis>=2.20.0",
    "locust>=2.19.1",
    "black>=23.11.0",
    "ruff>=0.1.7",
    "mypy>=1.7.1",
    "pre-commit>=3.5.0",
    "freezegun>=1.3.1",
    "mutmut>=2.4.3",
    "pip-audit>=2.6.1",
]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]
""",

    "docker-compose.yml": """\
version: "3.9"

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "2181"]
      interval: 10s
      retries: 5

  kafka:
    image: confluentinc/cp-kafka:7.5.1
    depends_on:
      zookeeper:
        condition: service_healthy
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    volumes:
      - kafka_data:/var/lib/kafka/data
    healthcheck:
      test: ["CMD", "kafka-topics", "--bootstrap-server", "localhost:9092", "--list"]
      interval: 15s
      retries: 10

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  mlflow:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile.mlflow
    ports:
      - "5000:5000"
    environment:
      MLFLOW_BACKEND_STORE_URI: postgresql://mlflow:mlflow@postgres:5432/mlflow
      MLFLOW_ARTIFACT_ROOT: /mlflow/artifacts
    depends_on:
      - postgres
    volumes:
      - mlflow_artifacts:/mlflow/artifacts

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: mlflow
      POSTGRES_DB: mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlflow"]
      interval: 10s
      retries: 5

  prometheus:
    image: prom/prometheus:v2.47.2
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=15d'

  grafana:
    image: grafana/grafana:10.2.2
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_USERS_ALLOW_SIGN_UP: "false"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infra/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./infra/grafana/provisioning:/etc/grafana/provisioning

volumes:
  zookeeper_data:
  kafka_data:
  redis_data:
  mlflow_artifacts:
  postgres_data:
  prometheus_data:
  grafana_data:

networks:
  default:
    name: smart-health-network
""",

    "Makefile": """\
.PHONY: up down logs test lint format type-check clean

up:
\tdocker compose up -d
\t@echo "✓ All services started"

down:
\tdocker compose down

logs:
\tdocker compose logs -f

test:
\tpytest tests/ -v --cov=src --cov-report=term-missing

lint:
\truff check src/ tests/

format:
\tblack src/ tests/

type-check:
\tmypy src/

simulate:
\tpython -m src.ingestion.simulator --patients 50 --rate 5

serve:
\tuvicorn src.serving.api:app --reload --port 8000

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -name "*.pyc" -delete
\tfind . -name ".mypy_cache" -exec rm -rf {} +
""",

    ".pre-commit-config.yaml": """\
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.7
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-PyYAML]
""",

    "configs/base_config.yaml": """\
kafka:
  bootstrap_servers: "localhost:9092"
  topics:
    wearable_raw: "health.wearable.raw"
    processed_vitals: "health.vitals.processed"
    alerts: "health.alerts"
    predictions: "health.predictions"
  consumer_group: "smart-health-consumers"
  auto_offset_reset: "latest"

redis:
  host: "localhost"
  port: 6379
  db: 0
  max_connections: 20
  feature_ttl_seconds: 3600

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "smart-health-monitoring"
  model_name: "patient-risk-scorer"

serving:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  prediction_cache_ttl: 5

monitoring:
  prometheus_port: 8001
  grafana_url: "http://localhost:3000"
""",

    "src/__init__.py": '"""Smart Health MLOps System."""\n__version__ = "0.1.0"\n',
    "src/ingestion/__init__.py": '"""Wearable data ingestion package."""\n',
    "src/streaming/__init__.py": '"""Stream processing package."""\n',
    "src/features/__init__.py": '"""Feature engineering package."""\n',
    "src/models/__init__.py": '"""ML model training package."""\n',
    "src/serving/__init__.py": '"""Model serving package."""\n',
    "src/drift/__init__.py": '"""Drift detection package."""\n',
    "src/retraining/__init__.py": '"""Automated retraining package."""\n',
    "src/monitoring/__init__.py": '"""Monitoring and metrics package."""\n',
    "tests/__init__.py": "",
    "tests/unit/__init__.py": "",
    "tests/integration/__init__.py": "",
    "tests/load/__init__.py": "",

    ".gitignore": """\
# Python
__pycache__/
*.py[cod]
*.pyo
.Python
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
venv/
env/

# MLflow
mlruns/
mlflow.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.hypothesis/
*.mutmut-cache

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Docker
.docker/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.*
!.env.example

# Automation
.automation_state/*.json

# OS
.DS_Store
Thumbs.db
""",

    ".env.example": """\
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_USER=mlflow
POSTGRES_PASSWORD=mlflow
POSTGRES_DB=mlflow

# Anthropic (for automation only)
ANTHROPIC_API_KEY=your-api-key-here

# Alerting
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
PAGERDUTY_API_KEY=your-pagerduty-key
""",

    "infra/docker/Dockerfile.mlflow": """\
FROM python:3.11-slim

RUN pip install mlflow==2.9.2 psycopg2-binary boto3

EXPOSE 5000

CMD ["mlflow", "server", \
     "--backend-store-uri", "${MLFLOW_BACKEND_STORE_URI}", \
     "--artifact-root", "${MLFLOW_ARTIFACT_ROOT}", \
     "--host", "0.0.0.0", \
     "--port", "5000"]
""",

    "infra/prometheus/prometheus.yml": """\
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: smart-health-serving
    static_configs:
      - targets: ['host.docker.internal:8001']

  - job_name: kafka
    static_configs:
      - targets: ['kafka:9101']

  - job_name: redis
    static_configs:
      - targets: ['redis:9121']
""",

    ".automation_state/.gitkeep": "",
}


# ─────────────────────────────────────────────
# Git helpers
# ─────────────────────────────────────────────
def run(cmd: list[str], cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  WARN: {' '.join(cmd)}\n  {result.stderr[:200]}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Bootstrap the Smart Health MLOps repo")
    parser.add_argument("--repo", type=str, required=True,
                        help="Your GitHub remote URL, e.g. https://github.com/USER/smart-health-mlops.git")
    args = parser.parse_args()

    print("\n🚀 Bootstrapping Smart Health MLOps repo...")
    print(f"   Remote: {args.repo}\n")

    # Create directories
    print("📁 Creating directory structure...")
    for d in DIRS:
        Path(d).mkdir(parents=True, exist_ok=True)
        # Add .gitkeep so directories are tracked
        keep = Path(d) / ".gitkeep"
        if not any(Path(d).iterdir()):
            keep.touch()
    print(f"   ✓ {len(DIRS)} directories created")

    # Write base files
    print("\n📝 Writing base files...")
    for filepath, content in BASE_FILES.items():
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"   ✓ {len(BASE_FILES)} files written")

    # Git init
    print("\n🔧 Initialising Git...")
    if not Path(".git").exists():
        run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "MLOps Engineer"])
    run(["git", "config", "user.email", "mlops@smart-health.dev"])

    # Add remote
    run(["git", "remote", "remove", "origin"])
    run(["git", "remote", "add", "origin", args.repo])
    print(f"   ✓ Remote set to {args.repo}")

    # Initial commit
    print("\n📦 Making initial commit...")
    run(["git", "add", "-A"])
    run(["git", "commit", "-m",
         "chore: bootstrap Smart Health MLOps project structure\n\n"
         "- 30-day MLOps project: Real-Time Smart Health Monitoring\n"
         "- Stack: Kafka, Faust, Redis, XGBoost, LSTM, FastAPI\n"
         "- MLflow tracking, Evidently drift detection, Airflow retraining\n"
         "- Full GitHub Actions CI/CD automation"])

    # Push
    print("\n🚀 Pushing to GitHub...")
    result = run(["git", "push", "-u", "origin", "main"])
    if result.returncode == 0:
        print("   ✓ Successfully pushed to GitHub!")
    else:
        print("   ⚠ Push failed — check your PAT and repo URL")
        print("     Run manually: git push -u origin main")

    print("\n" + "="*60)
    print("  ✅ Bootstrap complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Go to GitHub → Settings → Secrets → Actions")
    print("  2. Add secret: ANTHROPIC_API_KEY = your Anthropic key")
    print("  3. Add secret: AUTOMATION_PAT = GitHub PAT with repo write access")
    print("  4. The workflow runs daily at 9:00 AM UTC automatically")
    print("  5. Or trigger manually: Actions → Daily MLOps Commit Automation → Run workflow")
    print()


if __name__ == "__main__":
    main()
