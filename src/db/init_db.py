# src/db/init_db.py
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from asyncpg.exceptions import ConnectionDoesNotExistError
from src.models.schemas import Base
from src.core.config import get_settings

settings = get_settings()

async def check_postgres_connection():
    """Verifica la conexión a PostgreSQL"""
    try:
        engine = create_async_engine(settings.postgres_url)
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        print("✅ Conexión a PostgreSQL exitosa")
        return True
    except Exception as e:
        print(f"❌ Error al conectar con PostgreSQL: {str(e)}")
        print("\nPor favor, verifica que:")
        print("1. PostgreSQL esté instalado y ejecutándose")
        print("2. La base de datos exista")
        print("3. Las credenciales en el archivo .env sean correctas")
        print(f"\nURL de conexión actual: {settings.postgres_url}")
        return False

async def init_db(postgres_url: str):
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    
    Args:
        postgres_url (str): URL de conexión a PostgreSQL
    """
    try:
        # Crear el motor de SQLAlchemy
        engine = create_async_engine(postgres_url)
        
        # Crear todas las tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        print("✅ Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        raise

if __name__ == "__main__":
    # Para ejecutar este script directamente
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    postgres_url = os.getenv("POSTGRES_URL")
    
    if not postgres_url:
        raise ValueError("POSTGRES_URL no está definida en el archivo .env")
    
    asyncio.run(init_db(postgres_url)) 