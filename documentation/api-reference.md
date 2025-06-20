---
layout: default
title: API Reference
nav_order: 4
---

# API Reference

This document provides detailed information about the **Fever Model** of **Docokids** API endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints

### Conversations

#### Create New Conversation
```http
POST /conversations
```

Creates a new conversation and returns its ID.

**Response**
```json
{
  "id": "uuid-string",
  "messages": []
}
```

**Status Code**: `201 Created`

#### Send Message
```http
POST /conversations/{conv_id}/messages
```

Sends a user message and receives an AI response from the pediatric chatbot.

**Request Body**
```json
{
  "role": "user",
  "content": "¿Cuál es la edad del niño?"
}
```

**Response**
```json
{
  "id": "uuid-string",
  "role": "assistant",
  "content": "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?",
  "timestamp": "2024-03-20T12:00:00Z"
}
```

**Status Code**: `200 OK`

**Error Responses**:
- `404 Not Found`: Conversation not found
- `400 Bad Request`: Invalid message format

#### Get Conversation History
```http
GET /conversations/{conv_id}/history
```

Retrieves the full conversation history with all messages.

**Response**
```json
{
  "id": "uuid-string",
  "messages": [
    {
      "id": "uuid-string",
      "role": "user",
      "content": "¿Cuál es la edad del niño?",
      "timestamp": "2024-03-20T12:00:00Z"
    },
    {
      "id": "uuid-string",
      "role": "assistant", 
      "content": "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?",
      "timestamp": "2024-03-20T12:00:01Z"
    }
  ]
}
```

**Status Code**: `200 OK`

**Error Responses**:
- `404 Not Found`: Conversation not found

#### List All Conversations
```http
GET /conversations/
```

Lists all conversations with summary information.

**Response**
```json
[
  {
    "id": "uuid-string",
    "message_count": 4,
    "last_message_timestamp": "2024-03-20T12:00:00Z"
  },
  {
    "id": "uuid-string",
    "message_count": 2,
    "last_message_timestamp": "2024-03-20T11:30:00Z"
  }
]
```

**Status Code**: `200 OK`

### Health Check

#### Check API Health
```http
GET /health
```

Checks the health status of the API and its dependencies.

**Response**
```json
{
  "status": "ok"
}
```

**Status Code**: `200 OK`

## Data Models

### MessageCreate
```json
{
  "role": "user",
  "content": "string"
}
```

### MessageResponse
```json
{
  "id": "uuid-string",
  "role": "assistant",
  "content": "string",
  "timestamp": "datetime-string"
}
```

### ConversationResponse
```json
{
  "id": "uuid-string",
  "messages": [
    {
      "id": "uuid-string",
      "role": "string",
      "content": "string",
      "timestamp": "datetime-string"
    }
  ]
}
```

### ConversationListItem
```json
{
  "id": "uuid-string",
  "message_count": 0,
  "last_message_timestamp": "datetime-string"
}
```

## Error Responses

The API uses standard HTTP status codes and returns error messages in the following format:

```json
{
  "detail": "Error message description"
}
```

### Error Codes

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | Invalid input data or request format |
| `404 Not Found` | Resource not found (conversation, etc.) |
| `500 Internal Server Error` | Server error |

### Example Error Responses

#### Not Found Error
```json
{
  "detail": "Conversación no encontrada"
}
```

#### Validation Error
```json
{
  "detail": "Invalid message format"
}
```

## Example Usage

### Complete Conversation Flow

1. **Create a new conversation**:
```bash
curl -X POST "http://localhost:8000/conversations"
```

2. **Send first message**:
```bash
curl -X POST "http://localhost:8000/conversations/{conversation_id}/messages" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "Mi hijo tiene fiebre"}'
```

3. **Continue conversation**:
```bash
curl -X POST "http://localhost:8000/conversations/{conversation_id}/messages" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "1 año"}'
```

4. **Get conversation history**:
```bash
curl -X GET "http://localhost:8000/conversations/{conversation_id}/history"
```

5. **List all conversations**:
```bash
curl -X GET "http://localhost:8000/conversations"
```

## Prompt Engineering Integration

The API integrates with the advanced prompt engineering system that:

- **Simulates Real Pediatric Consultations**: The AI behaves like an experienced pediatrician
- **Structured Conversation Phases**: 
  - INITIAL: Asks for child's age
  - DISCOVERY: Explores symptoms one question at a time
  - ASSESSMENT: Detailed evaluation
  - GUIDANCE: Educational recommendations
- **Safety Monitoring**: Automatically detects emergency symptoms
- **Context Awareness**: Adapts questions based on information already provided

For detailed information about the prompt engineering system, see [Prompt Engineering Guide](prompt-engineering.md).

## Rate Limiting

Currently, there are no rate limits implemented. However, it's recommended to:

- Wait at least 1 second between requests
- Handle responses appropriately before sending new messages
- Respect the conversation flow for optimal AI responses

## CORS

The API supports CORS with the following configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## OpenAPI Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive testing capabilities and detailed schema information. 