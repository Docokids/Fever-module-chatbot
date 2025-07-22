#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

REQUIREMENTS_MAP = {
    'gemini': 'requirements-gemini.txt',
    'openai': 'requirements-openai.txt',
    'deepseek': 'requirements-deepseek.txt',
    'local': 'requirements-local.txt',
    'dev': 'requirements-dev.txt',
    'monitoring': 'requirements-dev.txt',  # monitoring está incluido en dev
}

CORE_REQUIREMENTS = 'requirements.txt'

ALL_OPTIONS = list(REQUIREMENTS_MAP.keys())


def pip_install(req_file):
    if Path(req_file).exists():
        print(f"📦 Instalando dependencias de {req_file} ...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
    else:
        print(f"⚠️  Archivo {req_file} no encontrado, se omite.")

def parse_providers_from_env():
    env = os.getenv('LLM_PROVIDERS', '')
    if not env:
        return []
    return [x.strip().lower() for x in env.split(',') if x.strip()]

def interactive_select():
    print("¿Qué proveedor(es) de LLM deseas instalar?")
    print("Opciones disponibles:")
    for idx, opt in enumerate(ALL_OPTIONS, 1):
        print(f"  {idx}. {opt}")
    print("Puedes seleccionar varios separados por coma (ej: 1,3,dev)")
    sel = input("Selecciona opción(es): ").strip()
    if not sel:
        return []
    result = set()
    for part in sel.split(','):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(ALL_OPTIONS):
            result.add(ALL_OPTIONS[int(part)-1])
        elif part in ALL_OPTIONS:
            result.add(part)
    return list(result)

def main():
    print("🧩 Instalador selectivo de dependencias LLM para DocoKids")
    print("----------------------------------------------")
    # Siempre instalar core
    pip_install(CORE_REQUIREMENTS)
    # Detectar modo
    providers = parse_providers_from_env()
    if not providers and sys.stdin.isatty():
        providers = interactive_select()
    if not providers:
        print("No se seleccionó ningún proveedor extra. Solo se instalaron dependencias core.")
        return
    installed = []
    for prov in providers:
        req = REQUIREMENTS_MAP.get(prov)
        if req:
            pip_install(req)
            installed.append(prov)
        else:
            print(f"⚠️  Opción desconocida: {prov}")
    print("\n✅ Resumen de instalación:")
    print(f"- Core (FastAPI, DB, etc): instalado")
    for prov in installed:
        print(f"- {prov}: instalado")
    print("----------------------------------------------")
    print("¡Listo! Solo tienes lo necesario para tu flujo.")

if __name__ == "__main__":
    main() 