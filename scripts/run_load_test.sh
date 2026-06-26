#!/bin/bash

# run_load_test.sh
# Script to run load tests using Locust for the Real-Time Smart Health Monitoring System

set -e

# Define the host and port for the FastAPI application
HOST="http://localhost:8000"
LOCUSTFILE="tests/load/locustfile.py"
OUTPUT_DIR="tests/load/results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULT_FILE="${OUTPUT_DIR}/load_test_results_${TIMESTAMP}.html"

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

# Function to display usage
usage() {
    echo "Usage: $0 [--host HOST] [--locustfile LOCUSTFILE] [--output-dir OUTPUT_DIR]"
    echo "Options:"
    echo "  --host HOST          Specify the host for the FastAPI application (default: http://localhost:8000)"
    echo "  --locustfile FILE    Specify the locustfile to use (default: tests/load/locustfile.py)"
    echo "  --output-dir DIR     Specify the output directory for results (default: tests/load/results)"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --host) HOST="$2"; shift ;;
        --locustfile) LOCUSTFILE="$2"; shift ;;
        --output-dir) OUTPUT_DIR="$2"; shift ;;
        *) usage ;;
    esac
    shift
done

# Run Locust load test
echo "Starting load test on ${HOST} using ${LOCUSTFILE}..."
locust -f "${LOCUSTFILE}" --host="${HOST}" --html="${RESULT_FILE}" --headless -u 100 -r 10 --run-time 1m

# Check if the load test was successful
if [[ $? -eq 0 ]]; then
    echo "Load test completed successfully. Results saved to ${RESULT_FILE}"
else
    echo "Load test failed."
    exit 1
fi

# Optionally, you can add commands to analyze results or send notifications here
# e.g., send_email_notification "${RESULT_FILE}" 

exit 0
# 11:48:02 — automated update
# perf improvement at 11:48:02
_CACHE: dict = {}  # perf: enable uvicorn worker count auto-s
