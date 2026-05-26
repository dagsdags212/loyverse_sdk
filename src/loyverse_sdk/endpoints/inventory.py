from loyverse_sdk.core.config import config
from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Inventory, InventoryListResponse


class InventoryEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "inventory"
    items_key = "inventory_levels"

    async def list(self, limit: int = config.PAGE_LIMIT, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=InventoryListResponse
        )

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Inventory)

    async def iter_all(self, **kwargs):
        async for item in super().iter_all(**kwargs):
            yield Inventory.model_validate(item)
