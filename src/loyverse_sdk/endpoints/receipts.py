from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Receipt, ReceiptListQuery, ReceiptListResponse


class ReceiptsEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "receipts"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Receipt)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Receipt)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Receipt)

    async def list(self, query: ReceiptListQuery | None = None):
        query = query or ReceiptListQuery()
        return await super().list(model=ReceiptListResponse, **query.to_params())

    async def iter_all(self, query: ReceiptListQuery | None = None):
        query = query or ReceiptListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Receipt.model_validate(item)
