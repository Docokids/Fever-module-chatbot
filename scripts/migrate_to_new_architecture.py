#!/usr/bin/env python3
"""
Script de migración para transicionar del sistema anterior al nuevo sistema de adapters.
Este script ayuda a verificar la compatibilidad y migrar configuraciones.
"""

import os
import sys
import asyncio
from typing import Dict, Any
import json

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.providers.factory import get_available_providers, get_llm_client
from src.core.config import Settings
from src.models.schemas import Message

def check_environment():
    """Verifica la configuración del entorno."""
    print("🔍 Verificando configuración del entorno...")
    
    # Variables de entorno requeridas
    env_vars = {
        "GEMINI_API_KEY": "Gemini API Key",
        "OPENAI_API_KEY": "OpenAI API Key", 
        "DEEPSEEK_API_KEY": "DeepSeek API Key",
        "LLM_PROVIDER": "LLM Provider",
        "LLM_MODEL": "LLM Model",
        "LLM_TEMPERATURE": "LLM Temperature"
    }
    
    missing_vars = []
    configured_vars = []
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            configured_vars.append(f"✅ {description}: {value[:10]}...")
        else:
            missing_vars.append(f"❌ {description}: No configurada")
    
    print("\nVariables de entorno configuradas:")
    for var in configured_vars:
        print(f"  {var}")
    
    if missing_vars:
        print("\nVariables de entorno faltantes:")
        for var in missing_vars:
            print(f"  {var}")
    
    return len(missing_vars) == 0

def test_provider_compatibility(provider_name: str, settings: Settings) -> Dict[str, Any]:
    """Prueba la compatibilidad de un proveedor específico."""
    print(f"\n🧪 Probando compatibilidad de {provider_name}...")
    
    try:
        # Crear settings específicos para el proveedor
        test_settings = Settings(
            llm_provider=provider_name,
            llm_model=settings.llm_model,
            llm_temperature=settings.llm_temperature
        )
        
        # Agregar API key si está disponible
        if provider_name == "gemini" and settings.gemini_api_key:
            test_settings.gemini_api_key = settings.gemini_api_key
        elif provider_name == "openai" and settings.openai_api_key:
            test_settings.openai_api_key = settings.openai_api_key
        elif provider_name == "deepseek" and settings.deepseek_api_key:
            test_settings.deepseek_api_key = settings.deepseek_api_key
        
        # Intentar crear el adapter
        adapter = get_llm_client(test_settings)
        
        # Test simple de generación
        test_context = [
            Message(role="user", content="Hola")
        ]
        
        response = asyncio.run(adapter.generate(test_context))
        
        return {
            "status": "success",
            "message": f"✅ {provider_name} funciona correctamente",
            "response_preview": response.content[:100] + "..." if len(response.content) > 100 else response.content
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Error con {provider_name}: {str(e)}",
            "response_preview": None
        }

async def run_migration_tests():
    """Ejecuta las pruebas de migración."""
    print("🚀 Iniciando pruebas de migración...")
    
    # Verificar entorno
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  Algunas variables de entorno no están configuradas.")
        print("   Esto puede causar problemas con ciertos proveedores.")
    
    # Obtener configuración actual
    settings = Settings()
    print(f"\n📋 Configuración actual:")
    print(f"   Proveedor: {settings.llm_provider}")
    print(f"   Modelo: {settings.llm_model}")
    print(f"   Temperatura: {settings.llm_temperature}")
    
    # Obtener proveedores disponibles
    available_providers = get_available_providers()
    print(f"\n📦 Proveedores disponibles: {', '.join(available_providers)}")
    
    # Probar cada proveedor
    results = {}
    for provider in available_providers:
        result = test_provider_compatibility(provider, settings)
        results[provider] = result
    
    # Mostrar resultados
    print(f"\n{'='*60}")
    print("📊 RESULTADOS DE MIGRACIÓN")
    print(f"{'='*60}")
    
    successful_providers = []
    failed_providers = []
    
    for provider, result in results.items():
        if result["status"] == "success":
            successful_providers.append(provider)
            print(f"✅ {provider.upper()}: {result['message']}")
            if result["response_preview"]:
                print(f"   Respuesta: {result['response_preview']}")
        else:
            failed_providers.append(provider)
            print(f"❌ {provider.upper()}: {result['message']}")
    
    # Resumen
    print(f"\n{'='*60}")
    print("📈 RESUMEN")
    print(f"{'='*60}")
    print(f"✅ Proveedores funcionando: {len(successful_providers)}")
    print(f"❌ Proveedores con problemas: {len(failed_providers)}")
    
    if successful_providers:
        print(f"\n🎉 Proveedores listos para usar: {', '.join(successful_providers)}")
    
    if failed_providers:
        print(f"\n⚠️  Proveedores que necesitan atención: {', '.join(failed_providers)}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if settings.llm_provider not in successful_providers:
        print(f"   ⚠️  El proveedor actual ({settings.llm_provider}) no está funcionando.")
        if successful_providers:
            print(f"   🔄 Considera cambiar a: {successful_providers[0]}")
    
    if len(successful_providers) > 1:
        print(f"   🎯 Tienes múltiples proveedores funcionando. Considera usar load balancing.")
    
    if failed_providers:
        print(f"   🔧 Revisa la configuración de: {', '.join(failed_providers)}")
    
    return len(successful_providers) > 0

def generate_migration_report():
    """Genera un reporte de migración."""
    print(f"\n📄 Generando reporte de migración...")
    
    report = {
        "timestamp": asyncio.run(get_current_timestamp()),
        "architecture_version": "2.0.0",
        "migration_status": "completed",
        "features": [
            "Modular LLM Adapters",
            "Unified Provider Interface", 
            "Template Method Pattern",
            "Factory Pattern",
            "Enhanced Error Handling",
            "Provider Health Checks"
        ],
        "supported_providers": get_available_providers(),
        "breaking_changes": [
            "GeminiClient renamed to GeminiAdapter",
            "New BaseLLMAdapter interface",
            "Updated factory pattern",
            "Enhanced configuration validation"
        ],
        "migration_steps": [
            "1. Update environment variables",
            "2. Test all providers",
            "3. Update API calls if needed",
            "4. Monitor logs for any issues"
        ]
    }
    
    # Guardar reporte
    with open("migration_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Reporte de migración guardado en migration_report.json")

async def get_current_timestamp():
    """Obtiene el timestamp actual."""
    from datetime import datetime
    return datetime.now().isoformat()

def main():
    """Función principal del script de migración."""
    print("🔄 DocoKids LLM Architecture Migration Tool")
    print("Este script ayuda a migrar al nuevo sistema de adapters LLM.")
    print("=" * 60)
    
    try:
        # Ejecutar pruebas de migración
        success = asyncio.run(run_migration_tests())
        
        if success:
            print(f"\n🎉 ¡Migración exitosa! El nuevo sistema está listo para usar.")
            
            # Generar reporte
            generate_migration_report()
            
            print(f"\n📋 Próximos pasos:")
            print(f"   1. Actualiza tu configuración de producción")
            print(f"   2. Monitorea los logs por posibles problemas")
            print(f"   3. Considera implementar load balancing si tienes múltiples proveedores")
            print(f"   4. Revisa el reporte de migración para más detalles")
            
        else:
            print(f"\n❌ La migración encontró problemas.")
            print(f"   Revisa la configuración y vuelve a ejecutar el script.")
            
    except Exception as e:
        print(f"\n💥 Error durante la migración: {str(e)}")
        print(f"   Revisa los logs para más detalles.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 