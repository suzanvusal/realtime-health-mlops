import json
import logging
from typing import Any, Dict, Optional
from kafka import KafkaConsumer
from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import CachedSchemaRegistryClient

class BaseConsumer:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.consumer = self.create_consumer()
        self.dlq_handler = DLQHandler(self.config['dlq_topic'])

    def load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as file:
            return json.load(file)

    def create_consumer(self) -> AvroConsumer:
        schema_registry_client = SchemaRegistryClient({
            'url': self.config['schema_registry_url']
        })
        consumer_config = {
            'bootstrap.servers': self.config['bootstrap_servers'],
            'group.id': self.config['group_id'],
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'schema.registry.url': self.config['schema_registry_url'],
        }
        return AvroConsumer(consumer_config, schema_registry_client=schema_registry_client)

    def consume(self) -> None:
        self.consumer.subscribe([self.config['topic']])
        try:
            while True:
                message = self.consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    logging.error(f"Consumer error: {message.error()}")
                    continue
                self.process_message(message)

        except Exception as e:
            logging.exception("Exception in consumer loop: %s", e)
        finally:
            self.consumer.close()

    def process_message(self, message: Any) -> None:
        try:
            data = message.value()
            self.validate_data(data)
            # Process the validated data
        except Exception as e:
            logging.error(f"Data validation error: {e}")
            self.dlq_handler.handle(message)

    def validate_data(self, data: Any) -> None:
        # Implement your data validation logic here
        if not isinstance(data, dict):
            raise ValueError("Invalid data format")

class DLQHandler:
    def __init__(self, dlq_topic: str):
        self.dlq_topic = dlq_topic
        self.consumer = KafkaConsumer(self.dlq_topic)

    def handle(self, message: Any) -> None:
        # Logic to send the message to the dead-letter queue
        logging.info(f"Sending message to DLQ: {message.value()}")
        # Implement DLQ logic here

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    consumer = BaseConsumer('configs/consumer_config.yaml')
    consumer.consume()