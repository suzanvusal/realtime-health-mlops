import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests
from confluent_kafka import Consumer, KafkaError

logger = logging.getLogger(__name__)


class SchemaRegistryClient:
    def __init__(self, schema_registry_url: str):
        self.schema_registry_url = schema_registry_url

    def get_schema(self, subject: str) -> Optional[Dict[str, Any]]:
        """Fetch the schema for a given subject from the schema registry."""
        try:
            response = requests.get(f"{self.schema_registry_url}/subjects/{subject}/versions/latest")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching schema for {subject}: {e}")
            return None


class BaseKafkaConsumer(ABC):
    def __init__(self, config: Dict[str, Any], schema_registry_url: str):
        self.consumer = Consumer(config)
        self.schema_registry_client = SchemaRegistryClient(schema_registry_url)

    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process the consumed message."""
        pass

    def consume(self, topic: str) -> None:
        """Start consuming messages from the specified Kafka topic."""
        self.consumer.subscribe([topic])
        logger.info(f"Subscribed to topic: {topic}")

        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                logger.error(f"Consumer error: {msg.error()}")
                continue

            message_value = json.loads(msg.value().decode('utf-8'))
            subject = f"{topic}-value"
            schema = self.schema_registry_client.get_schema(subject)

            if self.validate_message(message_value, schema):
                self.process_message(message_value)
            else:
                logger.warning(f"Message validation failed: {message_value}")

    def validate_message(self, message: Dict[str, Any], schema: Optional[Dict[str, Any]]) -> bool:
        """Validate the message against the schema."""
        if not schema:
            logger.error("No schema found for validation.")
            return False
        # Implement validation logic here (e.g., using jsonschema)
        return True

    def close(self) -> None:
        """Close the Kafka consumer."""
        self.consumer.close()
        logger.info("Kafka consumer closed.")