"""
User Service - Handles user registration, login, and profile management.
"""
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from shared.common.logging import setup_logging, get_logger
from shared.common.config import settings
from services.user_service.database.session import engine, Base
from services.user_service.routers.users import router as users_router

# Setup logging
setup_logging(service_name="user-service", debug=settings.debug)
logger = get_logger("user-service")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="User Service",
    description="Handles user registration, login, and profile management",
    version="1.0.0"
)

# Include routers
app.include_router(users_router)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Log service startup."""
    logger.info("User Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Log service shutdown."""
    logger.info("User Service shutting down")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "user-service"}
