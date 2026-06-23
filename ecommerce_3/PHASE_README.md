# E-Commerce System - Phase 3: Caching & Message Queue

This folder contains the Phase 3 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Add Redis for caching and RabbitMQ for asynchronous messaging

## New Components

### Redis (Caching Layer)
- Cache frequently accessed data (products, user sessions)
- Reduce database load
- Improve response times

### RabbitMQ (Message Queue)
- Asynchronous communication between services
- Event-driven architecture
- Decouple services

## Technology Stack

### Backend
- FastAPI (Python)
- SQLAlchemy
- Pydantic
- PostgreSQL

### Infrastructure
- **Redis**: Caching and session storage
- **RabbitMQ**: Message broker for events

## Project Structure

```
ecommerce_3/
├── services/
│   ├── user_service/
│   ├── inventory_service/
│   ├── order_service/
│   └── payment_service/
├── shared/
│   ├── common/
│   ├── events/         # Event definitions for RabbitMQ
│   └── auth/
├── infra/              # NEW: Infrastructure configurations
│   ├── redis/          # Redis configuration
│   └── rabbitmq/       # RabbitMQ configuration
└── tests/
```

## Key Changes from Phase 2

1. **Redis Integration**:
   - Product catalog caching
   - User session storage
   - Cache invalidation strategies

2. **RabbitMQ Integration**:
   - Event publishing (OrderCreated, InventoryUpdated, PaymentProcessed)
   - Event consumers in respective services
   - Dead letter queues for failed messages

3. **Event-Driven Patterns**:
   - Publish/Subscribe pattern
   - Event sourcing basics
   - Async task processing

## Getting Started

1. Start infrastructure services:
   ```bash
   # Using Docker Compose (recommended)
   cd infra
   docker-compose up -d redis rabbitmq
   ```

2. Install additional dependencies:
   ```bash
   pip install redis aiormq
   ```

3. Run services with cache and queue enabled

## Learning Objectives

- Caching strategies (cache-aside, write-through, write-behind)
- Cache invalidation patterns
- Message queue fundamentals
- Publish/Subscribe pattern
- Event-driven architecture
- Handling eventual consistency
- Retry mechanisms and dead letter queues

## Use Cases Implemented

### Redis
- Cache product listings (TTL: 5 minutes)
- Cache user profiles (TTL: 15 minutes)
- Session management
- Rate limiting

### RabbitMQ
- OrderCreated → Inventory Service (reserve stock)
- OrderCreated → Payment Service (process payment)
- PaymentProcessed → Order Service (update order status)
- InventoryLow → Notification Service (send alerts)

## Next Phase

Proceed to `ecommerce_4` to add API Gateway and Load Balancer.
