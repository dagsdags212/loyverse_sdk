"""Receipts service with business logic validation on top of ReceiptsEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Receipt
from loyverse_sdk.services.base import BaseService


class ReceiptsService(BaseService):
    """
    Service for Receipt operations with business logic validation.

    Wraps ReceiptsEndpoint with receipt data validation.
    """

    def _validate_receipt_data(self, data: dict) -> None:
        """
        Validate receipt data before create/update operations.

        Args:
            data: Receipt payload dict

        Raises:
            ValidationError: If required fields are missing
        """
        if not data:
            raise ValidationError(
                message="Receipt data cannot be empty",
                model_name="Receipt",
            )

    async def retrieve_receipt(self, id: str) -> Receipt:
        """
        Retrieve a receipt by ID.

        Args:
            id: Receipt UUID string

        Returns:
            Receipt: The retrieved receipt

        Raises:
            NotFoundError: If receipt not found
        """
        return await self._client.receipts.retrieve(id)

    async def list_receipts(self, **kwargs):
        """
        List all receipts with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Receipt objects
        """
        return await self._client.receipts.list(**kwargs)

    async def create_receipt(self, receipt_data: dict) -> Receipt:
        """
        Create a new receipt after validating input data.

        Args:
            receipt_data: Receipt creation payload dict

        Returns:
            Receipt: The created receipt

        Raises:
            ValidationError: If receipt data is invalid
        """
        self._validate_receipt_data(receipt_data)
        return await self._client.receipts.create(receipt_data)

    async def update_receipt(self, id: str, receipt_data: dict) -> Receipt:
        """
        Update an existing receipt after validating input data.

        Args:
            id: The receipt ID to update
            receipt_data: Receipt update payload dict

        Returns:
            Receipt: The updated receipt

        Raises:
            ValidationError: If receipt data is invalid
        """
        self._validate_receipt_data(receipt_data)
        return await self._client.receipts.update(id, receipt_data)

    async def iter_all_receipts(self, **kwargs):
        """
        Iterate through all receipts using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Receipt objects
        """
        async for receipt in self._client.receipts.iter_all(**kwargs):
            yield receipt
