import re
from uuid import UUID
from datetime import datetime, timedelta
from pydantic import Field, field_validator
from loyverse_api.models.base import Base


class User(Base):
    name: str
    email: str | None = None
    phone_number: str | None = None

    @field_validator("name", "email", "phone_number", mode="before")
    def sanitize_strings(cls, value: str | None) -> str | None:
        """Remove and collapse trailing whitespaces from strings"""
        if value:
            return re.sub(r"\s+", " ", value).strip()

    @field_validator("name", mode="before")
    def titlecase(cls, value: str | None) -> str | None:
        if value:
            return value.title()


class Employee(User):
    stores: str
    is_owner: bool = False

    @field_validator("stores", mode="before")
    def serialize_store_ids(cls, values) -> str:
        return ",".join(values)


class Customer(User):
    address: str | None = None
    city: str | None = Field(default=None, exclude=True)
    region: str | None = Field(default=None, exclude=True)
    postal_code: str | None = Field(default=None, exclude=True)
    country_code: str | None = Field(default=None, exclude=True)
    note: str | None = Field(default=None, exclude=True)
    customer_code: str | None = Field(default=None, exclude=True)
    first_visit: datetime | None = Field(default=None, exclude=True)
    last_visit: datetime | None = Field(default=None, exclude=True)
    total_visits: int = Field(default=1, exclude=True)
    total_spent: float = Field(default=0.0, exclude=True)
    total_points: float = Field(default=0.0, exclude=True)
    permanent_deletion_at: datetime | None = Field(default=None, exclude=True)

    def __repr__(self) -> str:
        return f"Customer(name={self.name},email={self.email},phone_number={self.phone_number})"

    def tenure(self) -> timedelta | None:
        if self.first_visit and self.last_visit:
            return self.last_visit - self.first_visit
