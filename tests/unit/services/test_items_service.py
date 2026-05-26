"""Unit tests for ItemsService."""

import pytest
from unittest.mock import AsyncMock, Mock

from loyverse_sdk.services.items import ItemsService
from loyverse_sdk.exceptions import ValidationError


class TestItemsService:
    """Tests for ItemsService business logic."""

    @pytest.fixture
    def mock_items_endpoint(self):
        """Create a mock ItemsEndpoint."""
        endpoint = AsyncMock()
        endpoint.create = AsyncMock(
            return_value=Mock(id="test-id", item_name="Test Item")
        )
        endpoint.retrieve = AsyncMock(
            return_value=Mock(
                id="test-id", item_name="Test Item", updated_at="2024-01-01T00:00:00Z"
            )
        )
        endpoint.update = AsyncMock(
            return_value=Mock(id="test-id", item_name="Updated Item")
        )
        return endpoint

    @pytest.fixture
    def mock_client(self, mock_items_endpoint):
        """Create a mock LoyverseClient with mocked items endpoint."""
        client = Mock()
        client.items = mock_items_endpoint
        return client

    @pytest.fixture
    def items_service(self, mock_client):
        """Create an ItemsService instance."""
        return ItemsService(mock_client)

    @pytest.mark.asyncio
    async def test_create_item_rejects_empty_name(self, items_service):
        """Test that create_item rejects empty item name."""
        with pytest.raises(ValidationError) as exc_info:
            await items_service.create_item({"item_name": "   "})
        assert "Item name cannot be empty" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_item_accepts_valid_name(
        self, items_service, mock_items_endpoint
    ):
        """Test that create_item accepts valid item name."""
        item_data = {"item_name": "Valid Item", "track_stock": False}
        result = await items_service.create_item(item_data)
        mock_items_endpoint.create.assert_called_once_with(item_data)
        assert result is not None

    @pytest.mark.asyncio
    async def test_update_item_safe_with_version_check(
        self, items_service, mock_items_endpoint
    ):
        """Test update_item_safe checks version when expected_updated_at provided."""
        current_item = Mock(id="test-id", updated_at="2024-01-01T00:00:00Z")
        mock_items_endpoint.retrieve.return_value = current_item

        updates = {"item_name": "Updated"}
        with pytest.raises(ValidationError) as exc_info:
            await items_service.update_item_safe(
                "test-id", updates, expected_updated_at="2023-12-01T00:00:00Z"
            )
        assert "Concurrent modification detected" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_item_safe_without_version_check(
        self, items_service, mock_items_endpoint
    ):
        """Test update_item_safe skips version check when expected_updated_at is None."""
        updates = {"item_name": "Updated"}
        await items_service.update_item_safe("test-id", updates)
        mock_items_endpoint.update.assert_called_once()
