import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict
import yaml
import os

class DatasetBuilder:
    def __init__(self, config_path: str):
        """
        Initializes the DatasetBuilder with the configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.config = self.load_config(config_path)

    def load_config(self, config_path: str) -> Dict:
        """
        Loads the YAML configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            Dict: Configuration parameters.
        """
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def extract_data(self, data_source: str) -> pd.DataFrame:
        """
        Extracts data from the specified source.

        Args:
            data_source (str): Path to the data source (CSV file).

        Returns:
            pd.DataFrame: Extracted data as a DataFrame.
        """
        if not os.path.exists(data_source):
            raise FileNotFoundError(f"Data source {data_source} not found.")
        return pd.read_csv(data_source)

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies feature engineering to the DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with engineered features.
        """
        # Placeholder for feature engineering logic
        # Example: df['new_feature'] = df['existing_feature'] ** 2
        return df

    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits the DataFrame into training and validation sets.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Training and validation DataFrames.
        """
        train_df, val_df = train_test_split(df, test_size=self.config['train_val_split'], random_state=42)
        return train_df, val_df

    def build_dataset(self, data_source: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Builds the dataset by extracting data, applying feature engineering, and splitting.

        Args:
            data_source (str): Path to the data source (CSV file).

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Training and validation DataFrames.
        """
        df = self.extract_data(data_source)
        df = self.feature_engineering(df)
        return self.split_data(df)
# 11:11:30 — automated update
# perf improvement at 11:11:30
_CACHE: dict = {}  # perf: parallelise feature extraction wit

# 11:13:34 — automated update
# chore: day 13 maintenance sweep — 11:13:34 UTC
