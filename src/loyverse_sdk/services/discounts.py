"""Discounts service with business logic validation on top of DiscountsEndpoint."""

from typing import Self

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Discount
from loyverse_sdk.services.base import BaseService


class DiscountsService(BaseService):
    """
    Service for Discount operations with business logic validation.

    Wraps DiscountsEndpoint with validation for discount types,
    percentage ranges, and amount constraints.
    """

    def _validate_percentage(self, discount_type: str, value: float) -> None:
        """
        Validate that percentage-type discounts are in range 0-100.

        Raises:
            ValidationError: If value is out of range for percentage type
        """
        if discount_type == "FIXED_PERCENT" or discount_type == "VARIABLE_PERCENT":
            if value > 100 or value < 0:
                raise ValidationError(
                    message="Percentage discount must be between 0 and 100",
                    model_name="Discount",
                )
        elif value < 0:
            raise ValidationError(
                message="Discount value cannot be negative",
                model_name="Discount",
            )

    def _validate_discount_data(self, data: dict) -> None:
        """
        Validate discount data before create/update operations.

        Raises:
            ValidationError: If required fields are missing or invalid
        """
        if not data:
            raise ValidationError(
                message="Discount data cannot be empty",
                model_name="Discount",
            )

        # Validate type is present
        discount_type = data.get("type")
        if not discount_type:
            raise ValidationError(
                message="Discount 'type' field is required",
                model_name="Discount",
            )

        # Validate percentage value if applicable
        percent_val = data.get("discount_percent")
        if percent_val is not None:
            self._validate_percentage(discount_type, percent_val)

        # Validate amount if applicable
        amount_val = data.get("discount_amount")
        if amount_val is not None:
            if amount_val < 0:
                raise ValidationError(
                    message="Discount amount cannot be negative",
                    model_name="Discount",
                )

    async def create_discount(self, discount_data: dict) -> Discount:
        """
        Create a new discount after validating input data.

        Args:
            discount_data: Discount creation payload dict

        Returns:
            Discount: The created discount

        Raises:
            ValidationError: If discount data is invalid
        """
        self._validate_discount_data(discount_data)
        return await self._client.discounts.create(discount_data)

    async def update_discount(self, id: str, discount_data: dict) -> Discount:
        """
        Update an existing discount after validating input data.

        Args:
            id: The discount ID to update
            discount_data: Discount update payload dict

        Returns:
            Discount: The updated discount

        Raises:
            ValidationError: If discount data is invalid
        """
        self._validate_discount_data(discount_data)
        return await self._client.discounts.update(id, discount_data)
