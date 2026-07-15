# Deployment Guide for Real-Time Smart Health Monitoring System

## Overview

This document provides a comprehensive guide for deploying the Real-Time Smart Health Monitoring System. It covers the necessary steps to set up the environment, deploy the services, and ensure that the system runs smoothly.

## Prerequisites

Before deploying the system, ensure that you have the following:

- Kubernetes cluster (e.g., GKE, EKS, AKS)
- kubectl installed and configured
- Helm installed
- Docker installed
- Access to a Kafka broker
- Redis instance
- MLflow server running
- Airflow instance for orchestration

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-health-monitoring.git
cd smart-health-monitoring
```

### 2. Build Docker Images

Navigate to the `services` directory and build the Docker images for each service.

```bash
cd services
docker build -t health-monitoring-api ./api
docker build -t health-monitoring-worker ./worker
```

### 3. Push Docker Images to Registry

Push the built images to your Docker registry.

```bash
docker tag health-monitoring-api your-registry/health-monitoring-api
docker push your-registry/health-monitoring-api

docker tag health-monitoring-worker your-registry/health-monitoring-worker
docker push your-registry/health-monitoring-worker
```

### 4. Deploy Kafka

Use Helm to deploy Kafka in your Kubernetes cluster.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka bitnami/kafka
```

### 5. Deploy Redis

Deploy Redis using Helm.

```bash
helm install redis bitnami/redis
```

### 6. Deploy MLflow

Deploy MLflow using the following command:

```bash
kubectl apply -f infra/mlflow/deployment.yaml
```

### 7. Deploy Airflow

Deploy Airflow using Helm.

```bash
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow
```

### 8. Deploy FastAPI Application

Create a Kubernetes deployment for the FastAPI application.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-monitoring-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: health-monitoring-api
  template:
    metadata:
      labels:
        app: health-monitoring-api
    spec:
      containers:
      - name: health-monitoring-api
        image: your-registry/health-monitoring-api
        ports:
        - containerPort: 8000
```

### 9. Expose the FastAPI Service

Create a service to expose the FastAPI application.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: health-monitoring-api
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: health-monitoring-api
```

### 10. Monitor and Maintain

After deployment, monitor the services using Kubernetes dashboard or any monitoring tool of your choice. Ensure that logs are being captured and that the system is functioning as expected.

## Conclusion

This deployment guide provides the necessary steps to deploy the Real-Time Smart Health Monitoring System. Ensure that you follow each step carefully and monitor the system for any issues post-deployment.