"""FastAPI main application entry point for E-commerce Recommender System."""

import logging
import os
import time
from urllib.parse import urlparse

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.database import DATABASE_URL, Base, engine, get_redis_status
from app.routes import ab_test, auth, products, recommend

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ROOT_PATH = os.getenv("ROOT_PATH", "").strip().rstrip("/")


def _build_allowed_origins() -> list[str]:
    defaults = ["http://localhost:3000", "http://127.0.0.1:3000"]
    raw_values = [
        os.getenv("CORS_ORIGINS", ""),
        os.getenv("FRONTEND_URL", ""),
        os.getenv("PUBLIC_URL", ""),
    ] + defaults

    origins: list[str] = []
    for raw in raw_values:
        if not raw:
            continue
        for candidate in raw.split(","):
            value = candidate.strip()
            if value and value not in origins:
                origins.append(value)
    return origins


ALLOWED_ORIGINS = _build_allowed_origins()

app = FastAPI(
    title="E-commerce Recommender API",
    description="Production-grade recommendation system with hybrid ML models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path=ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/health", tags=["Health"])
async def health_check():
    db_status = "down"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:  # pragma: no cover - runtime dependency check
        logger.warning("Database health check failed: %s", exc)

    status_value = "healthy" if db_status == "ok" else "degraded"
    return {
        "status": status_value,
        "database": db_status,
        "redis": get_redis_status(),
        "version": "1.0.0",
        "timestamp": time.time(),
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "E-commerce Recommender API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(products.router, prefix="/api/v1", tags=["Products"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendations"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(ab_test.router, prefix="/api/v1/ab-test", tags=["A/B Testing"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting E-commerce Recommender API...")
    try:
        parsed = urlparse(DATABASE_URL)
        if parsed.scheme not in {"sqlite", "postgresql", "postgres"}:
            raise ValueError(f"Unsupported DATABASE_URL scheme: {parsed.scheme}")
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError(
            f"DATABASE_URL is invalid or unreachable: {DATABASE_URL}. Check the database service and environment settings."
        ) from exc

    Base.metadata.create_all(bind=engine)

    if os.getenv("ENVIRONMENT", "development").lower() == "production":
        if os.getenv("ALLOW_SEED", "").lower() == "true":
            _auto_seed_and_train()
    else:
        _auto_seed_and_train()

    logger.info("API ready to accept requests")


def _auto_seed_and_train():
    """Seed the database and model only when the environment allows it."""
    allow_seed = os.getenv("ALLOW_SEED", "").lower() == "true"
    environment = os.getenv("ENVIRONMENT", "development").lower()
    if environment == "production" and not allow_seed:
        logger.info("Production seeding is disabled. Set ALLOW_SEED=true to enable a demo database seed.")
        return

    try:
        from app.database import SessionLocal
        from app.models import Product, User

        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            product_count = db.query(Product).count()
        finally:
            db.close()

        if user_count == 0 or product_count == 0:
            logger.info("Empty database detected. Running seed...")
            import subprocess
            import sys

            seed_path = os.path.join(os.path.dirname(__file__), "..", "seed_data.py")
            subprocess.run([sys.executable, seed_path], check=True)
            logger.info("Seed complete.")
    except Exception as exc:
        logger.warning("Startup seed skipped: %s", exc)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
