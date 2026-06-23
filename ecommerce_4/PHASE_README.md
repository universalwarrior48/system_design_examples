# E-Commerce System - Phase 4: API Gateway & Load Balancer

This folder contains the Phase 4 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Add Nginx as API Gateway and Load Balancer

## New Components

### API Gateway (Nginx)
- Single entry point for all client requests
- Request routing to appropriate services
- Authentication and authorization
- Rate limiting
- Request/Response transformation
- SSL termination

### Load Balancer (Nginx)
- Distribute traffic across multiple service instances
- Health checks
- Sticky sessions (if needed)
- Circuit breaker pattern

## Technology Stack

### Backend
- FastAPI (Python)
- SQLAlchemy
- Pydantic
- PostgreSQL

### Infrastructure
- **Redis**: Caching and session storage
- **RabbitMQ**: Message broker
- **Nginx**: API Gateway and Load Balancer
- PostgreSQL

## Project Structure

```
ecommerce_4/
├── gateway/              # NEW: Nginx API Gateway configuration
│   └── nginx.conf
├── services/
│   ├── user_service/     # Multiple instances possible
│   │   ├── app/
│   │   └── ...
│   ├── inventory_service/
│   │   ├── app/
│   │   └── ...
│   ├── order_service/
│   │   ├── app/
│   │   └── ...
│   └── payment_service/
├── shared/
│   ├── common/
│   ├── events/
│   └── auth/
├── infra/
│   ├── redis/
│   ├── rabbitmq/
│   └── postgres/
└── tests/
```

## Key Changes from Phase 3

1. **API Gateway Implementation**:
   - Centralized routing configuration
   - Path-based routing (`/api/users/*` → User Service)
   - Header manipulation
   - CORS handling
   - Request logging

2. **Load Balancing**:
   - Round-robin distribution
   - Least connections algorithm
   - Health check endpoints
   - Automatic failover

3. **Security Enhancements**:
   - JWT token validation at gateway
   - Rate limiting per IP/user
   - DDoS protection basics
   - HTTPS/SSL termination

## Getting Started

1. Configure Nginx:
   ```bash
   cd gateway
   # Review nginx.conf for routing rules
   ```

2. Start Nginx:
   ```bash
   # Using Docker
   docker run -d -p 80:80 -v $(pwd)/gateway/nginx.conf:/etc/nginx/nginx.conf nginx
   
   # Or install locally
   sudo nginx
   ```

3. Access services through gateway:
   ```
   http://localhost/api/users/*
   http://localhost/api/products/*
   http://localhost/api/orders/*
   ```

## Learning Objectives

- API Gateway patterns and best practices
- Load balancing algorithms
- Reverse proxy configuration
- SSL/TLS termination
- Rate limiting strategies
- Centralized authentication
- Request/Response logging
- Microservices security

## Nginx Configuration Highlights

### Routing Rules
```nginx
location /api/users/ {
    proxy_pass http://user_service_upstream;
}

location /api/products/ {
    proxy_pass http://inventory_service_upstream;
}

location /api/orders/ {
    proxy_pass http://order_service_upstream;
}
```

### Load Balancing
```nginx
upstream user_service_upstream {
    server user_service_1:8001;
    server user_service_2:8001;
    server user_service_3:8001;
}
```

## Next Phase

Proceed to `ecommerce_5` to add Prometheus monitoring and Grafana dashboards.
