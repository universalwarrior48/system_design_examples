"""
Payment Service - Handles payment processing and transactions.
"""
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from shared.common.logging import setup_logging, get_logger
from shared.common.config import settings
from services.payment_service.database.session import engine, Base
from services.payment_service.routers.payments import router as payments_router

# Setup logging
setup_logging(service_name="payment-service", debug=settings.debug)
logger = get_logger("payment-service")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Payment Service",
    description="Handles payment processing and transactions",
    version="1.0.0"
)

# Include routers
app.include_router(payments_router)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Log service startup."""
    logger.info("Payment Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Log service shutdown."""
    logger.info("Payment Service shutting down")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "payment-service"}
