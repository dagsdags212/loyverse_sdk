from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Webhook, WebhookListResponse


class WebhooksEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "webhooks"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(limit=limit, cursor=cursor, model=WebhookListResponse)

    async def iter_all(self, **kwargs):
        async for item in super().iter_all(**kwargs):
            yield Webhook.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Webhook)
