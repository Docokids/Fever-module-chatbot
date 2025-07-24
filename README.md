# 🤖 Pediatric Fever Chatbot API

[![Documentation Status](https://img.shields.io/badge/docs-online-success)](URL_DOCUMENTATION)  
[![License: GPL v3](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)  
[![Repo Status](https://img.shields.io/badge/status-active-brightgreen)](URL_REPO)  
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-green)](https://fastapi.tiangolo.com/)  
[![CI](https://img.shields.io/badge/ci-GitHub%20Actions-blue)](URL_CI)

---

## 📌 Table of Contents

- [About](#about)
- [Architecture](#architecture)
- [LLM Providers](#llm-providers)
- [Tech Stack](#tech-stack)
- [Prompt Engineering System](#prompt-engineering-system)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [LLM Provider Configuration](#llm-provider-configuration)
- [Contributing](#contributing)
- [License](#license)
- [Help and Support](#help-and-support)

---

## 🔍 About

This repository contains the source code for the **Fever Model** of **Docokids**, an AI-driven solution for pediatric fever assessment operating via a conversational API. The model has completed the **Exploratory Data Analysis (EDA)** phase and is currently progressing through **Feature Engineering** and **Model Fine-tuning**. 

The FastAPI-based API manages the conversation flow, maintains context, and provides a **modular LLM architecture** that allows seamless switching between different LLM providers (OpenAI, Gemini, DeepSeek, Local) in an isolated manner.

---

## 🌍 Architecture

### LLM Provider Architecture

```
Client (WhatsApp bot)
   ↓
FastAPI Application
   ├─ Routers: /conversations, /providers, /health
   ├─ Services: ConversationService, ProviderService
   ├─ Repositories: Redis (fast), Postgres (audit)
   └─ LLM Adapters: 
       ├─ BaseLLMAdapter (Template Method)
       ├─ GeminiAdapter
       ├─ OpenAIAdapter
       ├─ DeepSeekAdapter
       └─ LocalAdapter
```

### Key Design Patterns

- **Adapter Pattern**: Each LLM provider has its own adapter implementing a common interface
- **Template Method Pattern**: Base adapter provides common functionality while adapters implement provider-specific logic
- **Factory Pattern**: Dynamic provider selection and registration
- **Dependency Injection**: Clean separation of concerns and testability

---

## 🤖 LLM Providers

The system supports multiple LLM providers with a unified interface:

### Supported Providers

| Provider | Status | API Key Required | Models |
|----------|--------|------------------|--------|
| **Gemini** | ✅ Production Ready | `GEMINI_API_KEY` | `gemini-2.0-flash` |
| **OpenAI** | ✅ Production Ready | `OPENAI_API_KEY` | `gpt-4o-mini`, `gpt-4` |
| **DeepSeek** | ✅ Production Ready | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| **Local** | ✅ Development Ready | None | `allenai/OLMo-2-1124-13B-Instruct` |

### Provider Features

- **Unified Interface**: All providers implement the same `LLMClient` interface
- **Context-Aware**: Each provider receives the same conversation context
- **Safety Checks**: Built-in emergency symptom detection
- **Response Validation**: Ensures medical-appropriate responses
- **Fallback Handling**: Graceful error handling and fallback responses

### Switching Providers

Change providers by updating the `LLM_PROVIDER` environment variable:

```bash
# Use Gemini (default)
LLM_PROVIDER=gemini

# Use OpenAI
LLM_PROVIDER=openai

# Use DeepSeek
LLM_PROVIDER=deepseek

# Use Local Model
LLM_PROVIDER=local
```

---

## 🏗️ Tech Stack

- **Python 3.10+**
- **FastAPI** (ASGI web framework)
- **Pydantic** (data validation)
- **SQLAlchemy (async)** + **PostgreSQL** (audit)
- **Redis (aioredis)** (conversational state)
- **LLM Providers**:
  - **Google Gemini** (`google-generativeai`)
  - **OpenAI** (`openai`)
  - **DeepSeek** (`requests`)
  - **Local Models** (`torch`, `transformers`)
- **Prometheus** + **Grafana** (metrics)
- **OpenTelemetry** (distributed traces)
- **Sentry** (error monitoring)
- **Docker** (containerization)
- **Uvicorn** (ASGI server)
- **Pytest** (testing)

---

## 🧠 Prompt Engineering System

The system uses a sophisticated prompt engineering approach with:

### Conversation Phases

1. **Initial**: First interaction, asks for child's age
2. **Discovery**: Gathers symptoms and medical history
3. **Assessment**: Evaluates symptom severity and duration
4. **Guidance**: Provides educational information and recommendations

### Safety Features

- **Emergency Detection**: Automatic detection of critical symptoms
- **Medical Disclaimer**: Always recommends consulting a doctor
- **Response Validation**: Ensures appropriate medical responses

### Example Conversation Flow

```
User: "Hola"
Bot: "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?"

User: "2 años"
Bot: "¿Cuál es el síntoma principal que te preocupa?"

User: "Tiene fiebre"
Bot: "¿Cuál es la temperatura del niño?"

User: "39°C"
Bot: "¿Cuánto tiempo lleva con fiebre?"
```

For detailed documentation on the prompt engineering system, see [Prompt Engineering Guide](documentation/prompt-engineering.md).

---

## 🏁 Getting Started

Follow these steps to run the project locally:

### Using Docker Compose (Recommended)

1. Clone the repository:

   ```sh
   git clone URL_REPO && cd fever-model-docokids
   ```

2. Create a `.env` file in the root directory with your configuration:

   ```sh
   APP_NAME=DocoChat
   LLM_PROVIDER=gemini  # or openai, deepseek, local
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   REDIS_URL=redis://redis:6379/0
   POSTGRES_URL=postgresql+asyncpg://postgres:postgres@db:5432/docochat
   ```

3. Start the services using Docker Compose:

   ```sh
   docker-compose up --build
   ```

   This will start:
   - FastAPI application on http://localhost:8000
   - PostgreSQL database
   - Redis cache

4. Access the interactive API documentation at http://localhost:8000/docs

---

## 🚀 Usage

### API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/conversations` | Lists all conversations with message count and last message timestamp |
| POST | `/conversations` | Initiates a new conversation |
| POST | `/conversations/{id}/messages` | Sends a user message and receives model response |
| GET | `/conversations/{id}/history` | Retrieves full conversation history |
| GET | `/providers` | Lists available LLM providers and their status |
| GET | `/providers/health` | Checks health of configured LLM providers |

### LLM Provider Configuration

#### Environment Variables

```bash
# Select LLM Provider
LLM_PROVIDER=gemini  # gemini, openai, deepseek, local

# API Keys
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# Model Configuration
LLM_MODEL=gemini-2.0-flash  # Model name for selected provider
LLM_TEMPERATURE=0.7         # Generation temperature (0.0-2.0)
LLM_MAX_TOKENS=1000         # Maximum tokens to generate
```

#### Provider-Specific Configuration

**Gemini**:
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
LLM_MODEL=gemini-2.0-flash
```

**OpenAI**:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
LLM_MODEL=gpt-4o-mini
```

**DeepSeek**:
```bash
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
LLM_MODEL=deepseek-chat
```

**Local Models**:
```bash
LLM_PROVIDER=local
LLM_MODEL=allenai/OLMo-2-1124-13B-Instruct
# No API key required
```

### Example Requests

```sh
# List all conversations
curl -X GET http://localhost:8000/conversations

# Create new conversation
curl -X POST http://localhost:8000/conversations

# Send message
curl -X POST http://localhost:8000/conversations/{id}/messages \
  -H "Content-Type: application/json" \
  -d '{"msg": {"role": "user", "content": "¿Cómo tratarías la fiebre en un bebé?"}}'

# List providers
curl -X GET http://localhost:8000/providers

# Check provider health
curl -X GET http://localhost:8000/providers/health
```

### Testing Providers

Use the provided test script to verify all providers:

```bash
python examples/test_providers.py
```

---

## 🧪 CI/CD y Cobertura de Tests

Este proyecto utiliza **GitHub Actions** para CI/CD. El workflow está configurado para:
- Ejecutar **solo los tests** en cada push o pull request a `main`.
- Exigir una **cobertura mínima de código del 40%** (usando pytest-cov).
- Si la cobertura baja de ese umbral o algún test falla, el PR será rechazado automáticamente.

### Cómo ejecutar los tests y ver la cobertura localmente

```sh
# Ejecutar todos los tests y ver la cobertura en consola
pytest --cov=src --cov-report=term-missing -v

# (Opcional) Ver un reporte HTML navegable
pytest --cov=src --cov-report=html
# Luego abre htmlcov/index.html en tu navegador
```

### Buenas prácticas
- Escribe tests para cada nueva funcionalidad.
- No elimines tests sin justificación.
- Si deshabilitas tests, documenta el motivo y crea un issue para su reactivación.
- Mantén o mejora la cobertura en cada PR.

### Tests deshabilitados
- Los tests de `tests/test_adapters.py` y `tests/test_repositories.py` están deshabilitados temporalmente. Se recomienda reactivarlos y corregirlos en el futuro para mejorar la cobertura y robustez del proyecto.

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_adapters.py

# Run with coverage
pytest --cov=src
```

---

## 🔧 Development

### Adding a New LLM Provider

1. Create a new adapter in `src/providers/adapters/`:

```python
from src.providers.adapters.base_adapter import BaseLLMAdapter

class NewProviderAdapter(BaseLLMAdapter):
    def _format_messages_for_provider(self, context, system_prompt):
        # Format messages for your provider
        pass
    
    async def _call_provider(self, formatted_messages):
        # Call your provider's API
        pass
```

2. Register the adapter in `src/providers/factory.py`:

```python
from .adapters.new_provider_adapter import NewProviderAdapter

def _register_default_adapters(self):
    self.register_adapter("new_provider", NewProviderAdapter)
```

3. Add configuration in `src/core/config.py`:

```python
llm_provider: Literal["gemini", "openai", "deepseek", "local", "new_provider"] = "gemini"
new_provider_api_key: Optional[str] = os.getenv("NEW_PROVIDER_API_KEY")
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](documentation/contributing.md) for more details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

---

## 📄 License

This project is licensed under the **GNU GPL v3.0**. See the [LICENSE](LICENSE) file for details.

---

## 🆘 Help and Support

If you have questions or suggestions, open an issue on GitHub or contact us at **agomez@docokids.com**.

### Common Issues

**Provider not working?**
- Check API key configuration
- Verify provider is enabled in settings
- Check logs for detailed error messages

**Local model not loading?**
- Ensure sufficient RAM/VRAM
- Install required dependencies: `pip install torch transformers`
- Check model name is correct

**Response quality issues?**
- Adjust temperature settings
- Check prompt engineering configuration
- Verify conversation context is being passed correctly

---

## 📈 Roadmap

- [ ] **Load Balancing**: Automatic distribution between providers
- [ ] **Fallback System**: Automatic failover to backup providers
- [ ] **Performance Metrics**: Detailed provider performance tracking
- [ ] **A/B Testing**: Compare provider responses
- [ ] **Custom Models**: Support for fine-tuned models
- [ ] **Streaming**: Real-time response streaming
- [ ] **Multi-modal**: Support for image and voice inputs 
