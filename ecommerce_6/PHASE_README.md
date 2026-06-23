# E-Commerce System - Phase 6: Docker & Docker Compose

This folder contains the Phase 6 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Containerize all services with Docker and orchestrate with Docker Compose

## New Components

### Docker (Containerization)
- Dockerfile for each service
- Multi-stage builds for optimization
- Minimal base images (Alpine/Python slim)
- Layer caching strategies

### Docker Compose (Orchestration)
- Single command to start entire stack
- Service dependencies and health checks
- Network isolation
- Volume management for persistence

## Technology Stack

### Backend (Containerized)
- FastAPI (Python) in Docker containers
- SQLAlchemy
- Pydantic
- PostgreSQL

### Infrastructure (All Containerized)
- **Redis**: Caching
- **RabbitMQ**: Message broker
- **Nginx**: API Gateway and Load Balancer
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **PostgreSQL**: Database

## Project Structure

```
ecommerce_6/
├── gateway/
│   ├── nginx.conf
│   └── Dockerfile          # NEW
├── services/
│   ├── user_service/
│   │   ├── app/
│   │   ├── Dockerfile      # NEW
│   │   └── ...
│   ├── inventory_service/
│   │   ├── app/
│   │   ├── Dockerfile      # NEW
│   │   └── ...
│   ├── order_service/
│   │   ├── app/
│   │   ├── Dockerfile      # NEW
│   │   └── ...
│   └── payment_service/
│       ├── app/
│       ├── Dockerfile      # NEW
│       └── ...
├── shared/
│   ├── common/
│   ├── events/
│   └── auth/
├── infra/
│   ├── redis/
│   ├── rabbitmq/
│   ├── postgres/
│   ├── prometheus/
│   └── grafana/
├── docker-compose.yml      # NEW: Main orchestration file
├── docker-compose.dev.yml  # Development overrides
├── docker-compose.prod.yml # Production configuration
├── .dockerignore           # NEW: Docker ignore rules
└── tests/
```

## Key Changes from Phase 5

1. **Dockerfiles Created**:
   - Optimized multi-stage builds
   - Non-root user for security
   - Proper layer ordering for caching
   - Health check instructions

2. **Docker Compose Configuration**:
   - All services defined in single file
   - Network configuration
   - Volume mounts for development
   - Environment variable management
   - Service dependencies

3. **Build Optimization**:
   - Layer caching strategies
   - Minimal base images
   - Reduced image sizes
   - Faster build times

## Getting Started

1. Build all images:
   ```bash
   docker-compose build
   ```

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. View running containers:
   ```bash
   docker-compose ps
   ```

4. View logs:
   ```bash
   docker-compose logs -f
   ```

5. Stop all services:
   ```bash
   docker-compose down
   ```

## Learning Objectives

- Docker fundamentals and best practices
- Dockerfile optimization techniques
- Multi-stage builds
- Docker networking
- Volume management
- Docker Compose syntax and features
- Container health checks
- Environment configuration
- Build context optimization
- Security best practices

## Docker Commands Reference

```bash
# Build images
docker-compose build

# Build with no cache
docker-compose build --no-cache

# Start services
docker-compose up -d

# Start with rebuild
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]

# Execute command in container
docker-compose exec [service_name] bash

# Scale services
docker-compose up -d --scale user_service=3

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Sample Dockerfile (FastAPI Service)

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next Phase

Proceed to `ecommerce_7` to add Kubernetes deployment with Horizontal Pod Autoscaler (HPA).
