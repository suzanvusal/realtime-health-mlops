import pytest
from unittest.mock import patch, MagicMock
from src.ingestion.consumer import BaseConsumer
from src.ingestion.dlq_handler import DLQHandler
from src.ingestion.schema_registry import SchemaRegistry


class TestBaseConsumer:
    @pytest.fixture
    def consumer(self):
        config = {
            'topic': 'test_topic',
            'group_id': 'test_group',
            'bootstrap_servers': 'localhost:9092',
            'schema_registry_url': 'http://localhost:8081'
        }
        schema_registry = SchemaRegistry(config['schema_registry_url'])
        dlq_handler = DLQHandler()
        return BaseConsumer(config, schema_registry, dlq_handler)

    @patch('src.ingestion.consumer.Consumer')
    def test_consume_message_success(self, mock_consumer, consumer):
        mock_message = MagicMock()
        mock_message.value = b'{"key": "value"}'
        mock_consumer.return_value.__iter__.return_value = [mock_message]

        result = consumer.consume()
        assert result == {"key": "value"}

    @patch('src.ingestion.consumer.Consumer')
    def test_consume_message_invalid(self, mock_consumer, consumer):
        mock_message = MagicMock()
        mock_message.value = b'invalid_json'
        mock_consumer.return_value.__iter__.return_value = [mock_message]

        with patch.object(consumer.dlq_handler, 'handle') as mock_handle:
            result = consumer.consume()
            mock_handle.assert_called_once_with(mock_message)
            assert result is None

    @patch('src.ingestion.consumer.Consumer')
    def test_schema_validation_success(self, mock_consumer, consumer):
        valid_message = b'{"key": "value"}'
        assert consumer.validate_schema(valid_message) is True

    @patch('src.ingestion.consumer.Consumer')
    def test_schema_validation_failure(self, mock_consumer, consumer):
        invalid_message = b'invalid_json'
        assert consumer.validate_schema(invalid_message) is False

    @patch('src.ingestion.consumer.Consumer')
    def test_dlq_handler_called_on_failure(self, mock_consumer, consumer):
        mock_message = MagicMock()
        mock_message.value = b'invalid_json'
        mock_consumer.return_value.__iter__.return_value = [mock_message]

        with patch.object(consumer.dlq_handler, 'handle') as mock_handle:
            consumer.consume()
            mock_handle.assert_called_once_with(mock_message)
# 11:00:59 — automated update
# test marker: test: add integration test for consumer with embedded Kafka
_TEST_MARKER = 'test_consumer'
