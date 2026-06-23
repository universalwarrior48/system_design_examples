# E-Commerce System - Phase 5: Monitoring & Observability

This folder contains the Phase 5 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Add Prometheus for metrics collection and Grafana for visualization

## New Components

### Prometheus (Metrics Collection)
- Time-series database for metrics
- Service discovery
- Alerting rules
- Query language (PromQL)

### Grafana (Visualization)
- Dashboards for monitoring
- Alerts and notifications
- Multiple data source support
- Custom panels and visualizations

## Technology Stack

### Backend
- FastAPI (Python) with Prometheus client
- SQLAlchemy
- Pydantic
- PostgreSQL

### Infrastructure
- **Redis**: Caching and session storage
- **RabbitMQ**: Message broker
- **Nginx**: API Gateway and Load Balancer
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- PostgreSQL

## Project Structure

```
ecommerce_5/
├── gateway/
│   └── nginx.conf
├── services/
│   ├── user_service/
│   │   ├── app/
│   │   │   └── main.py      # Prometheus metrics added
│   │   └── ...
│   ├── inventory_service/
│   ├── order_service/
│   └── payment_service/
├── shared/
│   ├── common/
│   ├── events/
│   └── auth/
├── infra/
│   ├── redis/
│   ├── rabbitmq/
│   ├── postgres/
│   ├── prometheus/          # NEW: Prometheus configuration
│   │   └── prometheus.yml
│   └── grafana/             # NEW: Grafana dashboards
│       └── dashboards/
└── tests/
```

## Key Changes from Phase 4

1. **Prometheus Integration**:
   - Metrics endpoints in each service (`/metrics`)
   - Custom business metrics (orders per minute, revenue, etc.)
   - Standard metrics (request count, latency, errors)
   - Service discovery configuration

2. **Grafana Dashboards**:
   - System overview dashboard
   - Service-specific dashboards
   - Business metrics dashboard
   - Alert configurations

3. **Instrumentation**:
   - Request/response timing
   - Database query metrics
   - Cache hit/miss rates
   - Queue depth monitoring
   - Error rates and types

## Getting Started

1. Start monitoring stack:
   ```bash
   cd infra
   docker-compose up -d prometheus grafana
   ```

2. Access Grafana:
   ```
   http://localhost:3000
   Username: admin
   Password: admin
   ```

3. Access Prometheus:
   ```
   http://localhost:9090
   ```

## Learning Objectives

- Metrics collection and aggregation
- PromQL query language
- Dashboard design principles
- Alerting strategies
- SLI/SLO/SLA concepts
- Golden signals monitoring
- Distributed tracing basics
- Log aggregation patterns

## Key Metrics Tracked

### Application Metrics
- Request rate (requests/second)
- Request latency (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Active connections

### Business Metrics
- Orders per minute
- Revenue per hour
- Cart abandonment rate
- User registration rate

### Infrastructure Metrics
- CPU usage per service
- Memory consumption
- Database connection pool usage
- Cache hit ratio
- Queue depth

## Sample PromQL Queries

```promql
# Request rate per service
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Orders per minute
rate(orders_created_total[1m]) * 60
```

## Next Phase

Proceed to `ecommerce_6` to add Docker containerization and Docker Compose orchestration.
