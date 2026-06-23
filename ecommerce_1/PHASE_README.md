# E-Commerce System - Phase 1: Monolith

This folder contains the Phase 1 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Build a monolithic application with Frontend + FastAPI + PostgreSQL

## Features Included

- User Registration/Login
- Product Catalog
- Inventory Management
- Shopping Cart
- Checkout
- Payment Processing
- Order Management

## Technology Stack

### Backend
- FastAPI (Python)
- SQLAlchemy
- Pydantic
- PostgreSQL

### Frontend
- HTML/CSS/JavaScript (Option A - Simpler)
- OR React + Vite (Option B - Modern)

## Project Structure

```
ecommerce_1/
├── frontend/           # React/Vite or HTML/CSS/JS frontend
├── services/           # All services in monolith
│   ├── user_service/
│   ├── inventory_service/
│   ├── order_service/
│   └── payment_service/
├── shared/             # Shared code
│   ├── common/         # Common utilities
│   ├── events/         # Event definitions
│   └── auth/           # Authentication middleware
└── tests/              # Test files
```

## Getting Started

1. Install dependencies:
   ```bash
   cd services
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database

3. Run the application:
   ```bash
   cd services/user_service/app
   uvicorn main:app --reload
   ```

## Learning Objectives

- Understand basic CRUD operations
- Learn FastAPI fundamentals
- Database modeling with SQLAlchemy
- API design principles
- Request/Response handling with Pydantic

## Next Phase

Proceed to `ecommerce_2` to split the monolith into microservices.
