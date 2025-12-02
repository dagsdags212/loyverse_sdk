from loyverse_api.endpoints.base import BaseEndpoint
from loyverse_api.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_api.models import Customer, CustomerListResponse


class CustomersEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "customers"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=CustomerListResponse
        )

    async def iter_all(self):
        async for item in super().iter_all():
            yield Customer.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Customer)
