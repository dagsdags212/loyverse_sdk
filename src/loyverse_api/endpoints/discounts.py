from loyverse_api.endpoints.base import BaseEndpoint
from loyverse_api.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_api.models import Discount, DiscountListResponse


class DiscountsEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "discounts"

    async def list(self, *, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=DiscountListResponse
        )

    async def iter_all(self):
        async for item in super().iter_all():
            yield Discount.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Discount)
