"""
Order service routers.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import uuid

from services.order_service.database.session import get_db
from services.order_service.models.order import Order, OrderItem, OrderStatus
from services.order_service.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderStatusUpdate,
    OrderItemResponse
)
from shared.common.logging import get_logger

logger = get_logger("order-service")

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    skip: int = 0,
    limit: int = 100,
    db: Annotated[Session, Depends(get_db)] = None
):
    """List all orders."""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Get a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Create a new order."""
    # Calculate total price
    total_price = sum(item.quantity * item.unit_price for item in order_data.items)
    
    # Create the order
    order = Order(
        user_id=order_data.user_id,
        total_price=total_price,
        shipping_address=order_data.shipping_address,
        status=OrderStatus.PENDING
    )
    
    db.add(order)
    db.flush()  # Get the order ID before committing
    
    # Create order items
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            product_name=item_data.product_name,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=item_data.quantity * item_data.unit_price
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    logger.info(f"Created order: {order.id} for user: {order.user_id}")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: uuid.UUID,
    order_data: OrderUpdate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Update an existing order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    # Update fields
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    logger.info(f"Updated order: {order.id}")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: uuid.UUID,
    status_update: OrderStatusUpdate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Update order status."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    logger.info(f"Updated order {order.id} status to: {order.status}")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Cancel an order (only if pending)."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status: {order.status}"
        )
    
    order.status = OrderStatus.CANCELLED
    db.commit()
    logger.info(f"Cancelled order: {order.id}")
    return None
