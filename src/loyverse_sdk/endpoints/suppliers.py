from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Supplier, SupplierListQuery, SupplierListResponse


class SuppliersEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "suppliers"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Supplier)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Supplier)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Supplier)

    async def list(self, query: SupplierListQuery | None = None):
        query = query or SupplierListQuery()
        return await super().list(model=SupplierListResponse, **query.to_params())

    async def iter_all(self, query: SupplierListQuery | None = None):
        query = query or SupplierListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Supplier.model_validate(item)
