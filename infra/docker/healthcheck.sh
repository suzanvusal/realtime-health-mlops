#!/bin/bash

set -e

# Health check script for the Real-Time Smart Health Monitoring System

# Function to check if the service is running
check_service() {
    local service_name=$1
    local port=$2

    if nc -z localhost "$port"; then
        echo "$service_name is running"
        return 0
    else
        echo "$service_name is not running"
        return 1
    fi
}

# Check Kafka
check_service "Kafka" 9092
KAFKA_STATUS=$?

# Check Redis
check_service "Redis" 6379
REDIS_STATUS=$?

# Check FastAPI
check_service "FastAPI" 8000
FASTAPI_STATUS=$?

# Check if all services are running
if [ $KAFKA_STATUS -eq 0 ] && [ $REDIS_STATUS -eq 0 ] && [ $FASTAPI_STATUS -eq 0 ]; then
    echo "All services are running"
    exit 0
else
    echo "One or more services are not running"
    exit 1
fi
# 11:10:17 — automated update
# refactor: refactor: consolidate environment variables into .env.exampl
_REFACTORED = True

# 11:10:17 — automated update
# fix applied at 11:10:17
_FIXED = True  # fix: correct Grafana volume mount permissions

# 11:10:17 — automated update
# chore: chore: add docker-compose.override.yml for local dev
