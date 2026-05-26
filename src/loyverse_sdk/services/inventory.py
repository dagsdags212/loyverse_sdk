"""Inventory service with business logic validation on top of InventoryEndpoint."""

from loyverse_sdk.models import Inventory
from loyverse_sdk.services.base import BaseService


class InventoryService(BaseService):
    """
    Service for Inventory operations with business logic validation.

    Wraps InventoryEndpoint with inventory-level validation.
    """

    def _validate_inventory_data(self, data: dict) -> None:
        """
        Validate inventory data before create/update operations.

        Args:
            data: Inventory payload dict

        Raises:
            ValidationError: If required fields are missing
        """
        if not data:
            from loyverse_sdk.exceptions import ValidationError

            raise ValidationError(
                message="Inventory data cannot be empty",
                model_name="Inventory",
            )

    async def retrieve_inventory(self, id: str) -> Inventory:
        """
        Retrieve an inventory level by ID.

        Args:
            id: Inventory UUID string

        Returns:
            Inventory: The retrieved inventory level

        Raises:
            NotFoundError: If inventory not found
        """
        return await self._client.inventory.retrieve(id)

    async def list_inventory_levels(self, **kwargs):
        """
        List all inventory levels with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Inventory objects
        """
        return await self._client.inventory.list(**kwargs)

    async def iter_all_inventory(self, **kwargs):
        """
        Iterate through all inventory levels using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Inventory objects
        """
        async for item in self._client.inventory.iter_all(**kwargs):
            yield item
