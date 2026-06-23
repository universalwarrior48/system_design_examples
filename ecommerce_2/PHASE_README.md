# E-Commerce System - Phase 2: Microservices

This folder contains the Phase 2 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Split the monolith into separate microservices

## Services

- **User Service**: User registration, login, authentication
- **Inventory Service**: Product catalog, inventory management
- **Order Service**: Order creation, management, status tracking
- **Payment Service**: Payment processing (basic implementation)

## Technology Stack

### Backend (Each Service)
- FastAPI (Python)
- SQLAlchemy
- Pydantic
- PostgreSQL (separate database per service)

## Project Structure

```
ecommerce_2/
├── services/           # All microservices (separate folders)
│   ├── user_service/
│   │   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── database/
│   ├── inventory_service/
│   │   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── database/
│   ├── order_service/
│   │   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── database/
│   └── payment_service/
├── shared/             # Shared code between services
│   ├── common/         # Common utilities
│   ├── events/         # Event definitions
│   └── auth/           # Authentication middleware
└── tests/              # Test files
```

## Key Changes from Phase 1

1. **Service Separation**: Each service is now independent
2. **Database Per Service**: Each microservice has its own database
3. **Independent Deployment**: Services can be deployed separately
4. **API Contracts**: Clear interfaces between services

## Getting Started

1. Install dependencies for each service:
   ```bash
   cd services/user_service
   pip install -r requirements.txt
   
   cd ../inventory_service
   pip install -r requirements.txt
   
   cd ../order_service
   pip install -r requirements.txt
   ```

2. Set up separate PostgreSQL databases for each service

3. Run each service:
   ```bash
   # Terminal 1 - User Service
   cd services/user_service/app
   uvicorn main:app --reload --port 8001
   
   # Terminal 2 - Inventory Service
   cd services/inventory_service/app
   uvicorn main:app --reload --port 8002
   
   # Terminal 3 - Order Service
   cd services/order_service/app
   uvicorn main:app --reload --port 8003
   ```

## Learning Objectives

- Understand microservices architecture principles
- Learn service decomposition strategies
- Database-per-service pattern
- Inter-service communication basics
- API versioning and contracts
- Service discovery concepts

## Challenges Addressed

- Data consistency across services
- Service-to-service communication
- Distributed transactions
- Error handling in distributed systems

## Next Phase

Proceed to `ecommerce_3` to add Redis caching and RabbitMQ message queue.
