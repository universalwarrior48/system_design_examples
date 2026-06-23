"""
Order schemas for request/response validation.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class OrderStatusEnum(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemCreate(BaseModel):
    """Schema for creating an order item."""
    product_id: UUID
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    user_id: UUID
    items: List[OrderItemCreate]
    shipping_address: str


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: UUID
    user_id: UUID
    status: OrderStatusEnum
    total_price: float
    shipping_address: str
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    shipping_address: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatusEnum
