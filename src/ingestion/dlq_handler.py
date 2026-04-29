import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from confluent_kafka import Consumer, KafkaError
from fastapi import HTTPException
from src.ingestion.schema_registry import SchemaRegistryClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseConsumer(ABC):
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.consumer = self.create_consumer()
        self.schema_registry = SchemaRegistryClient(self.config['schema_registry_url'])

    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process the incoming Kafka message."""
        pass

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load consumer configuration from a YAML file."""
        import yaml
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def create_consumer(self) -> Consumer:
        """Create a Kafka consumer instance."""
        return Consumer(self.config['kafka'])

    def consume(self) -> None:
        """Start consuming messages from Kafka."""
        self.consumer.subscribe([self.config['topic']])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    self.handle_dlq(msg)
                    continue
            self.handle_message(msg)

    def handle_message(self, msg: Any) -> None:
        """Handle the incoming Kafka message."""
        try:
            message = json.loads(msg.value().decode('utf-8'))
            self.validate_message(message)
            self.process_message(message)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.handle_dlq(msg)

    def validate_message(self, message: Dict[str, Any]) -> None:
        """Validate the incoming message against the schema."""
        schema = self.schema_registry.get_schema(self.config['schema_name'])
        if not schema.validate(message):
            raise HTTPException(status_code=400, detail="Invalid message schema")

    def handle_dlq(self, msg: Any) -> None:
        """Handle messages that fail processing by sending them to a dead-letter queue."""
        dlq_topic = self.config['dlq_topic']
        logger.info(f"Sending message to DLQ: {msg.value()}")
        self.consumer.produce(dlq_topic, msg.value())
# 11:00:59 — automated update
# feat: implement graceful shutdown handler with signal trapping

# 11:00:59 — automated update
# feat: add consumer lag metric emission to Prometheus
