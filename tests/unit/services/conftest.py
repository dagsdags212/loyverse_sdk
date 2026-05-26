"""Shared fixtures for service layer tests."""

from unittest.mock import Mock, AsyncMock
import pytest

from loyverse_sdk.services.base import BaseService


@pytest.fixture
def mock_client():
    """Create a mock LoyverseClient with mocked endpoints."""
    client = Mock()
    # Mock each endpoint
    client.items = AsyncMock()
    client.customers = AsyncMock()
    client.discounts = AsyncMock()
    client.categories = AsyncMock()
    client.taxes = AsyncMock()
    return client


@pytest.fixture
def base_service(mock_client):
    """Create a BaseService instance for testing."""
    return BaseService(mock_client)
