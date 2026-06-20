import os
import pandas as pd
from typing import List, Dict
from datetime import datetime
from redis import Redis
import mlflow
from kafka import KafkaConsumer
import json

class DatasetAssembler:
    def __init__(self, redis_host: str, redis_port: int, kafka_topic: str):
        """
        Initializes the DatasetAssembler with Redis and Kafka configurations.

        Args:
            redis_host (str): The hostname of the Redis server.
            redis_port (int): The port number of the Redis server.
            kafka_topic (str): The Kafka topic to consume data from.
        """
        self.redis_client = Redis(host=redis_host, port=redis_port)
        self.kafka_topic = kafka_topic

    def fetch_data_from_kafka(self) -> List[Dict]:
        """
        Consumes messages from Kafka and returns a list of data records.

        Returns:
            List[Dict]: A list of data records fetched from Kafka.
        """
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        
        records = []
        for message in consumer:
            records.append(message.value)
            if len(records) >= 100:  # Limit the number of records for processing
                break
        return records

    def assemble_dataset(self, records: List[Dict]) -> pd.DataFrame:
        """
        Assembles a DataFrame from the list of records.

        Args:
            records (List[Dict]): A list of data records.

        Returns:
            pd.DataFrame: A DataFrame containing the assembled dataset.
        """
        df = pd.DataFrame(records)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def save_to_redis(self, df: pd.DataFrame) -> None:
        """
        Saves the DataFrame to Redis.

        Args:
            df (pd.DataFrame): The DataFrame to save.
        """
        self.redis_client.set('health_data', df.to_json(orient='records'))

    def run(self) -> None:
        """
        Main method to fetch, assemble, and save the dataset.
        """
        records = self.fetch_data_from_kafka()
        if records:
            df = self.assemble_dataset(records)
            self.save_to_redis(df)

if __name__ == "__main__":
    assembler = DatasetAssembler(redis_host='localhost', redis_port=6379, kafka_topic='health_data')
    assembler.run()