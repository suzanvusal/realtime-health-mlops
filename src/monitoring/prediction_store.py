import json
import logging
from typing import Any, Dict, List
import redis
from kafka import KafkaConsumer, KafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionStore:
    def __init__(self, redis_host: str, redis_port: int, kafka_topic: str):
        """
        Initializes the PredictionStore with Redis and Kafka configurations.

        Args:
            redis_host (str): Hostname for the Redis server.
            redis_port (int): Port number for the Redis server.
            kafka_topic (str): Kafka topic for prediction logging.
        """
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.kafka_topic = kafka_topic

    def log_prediction(self, prediction: Dict[str, Any]) -> None:
        """
        Logs a prediction to Redis and Kafka.

        Args:
            prediction (Dict[str, Any]): The prediction data to log.
        """
        try:
            prediction_id = prediction.get("id")
            self.redis_client.set(prediction_id, json.dumps(prediction))
            self.kafka_producer.send(self.kafka_topic, value=json.dumps(prediction).encode('utf-8'))
            logger.info(f"Logged prediction: {prediction_id}")
        except Exception as e:
            logger.error(f"Failed to log prediction: {e}")

    def ingest_feedback(self, feedback: Dict[str, Any]) -> None:
        """
        Ingests feedback for a specific prediction.

        Args:
            feedback (Dict[str, Any]): The feedback data to ingest.
        """
        try:
            prediction_id = feedback.get("id")
            existing_prediction = self.redis_client.get(prediction_id)
            if existing_prediction:
                existing_prediction = json.loads(existing_prediction)
                existing_prediction['feedback'] = feedback
                self.redis_client.set(prediction_id, json.dumps(existing_prediction))
                logger.info(f"Ingested feedback for prediction: {prediction_id}")
            else:
                logger.warning(f"No prediction found for ID: {prediction_id}")
        except Exception as e:
            logger.error(f"Failed to ingest feedback: {e}")

    def get_predictions(self) -> List[Dict[str, Any]]:
        """
        Retrieves all logged predictions from Redis.

        Returns:
            List[Dict[str, Any]]: A list of all predictions.
        """
        try:
            keys = self.redis_client.keys()
            predictions = [json.loads(self.redis_client.get(key)) for key in keys]
            logger.info("Retrieved all predictions")
            return predictions
        except Exception as e:
            logger.error(f"Failed to retrieve predictions: {e}")
            return []

# Example usage
if __name__ == "__main__":
    store = PredictionStore(redis_host='localhost', redis_port=6379, kafka_topic='predictions')
    store.log_prediction({"id": "123", "model": "xgboost", "result": 0.85})
    store.ingest_feedback({"id": "123", "outcome": "positive"})
    predictions = store.get_predictions()
    print(predictions)