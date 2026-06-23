"""
Inventory database models.
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from services.inventory_service.database.session import Base


class Product(Base):
    """Product model."""
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"


class InventoryEvent(Base):
    """Inventory event tracking model."""
    __tablename__ = "inventory_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    change = Column(Integer, nullable=False)  # Positive for add, negative for remove
    reason = Column(String, nullable=False)  # e.g., "sale", "restock", "return"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<InventoryEvent(id={self.id}, product_id={self.product_id}, change={self.change})>"
