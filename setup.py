from setuptools import setup, find_packages

setup(
    name="fever-module-chatbot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.4.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=1.0.0",
        "sqlalchemy>=2.0.0",
        "asyncpg>=0.28.0",
        "redis>=5.0.0",
        "alembic>=1.12.0",
        "google-generativeai>=0.3.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "langchain-anthropic>=0.0.1",
        "langchain-core>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ]
    }
) 