from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Tax, TaxListQuery, TaxListResponse


class TaxesEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "taxes"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Tax)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Tax)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Tax)

    async def list(self, query: TaxListQuery | None = None):
        query = query or TaxListQuery()
        return await super().list(model=TaxListResponse, **query.to_params())

    async def iter_all(self, query: TaxListQuery | None = None):
        query = query or TaxListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Tax.model_validate(item)
