from uuid import UUID
from pydantic import Field, field_validator
from loyverse_api.models.base import Base


class Store(Base):
    name: str
    address: str
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str = Field(default="PH")

    @field_validator("country", mode="after")
    @classmethod
    def check_country_code_format(cls, value: str) -> str:
        if len(value) != 2:
            raise ValueError("country must be a two-letter code")
        return value
