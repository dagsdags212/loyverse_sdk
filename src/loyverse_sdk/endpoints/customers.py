from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Customer, CustomerListQuery, CustomerListResponse


class CustomersEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "customers"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Customer)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Customer)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Customer)

    async def list(self, query: CustomerListQuery | None = None):
        query = query or CustomerListQuery()
        return await super().list(model=CustomerListResponse, **query.to_params())

    async def iter_all(self, query: CustomerListQuery | None = None):
        query = query or CustomerListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Customer.model_validate(item)
