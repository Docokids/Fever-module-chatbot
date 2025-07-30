---
layout: default
title: Getting Started
parent: User Guide
nav_order: 1
---

# Getting Started

This guide will help you set up and run the **Fever Model** of **Docokids** locally. **The chatbot and API are designed to handle conversations in Spanish. All responses will be in Spanish by default.** The model has completed the **Exploratory Data Analysis (EDA)** phase and is currently progressing through **Feature Engineering** and **Model Fine-tuning**.

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (recommended)
- Git

## Installation

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/alejo14171/Fever-module-chatbot.git
   cd Fever-module-chatbot
   ```

2. Create a `.env` file in the root directory with your configuration:
   ```env
   APP_NAME=DocoChat
   LLM_PROVIDER=gemini  # or openai
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   REDIS_URL=redis://redis:6379/0
   POSTGRES_URL=postgresql+asyncpg://postgres:postgres@db:5432/docochat
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This will start:
   - FastAPI application on http://localhost:8000
   - PostgreSQL database
   - Redis cache

4. Access the interactive API documentation at http://localhost:8000/docs

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alejo14171/Fever-module-chatbot.git
   cd Fever-module-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration (see above)

5. Start the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Usage

### Basic Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/conversations` | Lists all conversations with message count and last message timestamp |
| POST | `/conversations` | Initiates a new conversation |
| POST | `/conversations/{id}/messages` | Sends a user message and receives model response |
| GET | `/conversations/{id}/history` | Retrieves full conversation history |

### Example Requests

```bash
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

*Note: The API responses are in Spanish by default, as the target audience is Spanish-speaking caregivers. You can adapt the prompts for other languages if needed.*

## Testing

The project uses pytest for testing with async support through pytest-asyncio. For detailed testing documentation, see [Testing Guide](testing.md).

### Quick Start

1. Install test dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Run tests:
   ```sh
   # Run all tests
   pytest tests/ -v

   # Run with coverage
   pytest --cov=src tests/
   ```

### Test Structure

```
tests/
├── test_config.py      # Configuration tests
├── test_conversations.py # API endpoint tests
├── test_repositories.py # Database repository tests
└── test_services.py    # Business logic tests
```

### Key Features

- Async test support with pytest-asyncio
- FastAPI TestClient for API testing
- Database transaction management
- Mock support for external dependencies
- Coverage reporting

For more information about testing, including best practices, patterns, and troubleshooting, see the [Testing Guide](testing.md).

## Troubleshooting

### Common Issues

#### Docker Issues
- **Container fails to start**: Ensure ports 8000, 5432, and 6379 are not in use
- **Database connection errors**: Check if PostgreSQL container is running and accessible
- **Redis connection errors**: Verify Redis container status and connection string

#### Environment Setup
- **Module not found errors**: Ensure you're in the virtual environment and all dependencies are installed
- **API key issues**: Verify your API keys are correctly set in the .env file
- **Permission errors**: Check file permissions for the .env file and project directory

#### API Issues
- **Connection refused**: Verify the API is running and the port is correct
- **Authentication errors**: Check your JWT token and ensure it's not expired
- **Rate limiting**: Monitor your request frequency and adjust accordingly

### Getting Help

If you encounter any issues not covered here:
1. Check the [GitHub Issues](https://github.com/alejo14171/Fever-module-chatbot/issues)
2. Search for similar problems in the [Discussions](https://github.com/alejo14171/Fever-module-chatbot/discussions)
3. Open a new issue with:
   - Detailed error message
   - Steps to reproduce
   - Environment information
   - Expected vs actual behavior

## Next Steps

- Check out the [API Reference](api-reference.md) for detailed endpoint documentation
- Read about [Contributing](contributing.md) to the project
- Join our community for support and updates 