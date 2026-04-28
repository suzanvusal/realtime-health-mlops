#!/bin/bash

set -e

# Function to run linting
run_lint() {
    echo "Running linting..."
    flake8 .
}

# Function to run tests
run_tests() {
    echo "Running tests..."
    pytest --maxfail=1 --disable-warnings -q
}

# Function to build the project
build_project() {
    echo "Building the project..."
    python setup.py sdist bdist_wheel
}

# Function to run security scan
run_security_scan() {
    echo "Running security scan..."
    bandit -r .
}

# Main execution
echo "Starting CI/CD pipeline..."

run_lint
run_tests
build_project
run_security_scan

echo "CI/CD pipeline completed successfully."
# 11:09:18 — automated update
# ci: updated at 11:09:18
