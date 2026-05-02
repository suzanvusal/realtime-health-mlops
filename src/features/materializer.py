import json
import redis
from typing import Any, Dict
from datetime import timedelta
from src.features.redis_client import get_redis_client
from src.features.cache_policy import CachePolicy

class FeatureMaterializer:
    def __init__(self, redis_client: redis.Redis, cache_policy: CachePolicy) -> None:
        """
        Initialize the FeatureMaterializer.

        Args:
            redis_client (redis.Redis): Redis client instance.
            cache_policy (CachePolicy): Instance of CachePolicy for cache management.
        """
        self.redis_client = redis_client
        self.cache_policy = cache_policy

    def materialize_features(self, key: str, features: Dict[str, Any]) -> None:
        """
        Materialize features into Redis cache.

        Args:
            key (str): The key under which features will be stored.
            features (Dict[str, Any]): A dictionary of features to be cached.
        """
        if self.cache_policy.should_cache(key):
            self.redis_client.set(key, json.dumps(features), ex=self.cache_policy.get_expiration_time())
            print(f"Features materialized for key: {key}")

    def get_features(self, key: str) -> Dict[str, Any]:
        """
        Retrieve features from Redis cache.

        Args:
            key (str): The key for which features are to be retrieved.

        Returns:
            Dict[str, Any]: A dictionary of features if found, else an empty dictionary.
        """
        cached_data = self.redis_client.get(key)
        if cached_data:
            print(f"Features retrieved for key: {key}")
            return json.loads(cached_data)
        print(f"No cached features found for key: {key}")
        return {}

    def invalidate_cache(self, key: str) -> None:
        """
        Invalidate the cache for a specific key.

        Args:
            key (str): The key for which the cache should be invalidated.
        """
        self.redis_client.delete(key)
        print(f"Cache invalidated for key: {key}")

def main() -> None:
    redis_client = get_redis_client()
    cache_policy = CachePolicy(timedelta(minutes=10))
    feature_materializer = FeatureMaterializer(redis_client, cache_policy)

    # Example usage
    example_key = "patient:123:features"
    example_features = {"heart_rate": 72, "blood_pressure": "120/80"}
    
    feature_materializer.materialize_features(example_key, example_features)
    features = feature_materializer.get_features(example_key)
    print(features)
    feature_materializer.invalidate_cache(example_key)

if __name__ == "__main__":
    main()