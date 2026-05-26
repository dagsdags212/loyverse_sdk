"""Shifts service with business logic validation on top of ShiftsEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Shift
from loyverse_sdk.services.base import BaseService


class ShiftsService(BaseService):
    """
    Service for Shift operations with business logic validation.

    Wraps ShiftsEndpoint with shift data validation.
    """

    def _validate_shift_data(self, data: dict) -> None:
        """
        Validate shift data before create/update operations.

        Args:
            data: Shift payload dict

        Raises:
            ValidationError: If required fields are missing
        """
        if not data:
            raise ValidationError(
                message="Shift data cannot be empty",
                model_name="Shift",
            )

    async def retrieve_shift(self, id: str) -> Shift:
        """
        Retrieve a shift by ID.

        Args:
            id: Shift UUID string

        Returns:
            Shift: The retrieved shift

        Raises:
            NotFoundError: If shift not found
        """
        return await self._client.shifts.retrieve(id)

    async def list_shifts(self, **kwargs):
        """
        List all shifts with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Shift objects
        """
        return await self._client.shifts.list(**kwargs)

    async def iter_all_shifts(self, **kwargs):
        """
        Iterate through all shifts using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Shift objects
        """
        async for shift in self._client.shifts.iter_all(**kwargs):
            yield shift
