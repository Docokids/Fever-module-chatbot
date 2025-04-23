from fastapi import FastAPI, Depends
from src.core.config import get_settings, Settings
from src.db.session import init_db, close_db
from src.providers.interface import LLMClient
from src.providers.factory import get_llm_client
from fastapi import FastAPI
from src.api.v1 import conversations

app = FastAPI(title="DocoChat API")

# Routers v1
app.include_router(conversations.router)

@app.on_event("startup")
async def on_startup():
    settings = get_settings()
    # Inicializar DB y cache
    await init_db(settings.postgres_url)           # :contentReference[oaicite:8]{index=8}
    await init_redis(settings.redis_url)            # :contentReference[oaicite:9]{index=9}
    # Inicializar cliente LLM  
    app.state.llm_client = get_llm_client(settings) # :contentReference[oaicite:10]{index=10}

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()                                # :contentReference[oaicite:11]{index=11}
    await close_redis()                             # :contentReference[oaicite:12]{index=12}

@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "provider": settings.llm_provider}
