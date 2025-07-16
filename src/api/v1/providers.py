# src/api/v1/providers.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from pydantic import BaseModel
from src.providers.factory import get_available_providers, get_llm_client
from src.core.config import get_settings, Settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/providers", tags=["providers"])

class ProviderInfo(BaseModel):
    name: str
    available: bool
    configured: bool
    model: str | None = None
    temperature: float | None = None

class ProviderListResponse(BaseModel):
    providers: List[ProviderInfo]
    current_provider: str
    total_available: int

@router.get(
    "",
    response_model=ProviderListResponse,
    summary="Listar proveedores LLM disponibles",
    openapi_extra={
        "requestBody": None
    }
)
async def list_providers():
    """
    Lista todos los proveedores LLM disponibles y su estado de configuración.
    """
    try:
        settings = get_settings()
        available_providers = get_available_providers()
        
        providers_info = []
        for provider_name in available_providers:
            # Verificar si está configurado
            configured = False
            model = None
            temperature = None
            
            try:
                # Intentar crear el adapter para verificar configuración
                adapter = get_llm_client(settings)
                configured = True
                model = settings.llm_model
                temperature = settings.llm_temperature
            except Exception as e:
                logger.warning(f"Provider {provider_name} not properly configured: {str(e)}")
            
            providers_info.append(ProviderInfo(
                name=provider_name,
                available=True,
                configured=configured,
                model=model,
                temperature=temperature
            ))
        
        return ProviderListResponse(
            providers=providers_info,
            current_provider=settings.llm_provider,
            total_available=len([p for p in providers_info if p.configured])
        )
        
    except Exception as e:
        logger.error(f"Error listing providers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing providers: {str(e)}"
        )

@router.get(
    "/health",
    summary="Verificar salud de proveedores",
    openapi_extra={
        "requestBody": None
    }
)
async def health_check():
    """
    Verifica la salud de todos los proveedores configurados.
    """
    try:
        settings = get_settings()
        adapter = get_llm_client(settings)
        
        # Test simple de salud
        test_message = "Hola"
        test_context = []
        
        # Intentar generar una respuesta simple
        response = await adapter.generate(test_context)
        
        return {
            "status": "healthy",
            "provider": settings.llm_provider,
            "message": "Provider is responding correctly"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Provider health check failed: {str(e)}"
        )
