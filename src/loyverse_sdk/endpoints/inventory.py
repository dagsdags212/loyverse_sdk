from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Inventory, InventoryListQuery, InventoryListResponse


class InventoryEndpoint(BaseEndpoint, ListMixin, PaginationMixin):
    path = "inventory"
    items_key = "inventory_levels"

    async def list(self, query: InventoryListQuery | None = None):
        query = query or InventoryListQuery()
        return await super().list(model=InventoryListResponse, **query.to_params())

    async def iter_all(self, query: InventoryListQuery | None = None):
        query = query or InventoryListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Inventory.model_validate(item)
