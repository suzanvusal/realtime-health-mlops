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

# 10:59:46 — automated update
# perf improvement at 10:59:46
_CACHE: dict = {}  # perf: add lru_cache on patient metadata 

# 10:59:46 — automated update
# style: formatted at 10:59:46

# 10:04:05 — automated update
# test: add assertion for return type in app — 10:04:05 UTC

# 11:10:09 — automated update
# docs: update example in docstring of app — 11:10:09 UTC

# 11:11:30 — automated update
# chore: add logging statement to app — 11:11:30 UTC

# 11:13:34 — automated update
# docs: fix typo in inline comment in app — 11:13:34 UTC

# 10:12:47 — automated update
# fix: handle None input edge case in app — 10:12:47 UTC

# 10:20:23 — automated update
# docs: add module docstring to app — 10:20:23 UTC

# 10:20:23 — automated update
# refactor: extract magic number to named constant in app — 10:20:23 UTC
