from typing import List
from uuid import UUID
from pydantic import Field
from loyverse_sdk.models.common import Base, Pagination


class Tax(Base):
    name: str = Field(max_length=40)
    type: str
    rate: float = Field(ge=0.0, le=100.0)
    stores: List[UUID]


class TaxListResponse(Pagination):
    items: list[Tax] = Field(alias="taxes")
