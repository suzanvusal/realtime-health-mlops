# Deployment Guide for Real-Time Smart Health Monitoring System

## Introduction

This deployment guide provides step-by-step instructions for deploying the Real-Time Smart Health Monitoring System using Kafka, Faust, Redis, XGBoost, PyTorch, MLflow, FastAPI, Evidently, and Airflow. 

## Prerequisites

Before deploying the system, ensure you have the following prerequisites:

- Docker and Docker Compose installed
- Kubernetes cluster set up (e.g., GKE, EKS, AKS)
- Helm installed for managing Kubernetes applications
- Access to a Redis instance
- Kafka broker running
- MLflow tracking server configured

## Deployment Steps

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/smart-health-monitoring.git
cd smart-health-monitoring
```

### Step 2: Build Docker Images

Build the Docker images for the FastAPI application and the Kafka consumer:

```bash
docker-compose build
```

### Step 3: Configure Environment Variables

Create a `.env` file in the root of the project with the following variables:

```plaintext
REDIS_URL=redis://your_redis_url
KAFKA_BROKER=your_kafka_broker_url
MLFLOW_TRACKING_URI=http://your_mlflow_tracking_server
```

### Step 4: Deploy to Kubernetes

Use Helm to deploy the application to your Kubernetes cluster. First, navigate to the `infra/k8s` directory:

```bash
cd infra/k8s
```

Then, install the Helm chart:

```bash
helm install smart-health-monitoring ./chart
```

### Step 5: Set Up Airflow

Deploy Airflow using the provided Helm chart. Ensure you have the correct configuration in `airflow/values.yaml`:

```yaml
executor: CeleryExecutor
dags:
  path: /usr/local/airflow/dags
```

Install Airflow:

```bash
helm install airflow ./airflow
```

### Step 6: Monitor with Evidently

To monitor model performance, configure Evidently in your FastAPI application. Ensure the endpoint for monitoring is set up correctly in your FastAPI routes.

### Step 7: Verify Deployment

After deployment, verify that all services are running correctly:

```bash
kubectl get pods
kubectl get services
```

### Step 8: Access the Application

Access the FastAPI application through the service exposed in your Kubernetes cluster. You can use port forwarding for local testing:

```bash
kubectl port-forward svc/smart-health-monitoring 8000:80
```

Visit `http://localhost:8000/docs` to access the FastAPI documentation.

## Conclusion

You have successfully deployed the Real-Time Smart Health Monitoring System. For further customization and scaling, refer to the individual service documentation and Kubernetes best practices.