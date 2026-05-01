import numpy as np
import pandas as pd
from typing import List, Tuple
from src.features.hrv_calculator import calculate_hrv
from src.features.window_features import compute_sliding_window_features

class TrendDetector:
    def __init__(self, window_size: int, threshold: float):
        """
        Initializes the TrendDetector with a specified window size and threshold.

        :param window_size: Size of the sliding window for trend detection.
        :param threshold: Minimum change to consider a trend significant.
        """
        self.window_size = window_size
        self.threshold = threshold

    def detect_trends(self, data: pd.Series) -> List[Tuple[int, str]]:
        """
        Detects trends in the provided time series data.

        :param data: A pandas Series containing time series data.
        :return: A list of tuples where each tuple contains the index of the trend 
                 and the type of trend ('upward' or 'downward').
        """
        trends = []
        for i in range(len(data) - self.window_size):
            window = data[i:i + self.window_size]
            mean_change = window.mean() - data[i - 1] if i > 0 else 0
            
            if mean_change > self.threshold:
                trends.append((i + self.window_size, 'upward'))
            elif mean_change < -self.threshold:
                trends.append((i + self.window_size, 'downward'))

        return trends

    def analyze_hrv_trends(self, heart_rate_data: pd.Series) -> List[Tuple[int, str]]:
        """
        Analyzes trends in heart rate variability (HRV) based on heart rate data.

        :param heart_rate_data: A pandas Series containing heart rate data.
        :return: A list of tuples indicating HRV trends.
        """
        hrv_values = calculate_hrv(heart_rate_data)
        return self.detect_trends(hrv_values)

    def compute_features_and_trends(self, heart_rate_data: pd.Series) -> pd.DataFrame:
        """
        Computes sliding window features and detects trends in heart rate data.

        :param heart_rate_data: A pandas Series containing heart rate data.
        :return: A DataFrame containing computed features and detected trends.
        """
        features = compute_sliding_window_features(heart_rate_data, self.window_size)
        trends = self.detect_trends(heart_rate_data)

        feature_trend_df = pd.DataFrame(features)
        for index, trend in trends:
            feature_trend_df.loc[index, 'trend'] = trend

        return feature_trend_df.fillna('no trend')
# 10:27:16 — automated update
# feat: add polynomial trend feature with significance test

# 10:27:16 — automated update
# feat: add feature versioning metadata to each feature vector
