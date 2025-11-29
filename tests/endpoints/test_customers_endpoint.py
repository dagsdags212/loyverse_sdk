from loyverse_api.api.endpoints import LoyverseEndpoints
from loyverse_api.models import Customer
import pytest


@pytest.fixture
def endpoint():
    """Instantiate endpoint for /customers"""
    return LoyverseEndpoints.CUSTOMERS


def test_customers_endpoint(endpoint):
    customers = endpoint._get()
    assert len(customers) > 0


def test_fetch_all_customers(endpoint):
    customers = endpoint.fetch_all(debug=False)
    for customer in customers:
        Customer.model_validate(customer)


def test_fetch_customer_by_id(endpoint):
    cid = "35d627e4-5ef8-4e8c-bfa5-df775720069b"
    data = endpoint.fetch_by_id(cid)

    c = Customer.model_validate(data)

    assert c.name == "Marguerite Hoch"
    assert c.email == "margueritehoch@gmail.com"
