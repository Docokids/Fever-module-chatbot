---
layout: default
title: Testing Guide
nav_order: 7
---

# Testing Guide

**Note: The chatbot is designed to handle conversations in Spanish and all API responses are in Spanish by default.**

## Overview

This guide provides comprehensive information about testing in the Fever Model project. We use pytest with async support through pytest-asyncio for our test suite.

## Test Structure

```
tests/
├── test_config.py      # Configuration tests
├── test_conversations.py # API endpoint tests
├── test_repositories.py # Database repository tests
└── test_services.py    # Business logic tests
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run specific test function
pytest tests/test_config.py::test_default_settings -v

# Run with coverage report
pytest --cov=src tests/
```

### Test Configuration

The project uses `pytest.ini` for test configuration:

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v
asyncio_mode = strict
asyncio_default_fixture_loop_scope = function
```

## Writing Tests

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

### Fixtures

```python
@pytest.fixture
def mock_session():
    return MockSession()
```

### Mocking

```python
def test_with_mock(monkeypatch):
    def mock_function():
        return "mocked"
    monkeypatch.setattr(SomeClass, "method", mock_function)
```

## Test Categories

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Located in respective test files

### Integration Tests
- Test component interactions
- May use test database
- Located in `test_services.py`

### API Tests
- Test HTTP endpoints
- Use FastAPI TestClient
- Located in `test_conversations.py`

## Best Practices

### Test Naming
- Use descriptive names: `test_<functionality>_<scenario>`
- Example: `test_handle_message_with_valid_input`

### Test Organization
- One assertion per test when possible
- Group related tests in classes
- Use fixtures for common setup

### Test Coverage
- Aim for high test coverage
- Focus on critical paths
- Test edge cases and error conditions

### Test Database
- Use separate test database
- Clean up after tests
- Use transactions when possible

## Common Test Patterns

### Testing Async Code
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### Testing API Endpoints
```python
def test_api_endpoint(client):
    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.json() == expected_data
```

### Testing with Mocks
```python
def test_with_mock(monkeypatch):
    def mock_function():
        return "mocked"
    monkeypatch.setattr(module, "function", mock_function)
```

### Testing Database Operations
```python
@pytest.mark.asyncio
async def test_db_operation(session):
    result = await session.execute(query)
    assert result.scalar() == expected
```

## Troubleshooting

### Common Issues
- Async test failures: Check `@pytest.mark.asyncio` decorator
- Database connection issues: Verify test database configuration
- Mock failures: Check fixture scope and patching

### Debugging Tests
- Use `pytest -v` for verbose output
- Use `pytest --pdb` for post-mortem debugging
- Use `pytest -s` to see print statements

### Test Environment
- Ensure test environment variables are set
- Check database migrations are up to date
- Verify all dependencies are installed 

---

## CI/CD y Cobertura

- El workflow de GitHub Actions ejecuta **solo los tests** y exige una **cobertura mínima del 40%**.
- Si la cobertura baja de ese umbral o algún test falla, el PR será rechazado automáticamente.
- Para ejecutar los tests y ver la cobertura localmente:

```sh
pytest --cov=src --cov-report=term-missing -v
```

- Para ver un reporte HTML navegable:

```sh
pytest --cov=src --cov-report=html
# Luego abre htmlcov/index.html en tu navegador
```

### Tests deshabilitados
- Los tests de `tests/test_adapters.py` y `tests/test_repositories.py` están deshabilitados temporalmente. Se recomienda reactivarlos y corregirlos en el futuro para mejorar la cobertura y robustez del proyecto. 