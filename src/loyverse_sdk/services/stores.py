"""Stores service with business logic validation on top of StoresEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Store
from loyverse_sdk.services.base import BaseService


class StoresService(BaseService):
    """
    Service for Store operations with business logic validation.

    Wraps StoresEndpoint with store name validation.
    """

    def _validate_store_data(self, data: dict) -> None:
        """
        Validate store data before create/update operations.

        Args:
            data: Store payload dict

        Raises:
            ValidationError: If store name is empty
        """
        if not data:
            raise ValidationError(
                message="Store data cannot be empty",
                model_name="Store",
            )

        name = data.get("name")
        if not name or not str(name).strip():
            raise ValidationError(
                message="Store name cannot be empty or whitespace-only",
                model_name="Store",
            )

    async def retrieve_store(self, id: str) -> Store:
        """
        Retrieve a store by ID.

        Args:
            id: Store UUID string

        Returns:
            Store: The retrieved store

        Raises:
            NotFoundError: If store not found
        """
        return await self._client.stores.retrieve(id)

    async def list_stores(self, **kwargs):
        """
        List all stores with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Store objects
        """
        return await self._client.stores.list(**kwargs)

    async def create_store(self, store_data: dict) -> Store:
        """
        Create a new store after validating input data.

        Args:
            store_data: Store creation payload dict

        Returns:
            Store: The created store

        Raises:
            ValidationError: If store name is empty
        """
        self._validate_store_data(store_data)
        return await self._client.stores.create(store_data)

    async def update_store(self, id: str, store_data: dict) -> Store:
        """
        Update an existing store after validating input data.

        Args:
            id: The store ID to update
            store_data: Store update payload dict

        Returns:
            Store: The updated store

        Raises:
            ValidationError: If store name is empty
        """
        self._validate_store_data(store_data)
        return await self._client.stores.update(id, store_data)

    async def iter_all_stores(self, **kwargs):
        """
        Iterate through all stores using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Store objects
        """
        async for store in self._client.stores.iter_all(**kwargs):
            yield store
