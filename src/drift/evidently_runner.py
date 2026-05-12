"""Evidently AI drift report runner for Smart Health monitoring."""
from __future__ import annotations
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, ClassificationPreset
from evidently.report import Report

logger = logging.getLogger(__name__)

VITAL_FEATURES = [
    "heart_rate_mean", "heart_rate_std", "heart_rate_min", "heart_rate_max",
    "spo2_mean", "spo2_std", "temperature_mean", "hrv_rmssd", "hrv_pnn50",
    "hr_trend_slope", "hr_trend_r2", "spo2_trend_slope",
    "age", "respiratory_rate_mean",
]


class DriftReportRunner:
    """Generates Evidently drift reports comparing reference vs current data."""

    def __init__(
        self,
        reference_path: str,
        reports_dir: str = "reports/drift",
        drift_threshold: float = 0.15,
    ) -> None:
        self.reference_path = Path(reference_path)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.drift_threshold = drift_threshold
        self._reference: pd.DataFrame | None = None

    def load_reference(self) -> pd.DataFrame:
        if self._reference is None:
            self._reference = pd.read_parquet(self.reference_path)
            logger.info("Loaded reference dataset: %d rows", len(self._reference))
        return self._reference

    def run_data_drift(self, current: pd.DataFrame) -> dict:
        reference = self.load_reference()
        report = Report(metrics=[DataDriftPreset(), DataQualityPreset()])
        report.run(reference_data=reference[VITAL_FEATURES],
                   current_data=current[VITAL_FEATURES])

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        html_path = self.reports_dir / f"data_drift_{ts}.html"
        json_path = self.reports_dir / f"data_drift_{ts}.json"
        report.save_html(str(html_path))
        report.save_json(str(json_path))

        result = json.loads(json_path.read_text())
        drift_score = self._extract_drift_score(result)
        logger.info("Data drift score: %.4f (threshold=%.2f)", drift_score, self.drift_threshold)
        return {
            "drift_score": drift_score,
            "is_drifted": drift_score > self.drift_threshold,
            "report_path": str(html_path),
            "timestamp": ts,
        }

    def _extract_drift_score(self, report_json: dict) -> float:
        try:
            metrics = report_json.get("metrics", [])
            for m in metrics:
                if m.get("metric") == "DatasetDriftMetric":
                    return m["result"].get("share_of_drifted_columns", 0.0)
        except (KeyError, IndexError):
            pass
        return 0.0

# 11:24:54 — automated update
"""\ndocs: explain drift detection methodology in docs/drift.md\n"""
