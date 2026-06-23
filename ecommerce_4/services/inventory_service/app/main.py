"""
Inventory Service - Handles product catalog and inventory management.
"""
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from shared.common.logging import setup_logging, get_logger
from shared.common.config import settings
from services.inventory_service.database.session import engine, Base
from services.inventory_service.routers.products import router as products_router

# Setup logging
setup_logging(service_name="inventory-service", debug=settings.debug)
logger = get_logger("inventory-service")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Inventory Service",
    description="Handles product catalog and inventory management",
    version="1.0.0"
)

# Include routers
app.include_router(products_router)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Log service startup."""
    logger.info("Inventory Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Log service shutdown."""
    logger.info("Inventory Service shutting down")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "inventory-service"}
