import redis
import json
import time
from typing import Any, Dict
from src.features.redis_client import get_redis_client
from src.features.materializer import FeatureMaterializer

class CachePolicy:
    def __init__(self, redis_config: str, materializer: FeatureMaterializer):
        """
        Initialize the CachePolicy with Redis configuration and a feature materializer.

        Args:
            redis_config (str): Path to the Redis configuration file.
            materializer (FeatureMaterializer): Instance of FeatureMaterializer for feature updates.
        """
        self.redis_client = get_redis_client(redis_config)
        self.materializer = materializer

    def cache_feature(self, key: str, value: Any, expiration: int = 3600) -> None:
        """
        Cache a feature in Redis with an expiration time.

        Args:
            key (str): The key under which the feature will be cached.
            value (Any): The value of the feature to be cached.
            expiration (int): Time in seconds until the cache expires.
        """
        self.redis_client.set(key, json.dumps(value), ex=expiration)

    def get_cached_feature(self, key: str) -> Any:
        """
        Retrieve a feature from the Redis cache.

        Args:
            key (str): The key of the cached feature.

        Returns:
            Any: The cached feature value or None if not found.
        """
        cached_value = self.redis_client.get(key)
        if cached_value is not None:
            return json.loads(cached_value)
        return None

    def invalidate_cache(self, key: str) -> None:
        """
        Invalidate a specific cache entry.

        Args:
            key (str): The key of the cache entry to invalidate.
        """
        self.redis_client.delete(key)

    def materialize_features(self, feature_keys: Dict[str, Any]) -> None:
        """
        Materialize features and cache them.

        Args:
            feature_keys (Dict[str, Any]): A dictionary of feature keys and their corresponding values.
        """
        for key, value in feature_keys.items():
            self.cache_feature(key, value)

    def refresh_cache(self, key: str, refresh_interval: int = 300) -> None:
        """
        Refresh the cache for a specific feature if it is stale.

        Args:
            key (str): The key of the feature to refresh.
            refresh_interval (int): Time in seconds to check for cache refresh.
        """
        while True:
            cached_value = self.get_cached_feature(key)
            if cached_value is None:
                new_value = self.materializer.fetch_feature(key)
                self.cache_feature(key, new_value)
            time.sleep(refresh_interval)
# 10:04:05 — automated update
# feat: add Redis Streams for feature update notifications

# 10:04:05 — automated update
# test marker: test: add Redis mock tests using fakeredis library
_TEST_MARKER = 'cache_policy'
