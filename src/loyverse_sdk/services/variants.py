"""Variants service with business logic validation on top of VariantsEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Variant
from loyverse_sdk.services.base import BaseService


class VariantsService(BaseService):
    """
    Service for Variant operations with business logic validation.

    Wraps VariantsEndpoint with variant name and SKU validation.
    """

    def _validate_variant_data(self, data: dict) -> None:
        """
        Validate variant data before create/update operations.

        Args:
            data: Variant payload dict

        Raises:
            ValidationError: If required fields are missing or invalid
        """
        if not data:
            raise ValidationError(
                message="Variant data cannot be empty",
                model_name="Variant",
            )

        name = data.get("name")
        if not name or not str(name).strip():
            raise ValidationError(
                message="Variant name cannot be empty or whitespace-only",
                model_name="Variant",
            )

    async def retrieve_variant(self, id: str) -> Variant:
        """
        Retrieve a variant by ID.

        Args:
            id: Variant UUID string

        Returns:
            Variant: The retrieved variant

        Raises:
            NotFoundError: If variant not found
        """
        return await self._client.variants.retrieve(id)

    async def list_variants(self, **kwargs):
        """
        List all variants with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Variant objects
        """
        return await self._client.variants.list(**kwargs)

    async def create_variant(self, variant_data: dict) -> Variant:
        """
        Create a new variant after validating input data.

        Args:
            variant_data: Variant creation payload dict

        Returns:
            Variant: The created variant

        Raises:
            ValidationError: If variant name is empty
        """
        self._validate_variant_data(variant_data)
        return await self._client.variants.create(variant_data)

    async def update_variant(self, id: str, variant_data: dict) -> Variant:
        """
        Update an existing variant after validating input data.

        Args:
            id: The variant ID to update
            variant_data: Variant update payload dict

        Returns:
            Variant: The updated variant

        Raises:
            ValidationError: If variant name is empty
        """
        self._validate_variant_data(variant_data)
        return await self._client.variants.update(id, variant_data)

    async def iter_all_variants(self, **kwargs):
        """
        Iterate through all variants using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Variant objects
        """
        async for variant in self._client.variants.iter_all(**kwargs):
            yield variant
