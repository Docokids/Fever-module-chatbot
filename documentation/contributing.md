---
layout: default
title: Contributing
nav_order: 5
---

# Contributing to Docokids

Thank you for your interest in contributing to the Docokids project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing.

## How to Contribute

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/Fever-module-chatbot.git
   cd Fever-module-chatbot
   ```

### 2. Set Up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### 3. Create a Branch

Create a feature branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

1. Make your changes following our coding standards
2. Write or update tests as needed
3. Update documentation if necessary

### 5. Run Tests

```bash
pytest
flake8
mypy .
black . --check
```

### 6. Commit Changes

Follow our commit message format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Maintenance tasks

### 7. Push and Create Pull Request

1. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Include integration tests for API endpoints
- Test edge cases and error conditions

### Documentation

- Update README.md if needed
- Add or update API documentation
- Include docstrings for new functions
- Update CHANGELOG.md for significant changes

## Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Code coverage must not decrease
4. Documentation must be updated
5. Tests must be included

## Getting Help

- Open an issue for bugs or feature requests
- Join our community chat
- Contact the maintainers at agomez@docokids.com

## License

By contributing, you agree that your contributions will be licensed under the project's GNU GPL v3.0 License. 