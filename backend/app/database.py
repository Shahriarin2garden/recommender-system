"""
Database configuration and session management.
Handles PostgreSQL connection pooling and SQLAlchemy setup.
"""

import logging
import os
from typing import Generator, Optional

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)


def _normalize_database_url(raw_url: Optional[str]) -> str:
    if not raw_url:
        return "sqlite:///./recommender.db"

    normalized = raw_url.strip()
    if normalized.startswith("postgres://"):
        normalized = normalized.replace("postgres://", "postgresql://", 1)
    return normalized


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL"))

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """Yield a DB session and close it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


REDIS_URL = os.getenv("REDIS_URL", "").strip()
redis_client: Optional[redis.Redis] = None
memory_cache = {}
_redis_warning_sent = False


def get_redis() -> Optional[redis.Redis]:
    """Return a Redis client when configured, otherwise fall back to memory."""
    global redis_client, _redis_warning_sent

    if not REDIS_URL:
        if not _redis_warning_sent:
            logger.warning("REDIS_URL is empty; using in-memory cache fallback.")
            _redis_warning_sent = True
        return None

    if redis_client is not None:
        return redis_client

    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True, max_connections=50)
        redis_client.ping()
        return redis_client
    except Exception as exc:  # pragma: no cover - depends on Redis availability
        if not _redis_warning_sent:
            logger.warning("Redis unavailable; using in-memory cache fallback: %s", exc)
            _redis_warning_sent = True
        return None


def get_redis_status() -> str:
    if not REDIS_URL:
        return "disabled"

    client = get_redis()
    if client is None:
        return "unavailable"

    try:
        client.ping()
        return "ok"
    except Exception:
        return "unavailable"


def cache_get(key: str) -> Optional[str]:
    """Get a value from Redis or memory cache."""
    client = get_redis()
    if client is not None:
        try:
            return client.get(key)
        except Exception as exc:  # pragma: no cover - depends on Redis availability
            logger.warning("Redis GET error: %s", exc)
    return memory_cache.get(key)


def cache_set(key: str, value: str, ttl: int = 300) -> bool:
    """Set a value in Redis or memory cache with TTL."""
    client = get_redis()
    if client is not None:
        try:
            return bool(client.setex(key, ttl, value))
        except Exception as exc:  # pragma: no cover - depends on Redis availability
            logger.warning("Redis SET error: %s", exc)
    memory_cache[key] = value
    return True


def cache_delete(key: str) -> bool:
    """Delete a value from Redis or memory cache."""
    client = get_redis()
    if client is not None:
        try:
            return bool(client.delete(key))
        except Exception as exc:  # pragma: no cover - depends on Redis availability
            logger.warning("Redis DELETE error: %s", exc)
    if key in memory_cache:
        del memory_cache[key]
        return True
    return False
