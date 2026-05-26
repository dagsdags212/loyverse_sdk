"""
Unit tests for loyverse_sdk.endpoints.inventory module.

Tests endpoint structure, method contracts, and filter parameter forwarding
without real API calls.
"""

import pytest
import inspect
from unittest.mock import AsyncMock, MagicMock
from loyverse_sdk.endpoints.inventory import InventoryEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.endpoints.base import BaseEndpoint


class TestInventoryEndpointStructure:
    """Test InventoryEndpoint class structure and MRO."""

    def test_inherits_correct_mixins(self):
        """InventoryEndpoint should inherit ListMixin and PaginationMixin but NOT RetrieveMixin."""
        mro = InventoryEndpoint.__mro__
        assert BaseEndpoint in mro, "Should inherit BaseEndpoint"
        assert ListMixin in mro, "Should inherit ListMixin"
        assert PaginationMixin in mro, "Should inherit PaginationMixin"
        assert RetrieveMixin not in mro, "Should NOT inherit RetrieveMixin"

    def test_no_retrieve_method(self):
        """InventoryEndpoint should NOT have a retrieve() method."""
        client = MagicMock()
        client.request = AsyncMock()
        endpoint = InventoryEndpoint(client)

        with pytest.raises(AttributeError):
            endpoint.retrieve("some-id")

    def test_path_is_inventory(self):
        """Endpoint path should be 'inventory'."""
        client = MagicMock()
        client.request = AsyncMock()
        endpoint = InventoryEndpoint(client)
        assert endpoint.path == "inventory"

    def test_items_key_is_inventory_levels(self):
        """Items key should be 'inventory_levels' for pagination."""
        client = MagicMock()
        client.request = AsyncMock()
        endpoint = InventoryEndpoint(client)
        assert endpoint.items_key == "inventory_levels"


class TestInventoryEndpointListSignature:
    """Test the list() method signature includes filter parameters."""

    def test_list_has_store_id_param(self):
        """list() should accept an optional store_id parameter."""
        sig = inspect.signature(InventoryEndpoint.list)
        assert "store_id" in sig.parameters
        param = sig.parameters["store_id"]
        assert param.default is None, "store_id should default to None"

    def test_list_has_variant_ids_param(self):
        """list() should accept an optional variant_ids parameter."""
        sig = inspect.signature(InventoryEndpoint.list)
        assert "variant_ids" in sig.parameters
        param = sig.parameters["variant_ids"]
        assert param.default is None, "variant_ids should default to None"

    def test_list_has_limit_param(self):
        """list() should accept limit parameter."""
        sig = inspect.signature(InventoryEndpoint.list)
        assert "limit" in sig.parameters

    def test_list_has_cursor_param(self):
        """list() should accept cursor parameter."""
        sig = inspect.signature(InventoryEndpoint.list)
        assert "cursor" in sig.parameters


class TestInventoryEndpointHasIterAll:
    """Test that iter_all is available (from PaginationMixin)."""

    def test_iter_all_exists(self):
        """iter_all should be callable."""
        client = MagicMock()
        client.request = AsyncMock()
        endpoint = InventoryEndpoint(client)
        assert callable(endpoint.iter_all)

    def test_iter_all_is_async_generator(self):
        """iter_all should be an async generator function."""
        assert inspect.isasyncgenfunction(InventoryEndpoint.iter_all)


class TestInventoryEndpointFilterForwarding:
    """Test filter parameter forwarding behavior."""

    @pytest.mark.asyncio
    async def test_list_forwards_store_id_filter(self):
        """list(store_id=...) should pass store_id as query param to API."""
        client = MagicMock()
        client.request = AsyncMock(
            return_value={
                "inventory_levels": [],
                "cursor": None,
            }
        )
        endpoint = InventoryEndpoint(client)

        await endpoint.list(store_id="store-abc")

        call_args = client.request.call_args
        assert call_args[0][0] == "GET"
        assert call_args[0][1] == "inventory"
        assert "store_id" in str(call_args[1].get("params", {}))

    @pytest.mark.asyncio
    async def test_list_forwards_variant_ids_filter(self):
        """list(variant_ids=...) should pass variant_ids as query param to API."""
        client = MagicMock()
        client.request = AsyncMock(
            return_value={
                "inventory_levels": [],
                "cursor": None,
            }
        )
        endpoint = InventoryEndpoint(client)

        await endpoint.list(variant_ids="var-1,var-2")

        call_args = client.request.call_args
        assert call_args[0][0] == "GET"
        assert call_args[0][1] == "inventory"
        assert "variant_ids" in str(call_args[1].get("params", {}))

    @pytest.mark.asyncio
    async def test_list_no_filters_works(self):
        """list() without filters should still work."""
        client = MagicMock()
        client.request = AsyncMock(
            return_value={
                "inventory_levels": [],
                "cursor": None,
            }
        )
        endpoint = InventoryEndpoint(client)

        await endpoint.list()

        call_args = client.request.call_args
        assert call_args[0][0] == "GET"
        assert call_args[0][1] == "inventory"
