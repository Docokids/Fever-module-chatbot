from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from src.api.v1 import conversations, providers
from src.db.session import init_db, close_db
from src.cache.redis import init_redis, close_redis
from src.core.config import get_settings
from src.core.exceptions import (
    APIError,
    api_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
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

# Registrar manejadores de errores
app.add_exception_handler(APIError, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Incluir routers
app.include_router(conversations.router)
app.include_router(providers.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
