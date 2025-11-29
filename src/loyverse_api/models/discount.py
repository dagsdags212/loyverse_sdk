from uuid import UUID
from pydantic import Field
from loyverse_api.models.base import Base


class Discount(Base):
    type: str
    name: str
    amount: float = Field(default=0.0, alias="discount_amount")
    stores: list[UUID]
    restricted_access: bool = False
