import pandas as pd
import numpy as np
from typing import List, Dict
from src.features.window_features import SlidingWindowFeatures
from src.features.hrv_calculator import HRVCalculator
from src.features.trend_detector import TrendDetector

class FeatureStore:
    """
    A class to manage and compute features for the Real-Time Smart Health Monitoring System.
    """

    def __init__(self, window_size: int, step_size: int) -> None:
        """
        Initializes the FeatureStore with window and step sizes.

        Args:
            window_size (int): The size of the sliding window.
            step_size (int): The step size for sliding window.
        """
        self.window_size = window_size
        self.step_size = step_size
        self.sliding_window_features = SlidingWindowFeatures(window_size, step_size)
        self.hrv_calculator = HRVCalculator()
        self.trend_detector = TrendDetector()

    def compute_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Computes sliding window features, HRV, and trend detection from the input data.

        Args:
            data (pd.DataFrame): Input DataFrame containing health metrics.

        Returns:
            pd.DataFrame: DataFrame containing computed features.
        """
        features = pd.DataFrame()
        
        # Compute sliding window features
        sliding_features = self.sliding_window_features.compute(data)
        features = pd.concat([features, sliding_features], axis=1)

        # Compute HRV features
        hrv_features = self.hrv_calculator.calculate_hrv(data['heart_rate'])
        features = pd.concat([features, hrv_features], axis=1)

        # Compute trend features
        trend_features = self.trend_detector.detect_trends(data['heart_rate'])
        features = pd.concat([features, trend_features], axis=1)

        return features

    def save_features(self, features: pd.DataFrame, feature_store_path: str) -> None:
        """
        Saves computed features to a specified path.

        Args:
            features (pd.DataFrame): DataFrame containing computed features.
            feature_store_path (str): Path to save the features.
        """
        features.to_csv(feature_store_path, index=False)

    def load_features(self, feature_store_path: str) -> pd.DataFrame:
        """
        Loads features from a specified path.

        Args:
            feature_store_path (str): Path to load the features from.

        Returns:
            pd.DataFrame: DataFrame containing loaded features.
        """
        return pd.read_csv(feature_store_path)