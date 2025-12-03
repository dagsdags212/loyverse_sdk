from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.models import PosDevice, PosDeviceListResponse


class PosDevicesEndpoints(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "pos_devices"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=PosDeviceListResponse
        )

    async def iter_all(self):
        async for item in super().iter_all():
            yield PosDevice.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=PosDevice)
