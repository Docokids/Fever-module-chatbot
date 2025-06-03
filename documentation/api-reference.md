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

The API uses JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### Conversations

#### List Conversations
```http
GET /conversations
```

Returns a list of all conversations with message count and last message timestamp.

**Response**
```json
{
  "conversations": [
    {
      "id": "string",
      "message_count": 0,
      "last_message_at": "2024-03-20T12:00:00Z"
    }
  ]
}
```

#### Create Conversation
```http
POST /conversations
```

Initiates a new conversation.

**Response**
```json
{
  "id": "string",
  "created_at": "2024-03-20T12:00:00Z"
}
```

#### Send Message
```http
POST /conversations/{id}/messages
```

Sends a user message and receives model response.

**Request Body**
```json
{
  "role": "user",
  "content": "string"
}
```

**Response**
```json
{
  "id": "string",
  "role": "assistant",
  "content": "string",
  "created_at": "2024-03-20T12:00:00Z"
}
```

#### Get Conversation History
```http
GET /conversations/{id}/history
```

Retrieves the full conversation history.

**Response**
```json
{
  "messages": [
    {
      "id": "string",
      "role": "string",
      "content": "string",
      "created_at": "2024-03-20T12:00:00Z"
    }
  ]
}
```

### Health Check

#### Check API Health
```http
GET /health
```

Checks the health status of the API and its dependencies.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "dependencies": {
    "database": "connected",
    "redis": "connected",
    "llm_provider": "connected"
  }
}
```

## Error Responses

The API uses standard HTTP status codes and returns error messages in the following format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `AUTHENTICATION_ERROR` | 401 | Authentication failed |
| `AUTHORIZATION_ERROR` | 403 | Not authorized |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

### Example Error Responses

#### Not Found Error
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Conversation not found",
    "details": {
      "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
    }
  }
}
```

#### Validation Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid message format",
    "details": {
      "errors": [
        {
          "loc": ["body", "content"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
  }
}
```

#### Authentication Error
```json
{
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Invalid or expired token",
    "details": {
      "token_type": "Bearer"
    }
  }
}
```

#### Internal Server Error
```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred",
    "details": {
      "error": "Database connection failed"
    }
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage. Current limits:
- 100 requests per minute per IP
- 1000 requests per hour per API key

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1616248800
``` 