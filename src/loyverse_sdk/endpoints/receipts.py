from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Receipt, ReceiptListResponse


class ReceiptsEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "receipts"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(limit=limit, cursor=cursor, model=ReceiptListResponse)

    async def iter_all(self):
        async for item in super().iter_all():
            yield Receipt.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Receipt)
