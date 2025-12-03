from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Customer, CustomerListResponse


class CustomersEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "customers"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=CustomerListResponse
        )

    async def iter_all(self, **kwargs):
        async for item in super().iter_all(**kwargs):
            yield Customer.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Customer)
