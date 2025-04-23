from fastapi import Depends
from src.db.redis_repository import RedisConversationRepository
from src.db.postgres_repository import PostgresConversationRepository
from src.db.session import init_redis

async def get_redis_repo():
    redis = await init_redis()
    return RedisConversationRepository(redis)

async def get_postgres_repo():
    # asegurar init_db si es necesario
    return PostgresConversationRepository()

def get_repository(
    repo_type: str = "redis"  # o leer de settings
):
    if repo_type == "postgres":
        return Depends(get_postgres_repo)
    return Depends(get_redis_repo)
