from typing import Iterable
from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    CrudMixin,
    ListMixin,
    PaginationMixin,
)
from loyverse_sdk.models import Category, CategoryListResponse


class CategoriesEndpoint(BaseEndpoint, ListMixin, CrudMixin, PaginationMixin):
    path = "categories"

    async def list(self, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=CategoryListResponse
        )

    async def iter_all(self, **kwargs):
        async for item in super().iter_all(**kwargs):
            yield Category.model_validate(item)

    async def create(self, payload: dict):
        return await super().create(payload=payload, model=Category)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Category)

    async def update(self, id: str, payload: dict):
        return await super().update(id=id, payload=payload, model=Category)

    async def delete(self, id: str) -> Iterable[str]:
        return await super().delete(id=id)
