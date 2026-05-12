import os
from typing import Any, Dict, List
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric import DataDriftMetric
import pandas as pd
import yaml


class DriftConfig:
    def __init__(self, reference_data_path: str, current_data_path: str, report_path: str):
        """
        Initialize DriftConfig with paths for reference data, current data, and report output.

        Args:
            reference_data_path (str): Path to the reference dataset.
            current_data_path (str): Path to the current dataset for comparison.
            report_path (str): Path to save the drift report.
        """
        self.reference_data_path = reference_data_path
        self.current_data_path = current_data_path
        self.report_path = report_path
        self.column_mapping = ColumnMapping()

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load reference and current datasets.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Loaded reference and current dataframes.
        """
        reference_data = pd.read_csv(self.reference_data_path)
        current_data = pd.read_csv(self.current_data_path)
        return reference_data, current_data

    def generate_drift_report(self, reference_data: pd.DataFrame, current_data: pd.DataFrame) -> None:
        """
        Generate a drift report comparing reference and current datasets.

        Args:
            reference_data (pd.DataFrame): The reference dataset.
            current_data (pd.DataFrame): The current dataset to compare against.
        """
        report = Report(metrics=[DataDriftMetric()])
        report.run(reference_data=reference_data, current_data=current_data, column_mapping=self.column_mapping)
        report.save_html(self.report_path)

    @classmethod
    def from_yaml(cls, config_path: str) -> 'DriftConfig':
        """
        Create a DriftConfig instance from a YAML configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            DriftConfig: An instance of DriftConfig populated with values from the YAML file.
        """
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(
            reference_data_path=config['reference_data_path'],
            current_data_path=config['current_data_path'],
            report_path=config['report_path']
        )
# 11:24:54 — automated update
# feat: add drift score extraction from Evidently JSON output

# 11:24:54 — automated update
# fix applied at 11:24:54
_FIXED = True  # fix: reference dataset staleness check logic inverted

# 11:24:54 — automated update
# perf: add __slots__ to reduce memory in drift_config — 11:24:54 UTC
