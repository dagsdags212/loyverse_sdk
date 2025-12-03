from pydantic import Field
from loyverse_sdk.models.common import Base, Pagination


class Store(Base):
    name: str = Field(max_length=40)
    address: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=64)
    state: str | None = Field(default=None, max_length=64)
    postal_code: str | None = Field(default=None, max_length=20)
    country: str | None = Field(default=None, max_length=2)
    phone_number: str | None = Field(default=None, max_length=15)
    description: str | None = Field(default=None, max_length=128)


class StoreListResponse(Pagination):
    items: list[Store] = Field(alias="stores")
