# E-Commerce System - Learning Path

This repository contains a complete 7-phase learning journey for building a production-ready E-Commerce microservices system.

## Quick Navigation

| Phase | Folder | Focus Area | Key Technologies |
|-------|--------|------------|------------------|
| **Phase 1** | `ecommerce_1/` | Monolith | FastAPI, PostgreSQL |
| **Phase 2** | `ecommerce_2/` | Microservices | Service decomposition |
| **Phase 3** | `ecommerce_3/` | Caching & Messaging | Redis, RabbitMQ |
| **Phase 4** | `ecommerce_4/` | Gateway & LB | Nginx |
| **Phase 5** | `ecommerce_5/` | Monitoring | Prometheus, Grafana |
| **Phase 6** | `ecommerce_6/` | Containerization | Docker, Docker Compose |
| **Phase 7** | `ecommerce_7/` | Orchestration | Kubernetes, HPA |

## How to Use This Repository

1. **Start with Phase 1** (`ecommerce_1/`) - Build the monolithic foundation
2. **Progress sequentially** through each phase
3. **Read the PHASE_README.md** in each folder for detailed instructions
4. **Compare implementations** between phases to understand evolution

## Learning Approach

Each phase builds upon the previous one, adding new components and architectural patterns:

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7
   │           │           │           │           │           │
   │           │           │           │           │           └─ Kubernetes
   │           │           │           │           └───────────── Monitoring
   │           │           │           └───────────────────────── Gateway/LB
   │           │           └───────────────────────────────────── Cache/Queue
   │           └───────────────────────────────────────────────── Microservices
   └───────────────────────────────────────────────────────────── Monolith
```

## Features Across All Phases

- User Registration/Login
- Product Catalog
- Inventory Management
- Shopping Cart
- Checkout
- Payment Processing
- Order Management

## Prerequisites

- Python 3.9+
- Basic understanding of REST APIs
- Familiarity with command line
- Docker (for Phase 6+)
- Kubernetes (for Phase 7, optional)

## Getting Started

Choose your starting point based on your experience level:

- **Beginner**: Start from `ecommerce_1/` (Phase 1)
- **Intermediate**: Start from `ecommerce_2/` or `ecommerce_3/`
- **Advanced**: Jump to `ecommerce_5/` or later for infrastructure topics

See the `PHASE_README.md` file in each phase folder for detailed setup instructions.
