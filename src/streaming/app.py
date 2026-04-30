import faust
import json
from typing import Dict, Any
from src.streaming.agents import process_wearable_data
from src.streaming.models import WearableData

app = faust.App('health_monitoring', broker='kafka://localhost:9092')

# Define the topic for wearable data
wearable_data_topic = app.topic('wearable_data', value_type=dict)

@app.agent(wearable_data_topic)
async def wearable_data_agent(stream) -> None:
    """
    Process incoming wearable data in real-time.

    Args:
        stream: A Faust stream of wearable data.
    """
    async for value in stream:
        wearable_data = WearableData(**value)
        processed_data = await process_wearable_data(wearable_data)
        await save_to_redis(processed_data)

async def save_to_redis(data: Dict[str, Any]) -> None:
    """
    Save processed data to Redis.

    Args:
        data: The processed wearable data to save.
    """
    import aioredis

    redis_client = aioredis.from_url("redis://localhost")
    await redis_client.hmset_dict(data['user_id'], data)
    await redis_client.close()

if __name__ == '__main__':
    app.main()
# 10:59:46 — automated update
# feat: add real-time alert sink to Redis pub/sub
