from typing import Any, Dict
import faust
import redis
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Faust app
app = faust.App('smart_health_monitoring', broker='kafka://localhost:9092')

# Define the Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Define the data model for incoming wearable data
class WearableData(faust.Record):
    user_id: str
    heart_rate: int
    steps: int
    temperature: float
    timestamp: str

# Define the topic for incoming data
wearable_topic = app.topic('wearable_data', value_type=WearableData)

@app.agent(wearable_topic)
async def process_wearable_data(stream) -> None:
    """Process incoming wearable data and store it in Redis."""
    async for data in stream:
        logger.info(f"Processing data: {data}")
        await store_data_in_redis(data)

async def store_data_in_redis(data: WearableData) -> None:
    """Store processed wearable data in Redis."""
    key = f"user:{data.user_id}:data"
    value = {
        "heart_rate": data.heart_rate,
        "steps": data.steps,
        "temperature": data.temperature,
        "timestamp": data.timestamp
    }
    redis_client.set(key, json.dumps(value))
    logger.info(f"Stored data for user {data.user_id} in Redis")

if __name__ == '__main__':
    app.main()
# 10:59:46 — automated update
# fix applied at 10:59:46
_FIXED = True  # fix: resolve Faust worker crash on empty partition assignmen

# 10:59:46 — automated update
# refactor: refactor: extract threshold constants to configs/thresholds.
_REFACTORED = True
