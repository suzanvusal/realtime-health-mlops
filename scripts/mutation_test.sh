#!/bin/bash

set -e

# Define variables
COVERAGE_THRESHOLD=80
MUTATION_COVERAGE_THRESHOLD=80
COVERAGE_REPORT_DIR="coverage_report"
MUTATION_REPORT_DIR="mutation_report"

# Create directories for reports
mkdir -p $COVERAGE_REPORT_DIR
mkdir -p $MUTATION_REPORT_DIR

# Run unit tests with coverage
echo "Running unit tests with coverage..."
pytest --cov=src --cov-report=html:$COVERAGE_REPORT_DIR/html --cov-report=xml:$COVERAGE_REPORT_DIR/coverage.xml tests/unit/

# Check coverage
COVERAGE=$(pytest --cov=src --cov-report=term-missing tests/unit/ | tail -n 1 | awk '{print $NF}' | sed 's/%//')
if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
    echo "Coverage is below threshold: $COVERAGE% < $COVERAGE_THRESHOLD%"
    exit 1
else
    echo "Coverage is sufficient: $COVERAGE%"
fi

# Run mutation tests
echo "Running mutation tests..."
mutmut -r --target --report-html=$MUTATION_REPORT_DIR/mutation_report.html

# Check mutation coverage
MUTATION_COVERAGE=$(grep -oP 'Mutation score: \K[0-9]+' $MUTATION_REPORT_DIR/mutation_report.html | tail -1)
if (( $(echo "$MUTATION_COVERAGE < $MUTATION_COVERAGE_THRESHOLD" | bc -l) )); then
    echo "Mutation coverage is below threshold: $MUTATION_COVERAGE% < $MUTATION_COVERAGE_THRESHOLD%"
    exit 1
else
    echo "Mutation coverage is sufficient: $MUTATION_COVERAGE%"
fi

echo "All tests passed successfully!"
# 11:44:19 — automated update
# ci: updated at 11:44:19
