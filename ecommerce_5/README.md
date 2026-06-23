# E-Commerce System

A production-inspired E-Commerce System demonstrating microservices architecture, API Gateway, Load Balancer, caching, message queues, and observability.

## Features

- User Registration/Login
- Product Catalog
- Inventory Management
- Shopping Cart
- Checkout
- Payment Processing
- Order Management

## Technology Stack

### Frontend
- HTML/CSS/JavaScript (Option A - Simpler)
- React + Vite (Option B - Modern)

### Backend
- FastAPI (Python)
- SQLAlchemy
- Pydantic

### Infrastructure
| Component         | Technology |
| ----------------- | ---------- |
| API Gateway       | Nginx      |
| Load Balancer     | Nginx      |
| User Service      | FastAPI    |
| Inventory Service | FastAPI    |
| Order Service     | FastAPI    |
| Payment Service   | FastAPI    |
| Message Queue     | RabbitMQ   |
| Cache             | Redis      |
| Database          | PostgreSQL |
| Logging           | Structlog  |
| Metrics           | Prometheus |
| Visualization     | Grafana    |

## Project Structure

```
ecommerce/
├── frontend/           # React/Vite or HTML/CSS/JS frontend
├── gateway/            # Nginx API Gateway configuration
├── services/           # All microservices
│   ├── user_service/
│   ├── inventory_service/
│   ├── order_service/
│   └── payment_service/
├── shared/             # Shared code
│   ├── common/         # Common utilities
│   ├── events/         # Event definitions
│   └── auth/           # Authentication middleware
├── infra/              # Infrastructure configurations
│   ├── postgres/
│   ├── redis/
│   └── rabbitmq/
└── tests/              # Test files
```

## Build Phases

1. **Phase 1**: Monolith (Frontend + FastAPI + Postgres)
2. **Phase 2**: Split into microservices (UserService, InventoryService, OrderService)
3. **Phase 3**: Add Redis and RabbitMQ
4. **Phase 4**: Add API Gateway and Load Balancer
5. **Phase 5**: Add Prometheus and Grafana
6. **Phase 6**: Add Docker and Docker Compose
7. **Phase 7**: Add Kubernetes with HPA

## Getting Started

See individual phase documentation for setup instructions.
