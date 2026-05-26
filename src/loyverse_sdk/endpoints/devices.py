from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import PosDevice, PosDeviceListQuery, PosDeviceListResponse


class PosDevicesEndpoints(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "pos_devices"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=PosDevice)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=PosDevice)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=PosDevice)

    async def list(self, query: PosDeviceListQuery | None = None):
        query = query or PosDeviceListQuery()
        return await super().list(model=PosDeviceListResponse, **query.to_params())

    async def iter_all(self, query: PosDeviceListQuery | None = None):
        query = query or PosDeviceListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield PosDevice.model_validate(item)
