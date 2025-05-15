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
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Help and Support](#help-and-support)

---

## 🔍 About

This repository contains the source code for the **Fever Model** of **Docokids**, an AI-driven solution for pediatric fever assessment operating via a conversational API. The model has completed the **Exploratory Data Analysis (EDA)** phase and is currently progressing through **Feature Engineering** and **Model Fine-tuning**. The FastAPI-based API manages the conversation flow, maintains context, and allows for seamless switching between LLM providers (OpenAI, Gemini, local) in an isolated manner.

---

## 🌍 Architecture

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

---

## 🛠 Tech Stack

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
   LLM_PROVIDER=gemini  # or openai
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
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

### Manual Installation

1. Clone the repository:

   ```sh
   git clone URL_REPO && cd fever-model-docokids
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration (see above)

5. Start the application:

   ```sh
   uvicorn src.main:app --reload
   ```

---

## 🚀 Usage

### API Endpoints

| Method | Route                                 | Description                                 |
|--------|---------------------------------------|---------------------------------------------|
| GET    | `/conversations`                      | Lists all conversations with message count and last message timestamp |
| POST   | `/conversations`                      | Initiates a new conversation                |
| POST   | `/conversations/{id}/messages`        | Sends a user message and receives model response |
| GET    | `/conversations/{id}/history`         | Retrieves full conversation history         |

Example requests:

```sh
# List all conversations
curl -X GET http://localhost:8000/conversations

# Create new conversation
curl -X POST http://localhost:8000/conversations

# Send message
curl -X POST http://localhost:8000/conversations/{conversation_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "¿Cómo tratarías la fiebre en un bebé?"}'

# Get conversation history
curl -X GET http://localhost:8000/conversations/{conversation_id}/history
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -m "Add X"`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a Pull Request describing your contribution.

Follow the [style guides](https://pep8.org/) and ensure to add unit tests for new functionalities.

---

## 📜 License

This project is licensed under the **GNU GPL v3.0**. See the [LICENSE](LICENSE) file for details.

---

## 💡 Help and Support

If you have questions or suggestions, open an issue on GitHub or contact us at **agomez@docokids.com**.

Thank you for contributing to improving pediatric care with AI!

---

If you need further assistance or have specific questions about the project, feel free to ask! 
