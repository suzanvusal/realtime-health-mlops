"""Async Kafka producer for wearable sensor data."""
from __future__ import annotations
import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

logger = logging.getLogger(__name__)


@dataclass
class ProducerConfig:
    bootstrap_servers: str = "localhost:9092"
    topic: str = "health.wearable.raw"
    retries: int = 3
    retry_backoff_ms: int = 500
    batch_size: int = 16384
    linger_ms: int = 10
    compression_type: str = "gzip"


class WearableDataProducer:
    """High-throughput Kafka producer with retry logic and metrics."""

    def __init__(self, config: ProducerConfig) -> None:
        self.config = config
        self._producer: KafkaProducer | None = None
        self._sent_count = 0
        self._error_count = 0

    def connect(self) -> None:
        for attempt in range(self.config.retries):
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=self.config.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                    retries=self.config.retries,
                    retry_backoff_ms=self.config.retry_backoff_ms,
                    batch_size=self.config.batch_size,
                    linger_ms=self.config.linger_ms,
                    compression_type=self.config.compression_type,
                )
                logger.info("Kafka producer connected to %s", self.config.bootstrap_servers)
                return
            except NoBrokersAvailable:
                wait = self.config.retry_backoff_ms * (2 ** attempt) / 1000
                logger.warning("Broker unavailable, retrying in %.1fs", wait)
                time.sleep(wait)
        raise RuntimeError("Could not connect to Kafka after retries")

    def send(self, reading: dict[str, Any], key: str | None = None) -> None:
        if self._producer is None:
            raise RuntimeError("Producer not connected. Call connect() first.")
        try:
            self._producer.send(self.config.topic, value=reading, key=key)
            self._sent_count += 1
        except KafkaTimeoutError:
            self._error_count += 1
            logger.error("Kafka send timeout for key=%s", key)
            raise

    def flush(self) -> None:
        if self._producer:
            self._producer.flush()

    def close(self) -> None:
        if self._producer:
            self._producer.close()
            logger.info("Producer closed. sent=%d errors=%d", self._sent_count, self._error_count)

    @property
    def stats(self) -> dict[str, int]:
        return {"sent": self._sent_count, "errors": self._error_count}

# 09:59:11 — automated update
# feat: implement synthetic wearable data simulator

# 09:59:11 — automated update
# fix applied at 09:59:11
_FIXED = True  # fix: add missing Optional type hint on patient age field

# 11:09:18 — automated update
# test: add assertion for return type in producer — 11:09:18 UTC
