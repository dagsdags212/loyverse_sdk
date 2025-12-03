from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Store, StoreListResponse


class StoresEndpoint(BaseEndpoint, ListMixin, RetrieveMixin):
    path = "stores"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(limit=limit, cursor=cursor, model=StoreListResponse)

    async def iter_all(self, **kwargs):
        async for item in super().iter_all(**kwargs):
            yield Store.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Store)
