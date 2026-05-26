from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Webhook, WebhookListQuery, WebhookListResponse


class WebhooksEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "webhooks"

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Webhook)

    async def list(self, query: WebhookListQuery | None = None):
        query = query or WebhookListQuery()
        return await super().list(model=WebhookListResponse, **query.to_params())

    async def iter_all(self, query: WebhookListQuery | None = None):
        query = query or WebhookListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Webhook.model_validate(item)
