from loyverse_api.api.endpoints import LoyverseEndpoints
from loyverse_api.models import Receipt
from loyverse_api.models import Customer
import pytest


@pytest.fixture
def endpoint():
    """Instantiate endpoint for /receipts"""
    return LoyverseEndpoints.RECEIPTS


def test_receipt_endpoint_creation(endpoint):
    """Test /receipt API endpoint creation"""
    assert endpoint.url.endswith("receipts")
    assert endpoint.api_key is not None


def test_receipts_endpoint(endpoint):
    """Test receipt data ingestion and validation"""
    receipts, _ = endpoint._get()
    for receipt in receipts:
        Receipt.model_validate(receipt)


@pytest.fixture
def get_receipt_id():
    """Specific instance of a receipt id"""
    return "8-4072"


def test_fetch_receipt_by_id(endpoint, get_receipt_id):
    """Test receipt data retrieval from id"""
    rdata = endpoint.fetch_by_id(get_receipt_id)
    receipt = Receipt.model_validate(rdata)

    cdata = LoyverseEndpoints.CUSTOMERS.fetch_by_id(receipt.customer_id)
    customer = Customer.model_validate(cdata)

    assert receipt.customer_id == customer.id
