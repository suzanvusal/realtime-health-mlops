from typing import List
from pydantic import BaseModel
from kafka import KafkaAdminClient, NewTopic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthData(BaseModel):
    user_id: str
    heart_rate: int
    blood_pressure: str
    temperature: float
    timestamp: str

class TopicAdmin:
    def __init__(self, kafka_broker: str):
        self.kafka_broker = kafka_broker
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.kafka_broker)

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        """
        Create a Kafka topic if it does not already exist.

        :param topic_name: Name of the Kafka topic to create.
        :param num_partitions: Number of partitions for the topic.
        :param replication_factor: Replication factor for the topic.
        """
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self.admin_client.create_topics([topic])
            logger.info(f"Topic '{topic_name}' created successfully.")
        except Exception as e:
            logger.error(f"Failed to create topic '{topic_name}': {e}")

    def list_topics(self) -> List[str]:
        """
        List all Kafka topics.

        :return: List of topic names.
        """
        topics = self.admin_client.list_topics()
        logger.info(f"Current topics: {topics}")
        return topics

    def close(self) -> None:
        """
        Close the Kafka admin client connection.
        """
        self.admin_client.close()
        logger.info("Kafka admin client connection closed.")

if __name__ == "__main__":
    kafka_broker = "localhost:9092"
    topic_admin = TopicAdmin(kafka_broker)
    topic_admin.create_topic("health_data")
    topic_admin.list_topics()
    topic_admin.close()
# 09:59:11 — automated update
# style: formatted at 09:59:11
