"""Webhooks service with business logic validation on top of WebhooksEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Webhook
from loyverse_sdk.services.base import BaseService


class WebhooksService(BaseService):
    """
    Service for Webhook operations with business logic validation.

    Wraps WebhooksEndpoint with webhook URL and event validation.
    """

    def _validate_webhook_data(self, data: dict) -> None:
        """
        Validate webhook data before create/update operations.

        Args:
            data: Webhook payload dict

        Raises:
            ValidationError: If webhook URL is missing or invalid
        """
        if not data:
            raise ValidationError(
                message="Webhook data cannot be empty",
                model_name="Webhook",
            )

        url = data.get("webhook_url")
        if not url or not str(url).strip():
            raise ValidationError(
                message="Webhook URL cannot be empty or whitespace-only",
                model_name="Webhook",
            )

        # Basic URL format validation
        if url and not url.startswith(("http://", "https://")):
            raise ValidationError(
                message="Webhook URL must start with http:// or https://",
                model_name="Webhook",
            )

    async def retrieve_webhook(self, id: str) -> Webhook:
        """
        Retrieve a webhook by ID.

        Args:
            id: Webhook UUID string

        Returns:
            Webhook: The retrieved webhook

        Raises:
            NotFoundError: If webhook not found
        """
        return await self._client.webhooks.retrieve(id)

    async def list_webhooks(self, **kwargs):
        """
        List all webhooks with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Webhook objects
        """
        return await self._client.webhooks.list(**kwargs)

    async def create_webhook(self, webhook_data: dict) -> Webhook:
        """
        Create a new webhook after validating input data.

        Args:
            webhook_data: Webhook creation payload dict

        Returns:
            Webhook: The created webhook

        Raises:
            ValidationError: If webhook URL is invalid
        """
        self._validate_webhook_data(webhook_data)
        return await self._client.webhooks.create(webhook_data)

    async def update_webhook(self, id: str, webhook_data: dict) -> Webhook:
        """
        Update an existing webhook after validating input data.

        Args:
            id: The webhook ID to update
            webhook_data: Webhook update payload dict

        Returns:
            Webhook: The updated webhook

        Raises:
            ValidationError: If webhook URL is invalid
        """
        self._validate_webhook_data(webhook_data)
        return await self._client.webhooks.update(id, webhook_data)

    async def delete_webhook(self, id: str) -> None:
        """
        Delete a webhook by ID.

        Args:
            id: The webhook ID to delete

        Raises:
            NotFoundError: If webhook not found
        """
        return await self._client.webhooks.delete(id)

    async def iter_all_webhooks(self, **kwargs):
        """
        Iterate through all webhooks using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Webhook objects
        """
        async for webhook in self._client.webhooks.iter_all(**kwargs):
            yield webhook
