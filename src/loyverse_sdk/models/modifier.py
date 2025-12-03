from typing import List
from uuid import UUID
from pydantic import Field
from loyverse_sdk.models.common import Base, Pagination


class ModifierOption(Base):
    name: str
    price: float = Field(default=0.0, ge=0.0)
    position: int


class Modifier(Base):
    name: str
    position: int
    stores: List[UUID]
    modifier_options: List[ModifierOption] = Field(default_factory=list)


class ModifierListResponse(Pagination):
    items: list[Modifier] = Field(alias="modifiers")
