import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_recommender.db")
os.environ.setdefault("JWT_SECRET", "test-secret-key-1234567890abcdef")
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    # Context manager runs the startup event (create_all + seed)
    with TestClient(app) as c:
        yield c
