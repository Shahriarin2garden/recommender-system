"""FastAPI main application entry point for E-commerce Recommender System."""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import logging
import os

from app.routes import products, recommend, auth, ab_test
from app.database import engine, Base

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Recommender API",
    description="Production-grade recommendation system with hybrid ML models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow localhost dev + any Vercel deployment + custom domain via env var
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    ALLOWED_ORIGINS.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "timestamp": time.time()}

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "E-commerce Recommender API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

app.include_router(products.router, prefix="/api/v1", tags=["Products"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendations"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(ab_test.router, prefix="/api/v1/ab-test", tags=["A/B Testing"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting E-commerce Recommender API...")
    _auto_seed_and_train()
    logger.info("API ready to accept requests")

def _auto_seed_and_train():
    """Seed DB and train ML model if not already done."""
    try:
        from app.database import SessionLocal
        from app.models import User, Product
        db = SessionLocal()
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        db.close()

        if user_count == 0 or product_count == 0:
            logger.info("Empty database detected — running seed...")
            import subprocess, sys
            seed_path = os.path.join(os.path.dirname(__file__), '..', 'seed_data.py')
            subprocess.run([sys.executable, seed_path], check=True)
            logger.info("Seed complete.")

        # Train ML model if artifacts missing
        ml_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'ml')
        model_path = os.path.join(ml_dir, 'model.pkl')
        if not os.path.exists(model_path):
            logger.info("ML model not found — training...")
            import subprocess, sys
            train_path = os.path.join(os.path.dirname(__file__), '..', 'train_model.py')
            subprocess.run([sys.executable, train_path], check=True)
            logger.info("Training complete.")
    except Exception as e:
        logger.warning(f"Startup seed/train skipped: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
