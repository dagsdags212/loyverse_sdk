from pydantic import Field
from loyverse_sdk.models.common import Base, Pagination


class Supplier(Base):
    name: str = Field(max_length=40)
    contact: str | None = Field(max_length=64)
    email: str | None = Field(default=None, max_length=64)
    phone_number: str | None = Field(default=None, max_length=15)
    website: str | None = None
    address_1: str = Field(default=None, max_length=192)
    address_2: str = Field(default=None, max_length=192)
    city: str | None = Field(default=None, max_length=64)
    region: str | None = Field(default=None, max_length=64)
    postal_code: str | None = Field(default=None, max_length=20)
    country_code: str | None = Field(default=None, max_length=2)
    note: str | None = Field(default=None, max_length=500)


class SupplierListResponse(Pagination):
    items: list[Supplier] = Field(alias="suppliers")
