---
layout: default
title: Pediatric Fever Chatbot API
nav_order: 2
---

# Pediatric Fever Chatbot API

Welcome to the official documentation for the **Fever Model** of **Docokids**, an AI-driven solution for pediatric fever assessment operating via a conversational API. This API leverages AI to assist in handling pediatric fever-related conversations, integrating seamlessly with platforms like DocoChat.

## Features

- **AI-Driven Responses**: Provides intelligent responses based on pediatric fever-related queries
- **Advanced Prompt Engineering**: Sophisticated conversation system that simulates real pediatric consultations
- **DocoChat Integration**: Easily integrates with DocoChat for real-time communication
- **FastAPI Framework**: Built using FastAPI for high performance and ease of use
- **Comprehensive Documentation**: Detailed guides and references to assist developers
- **Multiple LLM Support**: Seamless switching between LLM providers (OpenAI, Gemini, local)

## 🧠 Prompt Engineering System

The chatbot implements an advanced **prompt engineering system** that simulates real pediatric consultations through structured conversation phases:

### **Conversation Phases**

1. **INITIAL**: First interaction - asks for child's age
2. **DISCOVERY**: Symptom exploration - one question at a time
3. **ASSESSMENT**: Detailed evaluation - intensity, duration, behavior
4. **GUIDANCE**: Educational guidance and recommendations

### **Key Features**

- **One Question Per Response**: Ensures focused, natural conversation flow
- **Context-Aware Questions**: Adapts questions based on information already provided
- **Medical Safety Checks**: Automatic detection of emergency symptoms
- **Structured Discovery**: Progressive information gathering like real medical consultations
- **Pediatric Expertise**: Specialized prompts for child health assessment

For detailed documentation on the prompt engineering system, see [Prompt Engineering Guide](prompt-engineering.md).

## Architecture

```
Client (WhatsApp bot)
   ↓
FastAPI Application
   ├─ Routers: /conversations, /providers, /health
   ├─ Services: ConversationService, ProviderService
   ├─ Repositories: Redis (fast), Postgres (audit)
   └─ LLM Adapters: OpenAIClient, GeminiClient, LocalLLMClient
```

- Implements the Repository and Dependency Injection patterns in FastAPI for scalability and testability.
- Metrics with Prometheus, JSON logging, and OpenTelemetry traces ensure observability in production.

## Tech Stack

- **Python 3.10+**
- **FastAPI** (ASGI web framework)
- **Pydantic** (data validation)
- **SQLAlchemy (async)** + **PostgreSQL** (audit)
- **Redis (aioredis)** (conversational state)
- **Prometheus** + **Grafana** (metrics)
- **OpenTelemetry** (distributed traces)
- **Sentry** (error monitoring)
- **Jekyll** (documentation)
- **GitHub Pages** (documentation hosting)
- **GitHub Actions** (CI/CD)
- **Docker** (containerization)
- **Uvicorn** (ASGI server)
- **Pytest** (testing)
- **Black** (code formatting)
- **Flake8** (linting)
- **MyPy** (type checking)
- **Alembic** (database migrations)
- **JWT** (authentication)
- **OpenAPI/Swagger** (API documentation)

## Getting Started

To begin using the Pediatric Fever Chatbot API, navigate to the [Getting Started](getting-started.md) section.

For detailed information on API endpoints, refer to the [API Reference](api-reference.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for more details.

## License

This project is licensed under the **GNU GPL v3.0**. See the [LICENSE](LICENSE) file for details.

## Support

If you have questions or suggestions, open an issue on GitHub or contact us at **agomez@docokids.com**.

---

## 📄 Additional Documentation Pages

- **[Getting Started](getting-started.md)**: Complete setup and installation guide
- **[API Reference](api-reference.md)**: Detailed API documentation and examples
- **[Contributing Guide](contributing.md)**: How to contribute to the project
- **[Testing Guide](testing.md)**: Testing procedures and best practices
- **[Privacy Policy](privacy-policy.md)**: How we handle user data and privacy
- **[Project Charter](Project_charter.md)**: Project vision, mission, and licensing strategy
- **[Prompt Engineering](prompt-engineering.md)**: Advanced prompt engineering system documentation
- **[Internal Code of Conduct](internal_code_of_conduct.md)**: Internal team guidelines

---

## ⚙️ Configuring `_config.yml`

Your `_config.yml` file should be placed inside the `docs/` directory and configured as follows:

```yaml
title: Pediatric Fever Chatbot API
description: Comprehensive documentation for the AI-powered pediatric fever chatbot.
theme: just-the-docs
url: https://yourusername.github.io/your-repo-name
baseurl: "/your-repo-name"