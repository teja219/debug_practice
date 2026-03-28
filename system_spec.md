# System Specification: OrderFlow — Distributed Order Processing System

## Overview
OrderFlow is a microservices-based e-commerce order processing system.
It handles order creation, inventory checks, payment processing, and fulfillment.

## Architecture

```
[Client] --> [API Gateway] --> [Order Service]
                                    |
                    +---------------+---------------+
                    |               |               |
            [Inventory Svc]  [Payment Svc]  [Notification Svc]
                    |               |
             [Inventory DB]  [Payment DB]
                    |
             [Order DB (shared read)]
```

## Services

### API Gateway
- Routes requests to Order Service
- Applies rate limiting: 100 requests/min per user
- Validates JWT tokens

### Order Service
- Creates orders, assigns unique order IDs
- Orchestrates calls to Inventory and Payment services
- On success: writes order to Order DB, triggers Notification
- On failure: rolls back and returns error

### Inventory Service
- Checks and reserves stock
- Uses optimistic locking to prevent oversell
- Exposes: `check_stock(item_id, qty)`, `reserve_stock(item_id, qty, order_id)`

### Payment Service
- Charges customer payment method
- Idempotency key = order_id
- Returns: `{status: "success"|"failed", transaction_id}`

### Notification Service
- Sends confirmation emails async via a queue
- Retries up to 3 times on failure

## Key Behaviors
- Orders must be atomic: either fully processed or fully rolled back
- Stock must never go negative
- Payment must never be double-charged
- Notifications are best-effort (non-blocking)
