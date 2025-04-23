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

---

## 🏁 Getting Started

Follow these steps to run the project locally:

### Installation

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

---

## 🚀 Usage

### Launch the API

```sh
uvicorn src.main:app --reload
```

This will expose the interactive documentation at **http://localhost:8000/docs**.

### API Endpoints

| Method | Route                                 | Description                                 |
|--------|---------------------------------------|---------------------------------------------|
| POST   | `/conversations`                      | Initiates a new conversation                |
| POST   | `/conversations/{id}/messages`        | Sends a user message and receives model response |
| GET    | `/conversations/{id}/history`         | Retrieves full conversation history         |
| GET    | `/providers`                          | Lists available LLM providers               |
| POST   | `/providers/{name}/select`            | Selects a provider for the conversation     |
| GET    | `/health`                             | API health status                           |

Example request:

```sh
curl -X POST http://localhost:8000/conversations \
  -H "Content-Type: application/json"
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
