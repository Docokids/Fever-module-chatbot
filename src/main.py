from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(
    title="DocoChat API",
    description="API para el módulo de chat de DocoKids",
    version="1.0.0"
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

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    
    # Inicializar base de datos
    await init_db(settings.postgres_url)
    logger.info("✅ Base de datos inicializada correctamente")
    
    # Inicializar Redis
    app.state.redis = await init_redis()
    logger.info("✅ Conexión a Redis establecida correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    if hasattr(app.state, 'redis'):
        await close_redis(app.state.redis)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
