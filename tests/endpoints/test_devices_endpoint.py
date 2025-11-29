from uuid import UUID
import pytest
from loyverse_api.api.endpoints import LoyverseEndpoints
from loyverse_api.models import PosDevice


@pytest.fixture
def endpoint():
    """Instantiate endpoint for /pos_devices"""
    return LoyverseEndpoints.POS_DEVICES


@pytest.fixture
def get_store_id():
    """Return id of main store"""
    return "86dd335a-7d4e-406d-adbd-3bde9b81804d"


def test_device_endpoint(endpoint):
    data, _ = endpoint._get()
    assert len(data) > 0


def test_stores_ingestion(endpoint, get_store_id):
    data, _ = endpoint._get()
    for device in data:
        d = PosDevice.model_validate(device)
        assert d.name is not None
        assert d.store_id == UUID(get_store_id)
