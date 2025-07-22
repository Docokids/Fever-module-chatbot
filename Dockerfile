FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y scripts de instalación
COPY requirements.txt .
COPY requirements-gemini.txt .
COPY requirements-openai.txt .
COPY requirements-deepseek.txt .
COPY requirements-local.txt .
COPY requirements-dev.txt .
COPY install_llm_deps.py .

# Instalar solo dependencias core primero
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo .env primero
COPY .env .

# Copiar el código de la aplicación
COPY . .

# Instalar dependencias LLM según variable de entorno
ARG LLM_PROVIDERS=""
ENV LLM_PROVIDERS=${LLM_PROVIDERS}
RUN python install_llm_deps.py

# Exponer el puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 