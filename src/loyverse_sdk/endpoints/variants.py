from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Variant, VariantListQuery, VariantListResponse


class VariantsEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "variants"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Variant)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Variant)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Variant)

    async def list(self, query: VariantListQuery | None = None):
        query = query or VariantListQuery()
        return await super().list(model=VariantListResponse, **query.to_params())

    async def iter_all(self, query: VariantListQuery | None = None):
        query = query or VariantListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Variant.model_validate(item)
