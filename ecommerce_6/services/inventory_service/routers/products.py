"""
Inventory service routers.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import uuid

from services.inventory_service.database.session import get_db
from services.inventory_service.models.product import Product, InventoryEvent
from services.inventory_service.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    InventoryAdjustment
)
from shared.common.logging import get_logger

logger = get_logger("inventory-service")

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Annotated[Session, Depends(get_db)] = None
):
    """List all products."""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Get a specific product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Create a new product."""
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info(f"Created product: {product.id}")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Update an existing product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Update fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    logger.info(f"Updated product: {product.id}")
    return product


@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def adjust_stock(
    product_id: uuid.UUID,
    adjustment: InventoryAdjustment,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Adjust product stock (for sales, restocks, returns)."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Check if adjustment would result in negative quantity
    new_quantity = product.quantity + adjustment.change
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product.quantity}, Requested change: {adjustment.change}"
        )
    
    # Update quantity
    product.quantity = new_quantity
    
    # Record the inventory event
    event = InventoryEvent(
        product_id=product.id,
        change=adjustment.change,
        reason=adjustment.reason
    )
    db.add(event)
    db.commit()
    db.refresh(product)
    
    logger.info(f"Adjusted stock for product {product.id}: {adjustment.change} ({adjustment.reason})")
    return product
