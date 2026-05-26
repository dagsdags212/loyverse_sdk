"""Unit tests for BaseService."""

import pytest
from unittest.mock import Mock

from loyverse_sdk.services.base import BaseService


class TestBaseService:
    """Tests for BaseService class."""

    def test_init_stores_client_reference(self):
        """Test that __init__ stores the client reference."""
        mock_client = Mock()
        service = BaseService(mock_client)
        assert service._client is mock_client

    def test_client_property_returns_client(self):
        """Test that client property returns the stored client."""
        mock_client = Mock()
        service = BaseService(mock_client)
        assert service.client is mock_client

    def test_client_property_is_readonly(self):
        """Test that client property cannot be reassigned."""
        mock_client = Mock()
        service = BaseService(mock_client)
        with pytest.raises(AttributeError):
            service.client = Mock()  # Should not allow reassignment
