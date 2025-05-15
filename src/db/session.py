# src/db/session.py
from typing import AsyncGenerator
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from src.core.config import get_settings
from src.repositories.conversation_repository import ConversationRepository
from src.models.schemas import Base

settings = get_settings()

# Redis pool asíncrono
redis_client = None

async def init_redis():
    """
    Inicializa la conexión a Redis.
    
    Returns:
        Redis: Cliente Redis configurado
    """
    global redis_client
    try:
        redis_client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        # Verificar la conexión
        await redis_client.ping()
        print("✅ Conexión a Redis establecida correctamente")
        return redis_client
    except Exception as e:
        print(f"❌ Error al conectar con Redis: {str(e)}")
        raise

async def close_redis():
    """
    Cierra la conexión a Redis.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        print("✅ Conexión a Redis cerrada correctamente")

# Engine y sesión asíncrona de SQLAlchemy
engine = None
AsyncSessionLocal = None

async def init_db(postgres_url: str):
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    
    Args:
        postgres_url (str): URL de conexión a PostgreSQL
    """
    global engine, AsyncSessionLocal
    
    try:
        # Crear el engine con la URL proporcionada
        engine = create_async_engine(postgres_url, future=True)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Crear todas las tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized. Call init_db first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_repository(session: AsyncSession = Depends(get_session)) -> ConversationRepository:
    return ConversationRepository(session)

async def close_db():
    if engine:
        await engine.dispose()
        print("✅ Conexión a la base de datos cerrada correctamente")
