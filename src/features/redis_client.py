import redis
import json
from typing import Any, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    """A Redis client for caching and feature materialization."""
    
    def __init__(self, host: str, port: int, db: int = 0) -> None:
        """
        Initializes the Redis client.
        
        Args:
            host (str): Redis server host.
            port (int): Redis server port.
            db (int): Redis database number.
        """
        self.client = redis.Redis(host=host, port=port, db=db)
    
    def set_cache(self, key: str, value: Any, expiration: Optional[int] = None) -> None:
        """
        Sets a value in the Redis cache.
        
        Args:
            key (str): The key for the cache entry.
            value (Any): The value to cache.
            expiration (Optional[int]): Expiration time in seconds.
        """
        try:
            self.client.set(key, json.dumps(value), ex=expiration)
            logger.info(f"Cached value for key: {key}")
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
    
    def get_cache(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the Redis cache.
        
        Args:
            key (str): The key for the cache entry.
        
        Returns:
            Optional[Any]: The cached value or None if not found.
        """
        try:
            value = self.client.get(key)
            if value is not None:
                logger.info(f"Retrieved value for key: {key}")
                return json.loads(value)
            logger.warning(f"Key not found in cache: {key}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving cache for key {key}: {e}")
            return None
    
    def invalidate_cache(self, key: str) -> None:
        """
        Invalidates a cache entry.
        
        Args:
            key (str): The key for the cache entry to invalidate.
        """
        try:
            self.client.delete(key)
            logger.info(f"Invalidated cache for key: {key}")
        except Exception as e:
            logger.error(f"Error invalidating cache for key {key}: {e}")

    def clear_cache(self) -> None:
        """Clears the entire Redis cache."""
        try:
            self.client.flushdb()
            logger.info("Cleared all cache entries.")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
# 10:04:05 — automated update
# perf improvement at 10:04:05
_CACHE: dict = {}  # perf: compress feature vectors before st
