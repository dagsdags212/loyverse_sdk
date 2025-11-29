# Loyverse API

A python library for interacting with the Loyverse API.

## Installation

The package utilizes `uv` for local installation.

```
git clone https://github.com/dagsdags212/loyverse_api.git
uv install loyverse_api
```

## Setup

Provide your Loyverse API key as an environment variable named `LOYVERSE_API_KEY`. 
```sh
export LOYVERSE_API_KEY=your_api_key
```

The API key may also be provided in a separate `.env` file located at the root of your project directory.
```.env
LOYVERSE_API_KEY=your_api_key
```

You can also specify the API key in your python script:
```python
import os
os.environ["LOYVERSE_API_KEY"] = "your_api_key"
```

## Usage

**Specifying Endpoints**

An interface to each endpoints specified in the official [Loyverse API reference](https://developer.loyverse.com/docs/#section/Pagination)
is provided by the `LoyverseEndpoints` class under the `endpoints` submodule.

```python
from loyverse_api.api.endpoints import LoyverseEndpoints

customers_endpoint = LoyverseEndpoints.CUSTOMERS
receipts_endpoint = LoyverseEndpoints.RECEIPTS
employees_endpoint = LoyverseEndpoints.EMPLOYEES
```

As of the most recent version, the endponts marked with a check are supported:

- [x] `/customers`
- [x] `/discounts`
- [x] `/employees`
- [x] `/inventory`
- [x] `/items`
- [x] `/payment_types`
- [x] `/pos_devices`
- [x] `/receipts`
- [x] `/stores`
- [ ] `/categories`
- [ ] `/shifts`
- [ ] `/suppliers`
- [ ] `/taxes`
- [ ] `/webhooks`
- [ ] `/variants`

**Query Parameters**

Set the query parameters thru the `.params` attribute. For example, we can override the limit of retrieving 50 records per request to 250 as follows:

```python
receipts_endpoint.params['limit'] = 250

# A more pythonic way
receipts_endpoint.set_limit(250)
```

Alternatively, globally set the value using the `LOYVERSE_LIMIT` enviroment variable:
```.env
LOYVERSE_LIMIT=250
```

**Retrieving Data**

`Endpoint` objects have the `fetch_all` method to retrieve all records:
```python
receipts_endpoint.fetch_all()

# Enable debug mode
receipts_endpoint.fetch_all(debug=True)
```

Convenience methods are also provided for retrieving **filtered** records:
```python
from datetime import datetime

# Get the 10 most recent transactions
receipts.fetch_most_recent(10)

# Get transactions created AFTER a specified date
start = datetime(2025, 1, 1)
receipts_endpoint.fetch_after_dt(dt=start)

# Get transactions created BEFORE a specified date
end = datetime(2025, 1, 1)
receipts_endpoint.fetch_before_dt(dt=end)

# Get transactions created between two dates
receipts_endpoint.fetch_between_dt(start=start, end=end)
```
