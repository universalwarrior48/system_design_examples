"""
Shared events module.
"""
from .models import (
    EventType,
    Event,
    OrderCreatedEvent,
    PaymentCompletedEvent,
    PaymentFailedEvent,
    InventoryReservedEvent,
    InventoryReleasedEvent,
    OrderConfirmedEvent,
    OrderCancelledEvent
)
from .publisher import EventPublisher, publisher
from .consumer import EventConsumer, consumer

__all__ = [
    "EventType",
    "Event",
    "OrderCreatedEvent",
    "PaymentCompletedEvent",
    "PaymentFailedEvent",
    "InventoryReservedEvent",
    "InventoryReleasedEvent",
    "OrderConfirmedEvent",
    "OrderCancelledEvent",
    "EventPublisher",
    "publisher",
    "EventConsumer",
    "consumer"
]
