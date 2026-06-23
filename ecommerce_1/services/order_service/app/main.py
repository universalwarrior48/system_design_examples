"""
Order Service - Handles order management and checkout.
"""
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from shared.common.logging import setup_logging, get_logger
from shared.common.config import settings
from services.order_service.database.session import engine, Base
from services.order_service.routers.orders import router as orders_router

# Setup logging
setup_logging(service_name="order-service", debug=settings.debug)
logger = get_logger("order-service")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Order Service",
    description="Handles order management and checkout",
    version="1.0.0"
)

# Include routers
app.include_router(orders_router)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Log service startup."""
    logger.info("Order Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Log service shutdown."""
    logger.info("Order Service shutting down")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "order-service"}
