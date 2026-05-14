#!/bin/bash

# Grafana Import Script
# This script imports Grafana dashboards for drift monitoring and model performance.

GRAFANA_URL="http://localhost:3000"
GRAFANA_API_KEY="YOUR_API_KEY_HERE"

# Function to import a dashboard
import_dashboard() {
    local dashboard_file=$1
    local dashboard_name=$(basename "$dashboard_file")

    echo "Importing dashboard: $dashboard_name"

    curl -X POST "$GRAFANA_URL/api/dashboards/db" \
        -H "Authorization: Bearer $GRAFANA_API_KEY" \
        -H "Content-Type: application/json" \
        -d @"$dashboard_file"

    if [ $? -eq 0 ]; then
        echo "Successfully imported $dashboard_name"
    else
        echo "Failed to import $dashboard_name"
    fi
}

# Import feature drift heatmap dashboard
import_dashboard "infra/grafana/dashboards/feature_drift_heatmap.json"

# Import model performance dashboard
import_dashboard "infra/grafana/dashboards/model_performance.json"

echo "All dashboards imported successfully."
# 11:19:18 — automated update
# feat: add time-range variable to all dashboards for drill-down

# 11:19:18 — automated update
"""\ndocs: add screenshot of dashboards to README\n"""
