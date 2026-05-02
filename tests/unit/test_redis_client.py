import pytest
import redis
from unittest.mock import patch, MagicMock
from src.features.redis_client import RedisClient
from src.features.materializer import FeatureMaterializer
from src.features.cache_policy import CachePolicy


@pytest.fixture
def redis_client() -> RedisClient:
    """Fixture for RedisClient."""
    return RedisClient(host='localhost', port=6379, db=0)


@pytest.fixture
def feature_materializer(redis_client: RedisClient) -> FeatureMaterializer:
    """Fixture for FeatureMaterializer."""
    return FeatureMaterializer(redis_client)


def test_redis_client_set_and_get(redis_client: RedisClient) -> None:
    """Test setting and getting a value in Redis."""
    key = 'test_key'
    value = 'test_value'
    
    redis_client.set(key, value)
    retrieved_value = redis_client.get(key)
    
    assert retrieved_value == value


def test_redis_client_cache_invalidation(redis_client: RedisClient) -> None:
    """Test cache invalidation in Redis."""
    key = 'test_key'
    value = 'test_value'
    
    redis_client.set(key, value)
    redis_client.invalidate(key)
    
    retrieved_value = redis_client.get(key)
    
    assert retrieved_value is None


@patch('src.features.materializer.FeatureMaterializer.materialize')
def test_feature_materialization(mock_materialize: MagicMock, feature_materializer: FeatureMaterializer) -> None:
    """Test feature materialization."""
    mock_materialize.return_value = True
    result = feature_materializer.materialize('user_id', {'feature1': 1, 'feature2': 2})
    
    assert result is True
    mock_materialize.assert_called_once_with('user_id', {'feature1': 1, 'feature2': 2})


def test_cache_policy(redis_client: RedisClient) -> None:
    """Test cache policy for feature materialization."""
    policy = CachePolicy(expiration_time=60)
    key = 'test_key'
    value = 'test_value'
    
    redis_client.set(key, value)
    assert redis_client.get(key) == value
    
    policy.invalidate(redis_client, key)
    assert redis_client.get(key) is None


def test_redis_client_connection_error() -> None:
    """Test RedisClient connection error handling."""
    with pytest.raises(redis.ConnectionError):
        RedisClient(host='invalid_host', port=6379, db=0)
# 10:04:05 — automated update
# test marker: test: add test for cache invalidation on stale features
_TEST_MARKER = 'test_redis_client'
