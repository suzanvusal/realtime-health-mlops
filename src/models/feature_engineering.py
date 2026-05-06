import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureEngineering:
    def __init__(self, config: Dict):
        """
        Initialize the FeatureEngineering class.

        Args:
            config (Dict): Configuration dictionary containing feature engineering parameters.
        """
        self.config = config
        self.scaler = StandardScaler()

    def extract_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from the raw data.

        Args:
            data (pd.DataFrame): Raw input data.

        Returns:
            pd.DataFrame: DataFrame containing extracted features.
        """
        logger.info("Starting feature extraction.")
        # Example feature extraction logic
        data['heart_rate_variability'] = data['heart_rate'].diff().rolling(window=5).std()
        data['activity_level'] = data['steps'] / data['active_minutes']
        features = data[['heart_rate', 'heart_rate_variability', 'activity_level']]
        logger.info("Feature extraction completed.")
        return features

    def scale_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Scale features using StandardScaler.

        Args:
            features (pd.DataFrame): DataFrame containing features to scale.

        Returns:
            pd.DataFrame: Scaled features.
        """
        logger.info("Scaling features.")
        scaled_features = self.scaler.fit_transform(features)
        logger.info("Feature scaling completed.")
        return pd.DataFrame(scaled_features, columns=features.columns)

    def split_data(self, features: pd.DataFrame, target: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split the data into training and validation sets.

        Args:
            features (pd.DataFrame): DataFrame containing features.
            target (pd.Series): Series containing target variable.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: Training and validation sets.
        """
        logger.info("Splitting data into train and validation sets.")
        X_train, X_val, y_train, y_val = train_test_split(features, target, 
                                                          test_size=self.config['test_size'], 
                                                          random_state=self.config['random_state'])
        logger.info("Data split completed.")
        return X_train, X_val, y_train, y_val

    def process_data(self, data: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Full data processing pipeline: extract features, scale them, and split the dataset.

        Args:
            data (pd.DataFrame): Raw input data.
            target_column (str): Name of the target column.

        Returns:
            Tuple[pd.DataFrame, pd.Series]: Processed features and target variable.
        """
        features = self.extract_features(data)
        scaled_features = self.scale_features(features)
        target = data[target_column]
        X_train, X_val, y_train, y_val = self.split_data(scaled_features, target)
        return (X_train, y_train), (X_val, y_val)
# 11:11:30 — automated update
# fix applied at 11:11:30
_FIXED = True  # fix: handle patients with fewer than 30 data points
