"""Suppliers service with business logic validation on top of SuppliersEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Supplier
from loyverse_sdk.services.base import BaseService


class SuppliersService(BaseService):
    """
    Service for Supplier operations with business logic validation.

    Wraps SuppliersEndpoint with supplier name and contact validation.
    """

    def _validate_supplier_data(self, data: dict) -> None:
        """
        Validate supplier data before create/update operations.

        Args:
            data: Supplier payload dict

        Raises:
            ValidationError: If supplier name is empty
        """
        if not data:
            raise ValidationError(
                message="Supplier data cannot be empty",
                model_name="Supplier",
            )

        name = data.get("name")
        if not name or not str(name).strip():
            raise ValidationError(
                message="Supplier name cannot be empty or whitespace-only",
                model_name="Supplier",
            )

    async def retrieve_supplier(self, id: str) -> Supplier:
        """
        Retrieve a supplier by ID.

        Args:
            id: Supplier UUID string

        Returns:
            Supplier: The retrieved supplier

        Raises:
            NotFoundError: If supplier not found
        """
        return await self._client.suppliers.retrieve(id)

    async def list_suppliers(self, **kwargs):
        """
        List all suppliers with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Supplier objects
        """
        return await self._client.suppliers.list(**kwargs)

    async def create_supplier(self, supplier_data: dict) -> Supplier:
        """
        Create a new supplier after validating input data.

        Args:
            supplier_data: Supplier creation payload dict

        Returns:
            Supplier: The created supplier

        Raises:
            ValidationError: If supplier name is empty
        """
        self._validate_supplier_data(supplier_data)
        return await self._client.suppliers.create(supplier_data)

    async def update_supplier(self, id: str, supplier_data: dict) -> Supplier:
        """
        Update an existing supplier after validating input data.

        Args:
            id: The supplier ID to update
            supplier_data: Supplier update payload dict

        Returns:
            Supplier: The updated supplier

        Raises:
            ValidationError: If supplier name is empty
        """
        self._validate_supplier_data(supplier_data)
        return await self._client.suppliers.update(id, supplier_data)

    async def iter_all_suppliers(self, **kwargs):
        """
        Iterate through all suppliers using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Supplier objects
        """
        async for supplier in self._client.suppliers.iter_all(**kwargs):
            yield supplier
