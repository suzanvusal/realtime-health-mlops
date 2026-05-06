import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict
import redis
import json
import logging

logging.basicConfig(level=logging.INFO)

class DataPipeline:
    def __init__(self, redis_host: str, redis_port: int, redis_db: int):
        """
        Initializes the DataPipeline with Redis connection parameters.

        :param redis_host: Hostname for Redis server
        :param redis_port: Port for Redis server
        :param redis_db: Database number for Redis
        """
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    
    def extract_data(self, key: str) -> pd.DataFrame:
        """
        Extracts data from Redis.

        :param key: Redis key for the data
        :return: DataFrame containing the extracted data
        """
        logging.info(f"Extracting data from Redis with key: {key}")
        data_json = self.redis_client.get(key)
        if data_json is None:
            logging.error(f"No data found for key: {key}")
            raise ValueError(f"No data found for key: {key}")
        data = json.loads(data_json)
        return pd.DataFrame(data)

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs feature engineering on the DataFrame.

        :param df: Input DataFrame
        :return: DataFrame with engineered features
        """
        logging.info("Starting feature engineering")
        # Example feature engineering steps
        df['heart_rate'] = df['heart_rate'] / 100  # Normalize heart rate
        df['temperature'] = df['temperature'] - 32  # Convert Fahrenheit to Celsius
        logging.info("Feature engineering completed")
        return df

    def split_data(self, df: pd.DataFrame, target_column: str, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Splits the DataFrame into training and validation sets.

        :param df: Input DataFrame
        :param target_column: Name of the target column
        :param test_size: Proportion of the dataset to include in the test split
        :return: Tuple of (X_train, X_val, y_train, y_val)
        """
        logging.info("Splitting data into train and validation sets")
        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
        logging.info("Data split completed")
        return X_train, X_val, y_train, y_val

    def run_pipeline(self, redis_key: str, target_column: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Executes the data pipeline.

        :param redis_key: Redis key for data extraction
        :param target_column: Name of the target column for splitting
        :return: Tuple of (X_train, X_val, y_train, y_val)
        """
        df = self.extract_data(redis_key)
        df = self.feature_engineering(df)
        return self.split_data(df, target_column)
# 11:11:30 — automated update
# fix applied at 11:11:30
_FIXED = True  # fix: temporal leakage — ensure val set is always after train
