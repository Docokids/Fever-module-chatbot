import redis.asyncio as redis
from src.core.config import get_settings

async def init_redis():
    settings = get_settings()
    redis_client = redis.from_url(settings.redis_url)
    return redis_client

async def close_redis(redis_client: redis.Redis):
    await redis_client.close() 