# src/db/session.py
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import get_settings

settings = get_settings()

# Redis pool asíncrono
async def init_redis():
    return await aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True
    )  # :contentReference[oaicite:0]{index=0}

# Engine y sesión asíncrona de SQLAlchemy
engine = create_async_engine(settings.postgres_url, future=True)  # :contentReference[oaicite:1]{index=1}
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    # Aquí podrías invocar a Alembic o crear tablas manualmente
    pass

async def close_db():
    await engine.dispose()
