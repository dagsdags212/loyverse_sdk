from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Category, CategoryListQuery, CategoryListResponse


class CategoriesEndpoint(BaseEndpoint, CrudMixin, ListMixin, PaginationMixin):
    path = "categories"

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Category)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Category)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Category)

    async def list(self, query: CategoryListQuery | None = None):
        query = query or CategoryListQuery()
        return await super().list(model=CategoryListResponse, **query.to_params())

    async def iter_all(self, query: CategoryListQuery | None = None):
        query = query or CategoryListQuery()
        async for item in super().iter_all(**query.to_params()):
            yield Category.model_validate(item)
