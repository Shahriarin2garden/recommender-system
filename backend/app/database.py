"""
Database configuration and session management.
Handles PostgreSQL connection pooling and SQLAlchemy setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator

# Database URL from environment variable
# Use SQLite for local dev, PostgreSQL for production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./recommender.db"  # Local SQLite file
)

# Create SQLAlchemy engine
# Different config for SQLite vs PostgreSQL
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite specific
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False  # Set to True for SQL query logging
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    
    Usage in FastAPI endpoints:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis connection setup
import redis
from typing import Optional

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client: Optional[redis.Redis] = None

def get_redis() -> redis.Redis:
    """
    Get Redis client instance.
    Creates connection pool on first call.
    """
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True,
            max_connections=50
        )
    return redis_client

def cache_get(key: str) -> Optional[str]:
    """Get value from Redis cache."""
    try:
        client = get_redis()
        return client.get(key)
    except Exception as e:
        print(f"Redis GET error: {e}")
        return None

def cache_set(key: str, value: str, ttl: int = 300) -> bool:
    """
    Set value in Redis cache with TTL.
    Default TTL is 5 minutes (300 seconds).
    """
    try:
        client = get_redis()
        return client.setex(key, ttl, value)
    except Exception as e:
        print(f"Redis SET error: {e}")
        return False

def cache_delete(key: str) -> bool:
    """Delete key from Redis cache."""
    try:
        client = get_redis()
        return client.delete(key) > 0
    except Exception as e:
        print(f"Redis DELETE error: {e}")
        return False
