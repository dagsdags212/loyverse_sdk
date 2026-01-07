# Loyverse SDK

Asynchronous Python SDK for the [Loyverse API](https://developer.loyverse.com/docs/), a point-of-sale (POS) system for managing business transactions, inventory, and customer data.

## Overview

The SDK provides:
- **Async/await** interface using `httpx` for non-blocking API calls
- **Type-safe** request/response models using Pydantic
- **Automatic pagination** with cursor-based iteration via `iter_all()`
- **Full CRUD operations** for supported endpoints
- **14 endpoints**: categories, customers, discounts, devices, employees, items, merchant, modifiers, receipts, stores, suppliers, taxes, webhooks, variants

### Codebase Structure

**`src/loyverse_sdk/`** contains:
- `client.py` - Main `LoyverseClient` class with endpoint access
- `endpoints/` - Endpoint classes using mixin pattern for CRUD operations
- `models/` - Pydantic models for request/response validation
- `auth.py` - Token-based authentication
- `core/` - Configuration, logging, and utilities

## Installation

```bash
uv pip install git+https://github.com/dagsdags212/loyverse_sdk.git
```

## Setup

Set your API token as an environment variable:

```bash
export LOYVERSE_API_TOKEN=your_api_token
```

Or create a `.env` file in your project root:

```env
LOYVERSE_API_TOKEN=your_api_token
```

## Quick Start

```python
import asyncio
from loyverse_sdk import LoyverseClient

async def main():
    # Create client (automatically loads token from environment)
    client = LoyverseClient()

    # List customers
    response = await client.customers.list(limit=10)
    print(f"Found {len(response.items)} customers")

    # Close connection
    await client.close()

asyncio.run(main())
```

## Usage Examples

### Customers Endpoint

The customers endpoint manages customer data from your POS system.

**List customers with pagination:**

```python
# Get first page of customers
response = await client.customers.list(limit=50)

for customer in response.items:
    print(f"{customer.name} - {customer.email}")
    print(f"  Total visits: {customer.total_visits}")
    print(f"  Total spent: ${customer.total_spent}")

# Get next page using cursor
if response.cursor:
    next_page = await client.customers.list(limit=50, cursor=response.cursor)
```

**Retrieve a single customer:**

```python
customer = await client.customers.retrieve(id="customer-uuid-here")
print(customer.name)
print(customer.phone_number)
print(customer.address)
```

**Create a new customer:**

```python
new_customer = await client.customers.create({
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St",
    "city": "San Francisco",
    "postal_code": "94102",
    "customer_code": "CUST001"
})

print(f"Created customer: {new_customer.id}")
```

**Update an existing customer:**

```python
updated = await client.customers.update(
    id=customer.id,
    payload={"email": "newemail@example.com", "note": "VIP customer"}
)

print(f"Updated {updated.name}")
```

**Delete a customer:**

```python
result = await client.customers.delete(id=customer.id)
print(result)  # {'deleted_object_ids': ['customer-uuid']}
```

**Iterate through all customers:**

```python
# Automatically handles pagination across all pages
async for customer in client.customers.iter_all():
    print(f"{customer.name} - Last visit: {customer.last_visit}")
```

**Filter customers by date:**

```python
from datetime import datetime

# Get customers created in the last 30 days
start_date = datetime.now() - timedelta(days=30)

async for customer in client.customers.iter_all(created_at_min=start_date):
    tenure = customer.tenure()  # timedelta between first and last visit
    print(f"{customer.name} - Customer for {tenure.days} days")
```

### Other Endpoints

All endpoints follow the same pattern. Available endpoints:

```python
client.categories   # Item categories
client.customers    # Customer records
client.discounts    # Discount rules
client.devices      # POS devices
client.employees    # Staff members
client.items        # Inventory items
client.merchant     # Merchant info
client.modifiers    # Item modifiers
client.receipts     # Transaction receipts
client.stores       # Store locations
client.suppliers    # Supplier records
client.taxes        # Tax configurations
client.variants     # Item variants
client.webhooks     # Webhook subscriptions
```

Each endpoint supports operations based on the [Loyverse API capabilities](https://developer.loyverse.com/docs/).
