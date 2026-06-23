"""
Event definitions for inter-service communication.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    ORDER_CREATED = "order.created"
    PAYMENT_COMPLETED = "payment.completed"
    PAYMENT_FAILED = "payment.failed"
    INVENTORY_RESERVED = "inventory.reserved"
    INVENTORY_RELEASED = "inventory.released"
    ORDER_CONFIRMED = "order.confirmed"
    ORDER_CANCELLED = "order.cancelled"


class Event(BaseModel):
    """Base event structure."""
    event_type: EventType
    order_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Optional[dict] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OrderCreatedEvent(Event):
    """Event published when an order is created."""
    event_type: EventType = EventType.ORDER_CREATED
    user_id: str
    total_price: float
    items: list


class PaymentCompletedEvent(Event):
    """Event published when payment is completed."""
    event_type: EventType = EventType.PAYMENT_COMPLETED
    payment_id: str
    amount: float
    transaction_id: str


class PaymentFailedEvent(Event):
    """Event published when payment fails."""
    event_type: EventType = EventType.PAYMENT_FAILED
    payment_id: str
    amount: float
    reason: str


class InventoryReservedEvent(Event):
    """Event published when inventory is reserved."""
    event_type: EventType = EventType.INVENTORY_RESERVED
    product_ids: list
    quantities: list


class InventoryReleasedEvent(Event):
    """Event published when inventory reservation is released."""
    event_type: EventType = EventType.INVENTORY_RELEASED
    product_ids: list
    quantities: list


class OrderConfirmedEvent(Event):
    """Event published when order is confirmed."""
    event_type: EventType = EventType.ORDER_CONFIRMED


class OrderCancelledEvent(Event):
    """Event published when order is cancelled."""
    event_type: EventType = EventType.ORDER_CANCELLED
    reason: str
