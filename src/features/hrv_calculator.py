import numpy as np
import pandas as pd
from typing import List, Tuple

class HRVCalculator:
    """Class to calculate Heart Rate Variability (HRV) metrics."""

    def __init__(self, window_size: int):
        """
        Initialize HRVCalculator with a specified sliding window size.

        Args:
            window_size (int): Size of the sliding window for HRV calculation.
        """
        self.window_size = window_size

    def calculate_hrv(self, rr_intervals: List[float]) -> Tuple[float, float]:
        """
        Calculate HRV metrics from a list of RR intervals.

        Args:
            rr_intervals (List[float]): List of RR intervals in milliseconds.

        Returns:
            Tuple[float, float]: RMSSD and SDNN HRV metrics.
        """
        rr_intervals = np.array(rr_intervals)
        if len(rr_intervals) < 2:
            return 0.0, 0.0

        # Calculate RMSSD
        diff_rr = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(diff_rr ** 2))

        # Calculate SDNN
        sdnn = np.std(rr_intervals)

        return rmssd, sdnn

    def sliding_window_hrv(self, rr_intervals: List[float]) -> pd.DataFrame:
        """
        Calculate HRV metrics using a sliding window approach.

        Args:
            rr_intervals (List[float]): List of RR intervals in milliseconds.

        Returns:
            pd.DataFrame: DataFrame containing RMSSD and SDNN metrics for each window.
        """
        hrv_metrics = []
        for i in range(len(rr_intervals) - self.window_size + 1):
            window = rr_intervals[i:i + self.window_size]
            rmssd, sdnn = self.calculate_hrv(window)
            hrv_metrics.append({'start_index': i, 'rmssd': rmssd, 'sdnn': sdnn})

        return pd.DataFrame(hrv_metrics)

def main():
    # Example usage
    rr_intervals = [800, 810, 790, 780, 770, 800, 820, 830, 810, 800]
    hrv_calculator = HRVCalculator(window_size=5)
    hrv_results = hrv_calculator.sliding_window_hrv(rr_intervals)
    print(hrv_results)

if __name__ == "__main__":
    main()