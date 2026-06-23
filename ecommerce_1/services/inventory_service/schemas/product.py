"""
Inventory schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProductBase(BaseModel):
    """Base schema for product."""
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InventoryAdjustment(BaseModel):
    """Schema for adjusting inventory."""
    change: int  # Positive for add, negative for remove
    reason: str  # e.g., "sale", "restock", "return"
