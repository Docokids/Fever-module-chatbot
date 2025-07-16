#!/usr/bin/env python3
"""
Script de ejemplo para probar los diferentes proveedores LLM.
Este script demuestra cómo cambiar entre diferentes proveedores y cómo funcionan.
"""

import asyncio
import os
from typing import List
from src.models.schemas import Message
from src.providers.factory import get_llm_client, get_available_providers
from src.core.config import Settings

async def test_provider(provider_name: str, api_key: str = None):
    """
    Prueba un proveedor específico.
    
    Args:
        provider_name: Nombre del proveedor a probar
        api_key: API key para el proveedor (opcional)
    """
    print(f"\n{'='*50}")
    print(f"Probando proveedor: {provider_name}")
    print(f"{'='*50}")
    
    try:
        # Configurar settings para el proveedor
        settings_dict = {
            "llm_provider": provider_name,
            "llm_model": "gemini-2.0-flash" if provider_name == "gemini" else "gpt-4o-mini",
            "llm_temperature": 0.7
        }
        
        # Agregar API key si se proporciona
        if api_key:
            if provider_name == "gemini":
                settings_dict["gemini_api_key"] = api_key
            elif provider_name == "openai":
                settings_dict["openai_api_key"] = api_key
            elif provider_name == "deepseek":
                settings_dict["deepseek_api_key"] = api_key
        
        settings = Settings(**settings_dict)
        
        # Crear cliente LLM
        llm_client = get_llm_client(settings)
        print(f"✅ Cliente {provider_name} creado exitosamente")
        
        # Crear contexto de prueba
        test_context = [
            Message(role="user", content="Hola, mi hijo tiene 2 años y tiene fiebre de 38 grados")
        ]
        
        print(f"📝 Enviando mensaje de prueba...")
        
        # Generar respuesta
        response = await llm_client.generate(test_context)
        
        print(f"🤖 Respuesta del {provider_name}:")
        print(f"   {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con {provider_name}: {str(e)}")
        return False

async def test_all_providers():
    """Prueba todos los proveedores disponibles."""
    print("🚀 Iniciando pruebas de proveedores LLM")
    
    # Obtener proveedores disponibles
    available_providers = get_available_providers()
    print(f"📋 Proveedores disponibles: {', '.join(available_providers)}")
    
    # Configurar API keys desde variables de entorno
    api_keys = {
        "gemini": os.getenv("GEMINI_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
        "deepseek": os.getenv("DEEPSEEK_API_KEY"),
        "local": None  # Local no requiere API key
    }
    
    results = {}
    
    # Probar cada proveedor
    for provider in available_providers:
        api_key = api_keys.get(provider)
        success = await test_provider(provider, api_key)
        results[provider] = success
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE PRUEBAS")
    print(f"{'='*50}")
    
    for provider, success in results.items():
        status = "✅ EXITOSO" if success else "❌ FALLÓ"
        print(f"{provider.upper():<15} : {status}")
    
    successful_providers = [p for p, s in results.items() if s]
    print(f"\n🎉 Proveedores funcionando: {', '.join(successful_providers) if successful_providers else 'Ninguno'}")

def main():
    """Función principal."""
    print("🤖 DocoKids LLM Provider Test")
    print("Este script prueba todos los proveedores LLM configurados.")
    print("\n💡 Asegúrate de tener las variables de entorno configuradas:")
    print("   - GEMINI_API_KEY")
    print("   - OPENAI_API_KEY") 
    print("   - DEEPSEEK_API_KEY")
    print("\n🔧 Para modelos locales, asegúrate de tener torch y transformers instalados.")
    
    # Ejecutar pruebas
    asyncio.run(test_all_providers())

if __name__ == "__main__":
    main() 