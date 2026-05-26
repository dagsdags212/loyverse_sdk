"""Taxes service with business logic validation on top of TaxesEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Tax
from loyverse_sdk.services.base import BaseService


class TaxesService(BaseService):
    """
    Service for Tax operations with business logic validation.

    Wraps TaxesEndpoint with validation for tax percentages
    and compound tax status.
    """

    def _validate_tax_data(self, data: dict) -> None:
        """
        Validate tax data before create/update operations.

        Raises:
            ValidationError: If tax percentage is out of range
        """
        if not data:
            raise ValidationError(
                message="Tax data cannot be empty",
                model_name="Tax",
            )

        rate = data.get("rate")
        if rate is not None:
            if rate < 0 or rate > 100:
                raise ValidationError(
                    message="Tax rate must be between 0 and 100",
                    model_name="Tax",
                )

    async def create_tax(self, tax_data: dict) -> Tax:
        """
        Create a new tax after validating input data.

        Args:
            tax_data: Tax creation payload dict

        Returns:
            Tax: The created tax

        Raises:
            ValidationError: If tax percentage is out of range
        """
        self._validate_tax_data(tax_data)
        return await self._client.taxes.create(tax_data)

    async def update_tax(self, id: str, tax_data: dict) -> Tax:
        """
        Update an existing tax after validating input data.

        Args:
            id: The tax ID to update
            tax_data: Tax update payload dict

        Returns:
            Tax: The updated tax

        Raises:
            ValidationError: If tax percentage is out of range
        """
        self._validate_tax_data(tax_data)
        return await self._client.taxes.update(id, tax_data)
