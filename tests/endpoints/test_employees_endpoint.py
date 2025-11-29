import pytest
from loyverse_api.api.endpoints import LoyverseEndpoints
from loyverse_api.models.user import Employee


@pytest.fixture
def endpoint():
    """Instantiate endpoint for /employees"""
    return LoyverseEndpoints.EMPLOYEES


@pytest.fixture
def get_employees():
    """Return a list of current employees"""
    return ["Hannah", "Matet"]


def test_employees_endpoint(endpoint):
    data, _ = endpoint._get()
    assert len(data) == 2


def test_employees_ingestion(endpoint, get_employees):
    data, _ = endpoint._get()
    for empl in data:
        e = Employee.model_validate(empl)
        assert e.name in get_employees
