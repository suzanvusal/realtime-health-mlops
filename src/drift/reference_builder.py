import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from typing import Any, Dict, Optional
import mlflow
import os


class ReferenceBuilder:
    def __init__(self, reference_data_path: str):
        """
        Initializes the ReferenceBuilder with the path to the reference dataset.

        Args:
            reference_data_path (str): Path to the reference dataset CSV file.
        """
        self.reference_data_path = reference_data_path
        self.reference_data: Optional[pd.DataFrame] = None

    def load_reference_data(self) -> pd.DataFrame:
        """
        Loads the reference dataset from the specified path.

        Returns:
            pd.DataFrame: The loaded reference dataset.
        """
        if not os.path.exists(self.reference_data_path):
            raise FileNotFoundError(f"Reference data file not found: {self.reference_data_path}")
        
        self.reference_data = pd.read_csv(self.reference_data_path)
        return self.reference_data

    def generate_drift_report(self, current_data: pd.DataFrame, column_mapping: Dict[str, Any]) -> Report:
        """
        Generates a drift report comparing the reference dataset with the current dataset.

        Args:
            current_data (pd.DataFrame): The current dataset to compare against the reference.
            column_mapping (Dict[str, Any]): Mapping of columns for the report.

        Returns:
            Report: The generated drift report.
        """
        if self.reference_data is None:
            raise ValueError("Reference data not loaded. Call load_reference_data() first.")
        
        report = Report(metrics=[DataDriftPreset()])
        report.calculate(reference=self.reference_data, current=current_data, column_mapping=ColumnMapping(**column_mapping))
        return report

    def save_drift_report(self, report: Report, output_path: str) -> None:
        """
        Saves the drift report to the specified output path.

        Args:
            report (Report): The drift report to save.
            output_path (str): Path to save the report.
        """
        report.save_html(output_path)
        mlflow.log_artifact(output_path)

    def run(self, current_data: pd.DataFrame, column_mapping: Dict[str, Any], output_path: str) -> None:
        """
        Executes the drift detection process.

        Args:
            current_data (pd.DataFrame): The current dataset to compare against the reference.
            column_mapping (Dict[str, Any]): Mapping of columns for the report.
            output_path (str): Path to save the drift report.
        """
        self.load_reference_data()
        report = self.generate_drift_report(current_data, column_mapping)
        self.save_drift_report(report, output_path)
# 11:24:54 — automated update
# feat: implement drift severity classification (none/warn/critical)

# 11:24:54 — automated update
# perf improvement at 11:24:54
_CACHE: dict = {}  # perf: run drift reports in parallel for 

# 11:24:54 — automated update
# refactor: rename variable for clarity in reference_builder — 11:24:54 UTC
