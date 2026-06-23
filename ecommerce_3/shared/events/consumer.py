"""
RabbitMQ Event Consumer for inter-service communication.
"""
import aio_pika
import json
from typing import Callable, Awaitable
from shared.common.logging import get_logger
from shared.common.config import settings

logger = get_logger("event-consumer")


class EventConsumer:
    """Consumes events from RabbitMQ queues."""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queues = {}
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
            self.channel = await self.connection.channel()
            logger.info("Event consumer connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def subscribe(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
        callback: Callable[[dict], Awaitable[None]]
    ) -> None:
        """Subscribe to an event type with a callback handler."""
        if not self.channel:
            logger.warning("RabbitMQ not connected, cannot subscribe")
            return
        
        # Declare exchange
        exchange = await self.channel.declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        
        # Declare queue with dead letter exchange
        dlx_exchange = await self.channel.declare_exchange(
            "dead_letter_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True
        )
        
        queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": "dead_letter_exchange",
                "x-dead-letter-routing-key": "dead_letter_queue"
            }
        )
        
        # Bind queue to exchange
        await queue.bind(exchange, routing_key=routing_key)
        
        self.queues[queue_name] = queue
        logger.info(f"Subscribed to {exchange_name} with routing key {routing_key}")
        
        # Start consuming
        await queue.consume(self._make_callback(callback))
    
    def _make_callback(self, callback: Callable[[dict], Awaitable[None]]) -> Callable:
        """Wrap user callback with error handling."""
        async def wrapper(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    body = json.loads(message.body.decode())
                    await callback(body)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    raise  # Re-raise to trigger retry/dead letter
        return wrapper
    
    async def close(self) -> None:
        """Close RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            logger.info("Event consumer connection closed")


# Global consumer instance
consumer = EventConsumer()
