"""Modifiers service with business logic validation on top of ModifiersEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Modifier
from loyverse_sdk.services.base import BaseService


class ModifiersService(BaseService):
    """
    Service for Modifier operations with business logic validation.

    Wraps ModifiersEndpoint with modifier name validation.
    """

    def _validate_modifier_data(self, data: dict) -> None:
        """
        Validate modifier data before create/update operations.

        Args:
            data: Modifier payload dict

        Raises:
            ValidationError: If modifier name is empty
        """
        if not data:
            raise ValidationError(
                message="Modifier data cannot be empty",
                model_name="Modifier",
            )

        name = data.get("name")
        if not name or not str(name).strip():
            raise ValidationError(
                message="Modifier name cannot be empty or whitespace-only",
                model_name="Modifier",
            )

    async def retrieve_modifier(self, id: str) -> Modifier:
        """
        Retrieve a modifier by ID.

        Args:
            id: Modifier UUID string

        Returns:
            Modifier: The retrieved modifier

        Raises:
            NotFoundError: If modifier not found
        """
        return await self._client.modifiers.retrieve(id)

    async def list_modifiers(self, **kwargs):
        """
        List all modifiers with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Modifier objects
        """
        return await self._client.modifiers.list(**kwargs)

    async def create_modifier(self, modifier_data: dict) -> Modifier:
        """
        Create a new modifier after validating input data.

        Args:
            modifier_data: Modifier creation payload dict

        Returns:
            Modifier: The created modifier

        Raises:
            ValidationError: If modifier name is empty
        """
        self._validate_modifier_data(modifier_data)
        return await self._client.modifiers.create(modifier_data)

    async def update_modifier(self, id: str, modifier_data: dict) -> Modifier:
        """
        Update an existing modifier after validating input data.

        Args:
            id: The modifier ID to update
            modifier_data: Modifier update payload dict

        Returns:
            Modifier: The updated modifier

        Raises:
            ValidationError: If modifier name is empty
        """
        self._validate_modifier_data(modifier_data)
        return await self._client.modifiers.update(id, modifier_data)

    async def iter_all_modifiers(self, **kwargs):
        """
        Iterate through all modifiers using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Modifier objects
        """
        async for modifier in self._client.modifiers.iter_all(**kwargs):
            yield modifier
