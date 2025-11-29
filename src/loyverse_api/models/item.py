from uuid import UUID
from pydantic import Field
from loyverse_api.models.base import Base


class Item(Base):
    handle: str
    referenced_id: UUID | None = None
    item_name: str = Field(alias="name")
    description: str | None = None
    track_stock: bool = False
    sold_by_weight: bool = False
    is_composite: bool = False
    use_production: bool = False
    category_id: str | None = None
    primary_supplier_id: UUID | None = None
