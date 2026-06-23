"""
RabbitMQ Event Publisher for inter-service communication.
"""
import aio_pika
import json
from typing import Any, Dict
from datetime import datetime
from shared.events.models import Event, EventType
from shared.common.logging import get_logger
from shared.common.config import settings

logger = get_logger("event-publisher")


class EventPublisher:
    """Publishes events to RabbitMQ exchanges."""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchanges = {}
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
            self.channel = await self.connection.channel()
            
            # Declare exchanges for different event types
            await self._declare_exchange("order_events")
            await self._declare_exchange("payment_events")
            await self._declare_exchange("inventory_events")
            
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def _declare_exchange(self, exchange_name: str) -> None:
        """Declare a topic exchange."""
        exchange = await self.channel.declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        self.exchanges[exchange_name] = exchange
        logger.info(f"Declared exchange: {exchange_name}")
    
    async def publish(self, event: Event, routing_key: str) -> None:
        """Publish an event to the appropriate exchange."""
        if not self.channel:
            logger.warning("RabbitMQ not connected, skipping event publish")
            return
        
        exchange_name = self._get_exchange_for_event(event.event_type)
        if exchange_name not in self.exchanges:
            logger.error(f"Exchange {exchange_name} not found")
            return
        
        exchange = self.exchanges[exchange_name]
        
        message_body = json.dumps({
            "event_type": event.event_type.value,
            "order_id": str(event.order_id),
            "timestamp": event.timestamp.isoformat(),
            "data": event.dict(exclude={"event_type", "order_id", "timestamp"})
        }).encode()
        
        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            timestamp=datetime.utcnow()
        )
        
        try:
            await exchange.publish(message, routing_key=routing_key)
            logger.info(f"Published event {event.event_type.value} with routing key {routing_key}")
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
    
    def _get_exchange_for_event(self, event_type: EventType) -> str:
        """Determine which exchange to use based on event type."""
        if event_type in [EventType.ORDER_CREATED, EventType.ORDER_CONFIRMED, EventType.ORDER_CANCELLED]:
            return "order_events"
        elif event_type in [EventType.PAYMENT_COMPLETED, EventType.PAYMENT_FAILED]:
            return "payment_events"
        elif event_type in [EventType.INVENTORY_RESERVED, EventType.INVENTORY_RELEASED]:
            return "inventory_events"
        return "order_events"
    
    async def close(self) -> None:
        """Close RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")


# Global publisher instance
publisher = EventPublisher()
