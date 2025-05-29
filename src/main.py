from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.v1 import conversations
from src.db.session import init_db, close_db
from src.cache.redis import init_redis, close_redis
from src.core.config import get_settings
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    
    # Inicializar base de datos
    await init_db(settings.postgres_url)
    logger.info("✅ Base de datos inicializada correctamente")
    
    # Inicializar Redis
    app.state.redis = await init_redis()
    logger.info("✅ Conexión a Redis establecida correctamente")
    
    yield
    
    # Shutdown
    await close_db()
    if hasattr(app.state, 'redis'):
        await close_redis(app.state.redis)

app = FastAPI(
    title="DocoChat API",
    description="API para el módulo de chat de DocoKids",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(conversations.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
